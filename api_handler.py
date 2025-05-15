# -*- coding: utf-8 -*-

"""
Handles interaction with the Gemini API, including key rotation and error handling.
"""

from aqt.qt import *
from aqt.utils import showInfo, showWarning, askUser
from aqt import mw

import google.generativeai as genai
import base64
import re # To extract image data from HTML
import logging # Added for debugging
import os # To construct file paths
import mimetypes # To guess image MIME types

# Configure basic logging (adjust level and format as needed)
# Consider writing to a file in production: logging.basicConfig(filename='autocards_debug.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from . import config

def get_current_api_key():
    """Gets the current API key from the configuration, handling index."""
    cfg = config.get_config()
    api_keys = cfg.get("api_keys", [])
    current_index = cfg.get("current_api_key_index", 0)

    if not api_keys:
        showWarning("No Gemini API keys configured. Please go to Tools > Addons > AutoCards by M Sajeel🃏 > API and Model Settings to add one.")
        return None

    if current_index >= len(api_keys):
        # Reset index if it's out of bounds (shouldn't happen with proper saving, but as a safeguard)
        current_index = 0
        cfg["current_api_key_index"] = current_index
        config.save_config()

    return api_keys[current_index]

def rotate_api_key():
    """Rotates the API key index in the configuration."""
    cfg = config.get_config()
    api_keys = cfg.get("api_keys", [])
    current_index = cfg.get("current_api_key_index", 0)

    if not api_keys:
        return # Nothing to rotate

    new_index = (current_index + 1) % len(api_keys)
    cfg["current_api_key_index"] = new_index
    config.save_config()

# Removed the old extract_image_data_from_html function as it's insufficient
# We will handle image extraction directly within call_gemini

def call_gemini(content_html, prompt, model_name):
    """
    Calls the Gemini API with the given content and prompt.
    Handles API key rotation and retry on failure.
    Returns the generated text or None on unrecoverable error/cancel.
    """
    retry_count = 0
    max_retries = len(config.get_config().get("api_keys", [])) * 2 # Allow trying each key twice

    while retry_count < max_retries:
        api_key = get_current_api_key()
        if api_key is None:
            return None # No keys configured

        genai.configure(api_key=api_key)

        try:
            model = genai.GenerativeModel(model_name)
            logging.info(f"Preparing content for Gemini. Prompt: '{prompt[:100]}...', Model: {model_name}")

            # Prepare content parts for the API
            content_parts = []
            if prompt:
                content_parts.append(prompt)

            # --- New Image Handling Logic ---
            logging.info(f"Processing HTML for images: {content_html[:200]}...")
            processed_html = content_html # Start with original HTML
            media_dir = mw.col.media.dir() # Get Anki's media directory
            img_tags_found = re.findall(r'(<img[^>]+src="([^"]+)"[^>]*>)', content_html, re.IGNORECASE) # Find all img tags and their src

            image_added = False
            if not media_dir:
                logging.warning("Could not determine Anki media directory. Cannot process local image files.")
            else:
                logging.info(f"Found {len(img_tags_found)} potential image tags. Media dir: {media_dir}")
                for full_tag, src_value in img_tags_found:
                    # Skip data URIs for now, focus on file references
                    if src_value.startswith('data:'):
                        logging.info(f"Skipping data URI image: {src_value[:50]}...")
                        continue

                    img_filename = src_value
                    img_path = os.path.join(media_dir, img_filename)
                    logging.info(f"Checking for image file: {img_path}")

                    if os.path.exists(img_path):
                        try:
                            with open(img_path, "rb") as f:
                                img_bytes = f.read()

                            mime_type, _ = mimetypes.guess_type(img_path)
                            if not mime_type:
                                mime_type = 'application/octet-stream' # Default if type unknown
                                logging.warning(f"Could not guess MIME type for {img_filename}, using default.")
                            elif mime_type.lower() == 'image/jpg': # Explicitly check for jpg and convert to jpeg
                                mime_type = 'image/jpeg'
                                logging.info(f"Corrected MIME type from image/jpg to image/jpeg for {img_filename}")

                            # Check size (Gemini 2.5 Flash limit is 20MB)
                            if len(img_bytes) < 20 * 1024 * 1024:
                                logging.info(f"Adding image part: file={img_filename}, mime_type={mime_type}, size={len(img_bytes)} bytes")
                                content_parts.append({
                                    'mime_type': mime_type, # Use potentially corrected mime_type
                                    'data': img_bytes
                                })
                                image_added = True
                                # Remove the processed img tag from the HTML that will be sent as text
                                processed_html = processed_html.replace(full_tag, '', 1)
                            else:
                                logging.warning(f"Image file {img_filename} is too large ({len(img_bytes)} bytes), skipping. Max size is 20MB.")
                                # Keep the tag in HTML for context? Or remove? Let's remove it to avoid confusion.
                                processed_html = processed_html.replace(full_tag, f'[Image "{img_filename}" skipped - too large]', 1)

                        except Exception as read_err:
                            logging.error(f"Error reading image file {img_path}: {read_err}", exc_info=True)
                            # Keep the tag in HTML but maybe add a note?
                            processed_html = processed_html.replace(full_tag, f'[Image "{img_filename}" skipped - read error]', 1)
                    else:
                        logging.warning(f"Image file not found: {img_path}. Skipping tag.")
                        # Remove the tag for the missing image
                        processed_html = processed_html.replace(full_tag, f'[Image "{img_filename}" skipped - not found]', 1)

            # Add the remaining/processed HTML content as a text part, if any
            final_text_part = processed_html.strip()
            if final_text_part:
                logging.info(f"Adding final text part (HTML with processed img tags): {final_text_part[:150]}...")
                content_parts.append(final_text_part)
            elif not image_added and not prompt:
                # Handle case where HTML was *only* an image tag that got removed, and there's no prompt
                logging.warning("No text prompt and image could not be processed or was removed. Sending empty content list might cause errors.")
                # Optionally add a placeholder text part?
                # content_parts.append(" ") # Avoid sending empty list

            # --- End New Image Handling Logic ---

            # Log the structure of content_parts before sending
            loggable_parts = []
            for part in content_parts:
                if isinstance(part, str):
                    loggable_parts.append(f'str(len={len(part)})')
                elif isinstance(part, dict) and 'mime_type' in part and 'data' in part:
                    loggable_parts.append(f"dict(mime_type='{part['mime_type']}', data_len={len(part['data'])})")
                else:
                    loggable_parts.append(f'Unknown_Type({type(part)})')
            logging.info(f"Final content_parts structure being sent to Gemini: {loggable_parts}")

            # Make the API call
            # Use generate_content for multimodal or text-only
            response = model.generate_content(content_parts)
            logging.info("Gemini API call successful.")

            # Check for empty response or errors within the response object
            if not response or not response.text:
                 raise Exception("Gemini API returned an empty response.")

            # Success
            rotate_api_key() # Rotate key on success for load balancing/distribution
            return response.text

        except Exception as e:
            error_message = f"Gemini API Error (Key Index: {config.get_config().get('current_api_key_index', 0)}):\n{e}"
            logging.error(f"Gemini API Error: {error_message}", exc_info=True) # Log full traceback
            showWarning(error_message)

            # Ask user if they want to retry
            retry = askUser("API call failed. Retry with next API key?", defaultno=False)

            if retry:
                rotate_api_key() # Rotate key for the retry attempt
                retry_count += 1
                # Continue loop
            else:
                # User cancelled
                return None # Return None on cancel

    # If loop finishes without success
    logging.warning("Max retry attempts reached for Gemini API call.")
    showWarning("Max retry attempts reached. Could not get a response from the Gemini API.")
    return None