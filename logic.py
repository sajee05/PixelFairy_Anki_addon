# -*- coding: utf-8 -*-

"""
Core logic for the AutoCards addon, handling editor button clicks and field updates.
"""

from aqt import mw
from aqt.utils import showInfo, showWarning, qconnect
from aqt.editor import Editor
from aqt.qt import QProgressDialog, Qt, QObject, QThread, pyqtSignal # Import threading components
from aqt.browser import Browser # Added Browser import
import logging # Import the logging module

# Import vendored markdown library
import markdown

from . import config
from . import api_handler

# --- Worker Thread for API Calls ---

class Worker(QObject):
    """Runs the API call in a separate thread."""
    finished = pyqtSignal(object, object) # Signal to emit result (text or None) and potential error

    def __init__(self, content_html, prompt, model_name):
        super().__init__()
        self.content_html = content_html
        self.prompt = prompt
        self.model_name = model_name

    def run(self):
        """Execute the API call."""
        try:
            result = api_handler.call_gemini(self.content_html, self.prompt, self.model_name)
            self.finished.emit(result, None) # Emit result, no error
        except Exception as e:
            self.finished.emit(None, e) # Emit None for result, pass the exception

# --- Main Logic ---

# Store thread and worker globally to prevent premature garbage collection
# This is a simple approach; a more robust solution might manage these differently
current_thread = None
current_worker = None

def on_autocards_button_click(editor: Editor, button_number: int):
    """
    Handles the click event for the AutoCards editor buttons.
    Gets field content, calls API in background thread, and updates the field.
    Gets field content, calls API, and updates the field.
    """
    cfg = config.get_config()

    # Determine which prompt to use
    prompt_key = f"prompt{button_number}"
    prompt = cfg.get(prompt_key, "").strip()

    if not prompt:
        showWarning(f"Prompt for 🤖{button_number} is not configured. Please go to Tools > Addons > AutoCards by M Sajeel🤖 > Add Prompts to set it up.")
        return

    # Get the index of the currently focused field
    field_index = editor.currentField

    if field_index is None:
        showWarning("Please focus on a field before clicking the button.")
        return

    # Get the content of the focused field (HTML content)
    original_html = editor.note.fields[field_index]

    # Get the model name
    model_name = cfg.get("model_name", "gemini-2.5-flash-preview-04-17")

    global current_thread, current_worker # Use global references

    # --- Setup Progress Dialog ---
    progress_dialog = QProgressDialog(
        "Pixel fairies are painting your card…",
        None, # No cancel button text needed as it's hidden
        0, 0, editor.widget
    )
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setWindowTitle("AutoCards Processing")
    progress_dialog.setCancelButton(None) # Hide cancel button

    # --- Setup Worker and Thread ---
    current_thread = QThread()
    current_worker = Worker(original_html, prompt, model_name)
    current_worker.moveToThread(current_thread)

    # --- Define Slot for Handling Result ---
    def handle_api_result(result_text, error):
        logging.info("handle_api_result called.") # Log entry
        progress_dialog.close() # Close dialog first

        if error:
            logging.error(f"API call finished with error: {error}")
            showWarning(f"API call failed: {error}")
            # api_handler.call_gemini might have shown more specific warnings already
        elif result_text is not None:
            logging.info(f"API call successful. Result length: {len(result_text)}")
            try:
                # Convert Markdown response to HTML
                logging.info("Converting Markdown to HTML...")
                generated_html = markdown.markdown(result_text)
                logging.info("Markdown conversion successful.")

                # Determine placement based on config
                placement = cfg.get("output_placement", "top") # Default to top
                logging.info(f"Output placement setting: {placement}")

                # Combine generated content with original content based on placement
                if placement == "replace":
                    combined_html = generated_html
                    logging.info("Combined HTML prepared (Replace).")
                elif placement == "below":
                    combined_html = original_html + "<br><hr><br>" + generated_html
                    logging.info("Combined HTML prepared (Below).")
                else: # Default to "top"
                    combined_html = generated_html + "<br><hr><br>" + original_html
                    logging.info("Combined HTML prepared (Top).")

                # Update the field content using JavaScript
                # Escape necessary characters for JS string literal
                escaped_html = combined_html.replace('\\', '\\\\').replace("'", "\\'").replace('`', '\\`').replace('\n', '\\n')
                # 1. Update the Python Note object directly
                logging.info(f"Updating editor.note.fields[{field_index}] directly...")
                editor.note.fields[field_index] = combined_html
                logging.info("Python note field updated.")

                # 2. Reload the note in the editor to display the updated field content
                logging.info("Calling editor.loadNote(True) to refresh display...")
                editor.loadNote(True) # Load the current note to show changes
                logging.info("editor.loadNote(True) called.")

            except Exception as update_err:
                logging.error(f"Error updating field after successful API call: {update_err}", exc_info=True)
                showWarning(f"Error updating field after successful API call: {update_err}")
        else:
            # API call was likely cancelled or failed silently (should be caught by error signal)
            # api_handler should have shown a warning if applicable
            pass

        # Clean up thread
        current_thread.quit()
        current_thread.wait()

    # --- Connect Signals and Start Thread ---
    current_worker.finished.connect(handle_api_result)
    current_thread.started.connect(current_worker.run)
    # Optional: Connect finished signal for cleanup if needed, but handle_api_result does it
    # current_thread.finished.connect(current_thread.deleteLater) # Schedule thread deletion
    # current_worker.finished.connect(current_worker.deleteLater) # Schedule worker deletion

    current_thread.start()
    progress_dialog.show() # Show dialog after starting thread
# --- Browser Context Menu Handler ---

def on_autocards_browser_menu_action(browser: Browser, editor: Editor, button_number: int):
    """
    Handles the action triggered from the browser editor's context menu.
    Similar to on_autocards_button_click but uses the browser's editor instance.
    """
    cfg = config.get_config()
    prompt_key = f"prompt{button_number}"
    prompt = cfg.get(prompt_key, "").strip()

    if not prompt:
        showWarning(f"Prompt for 🤖{button_number} is not configured. Please go to Tools > Addons > AutoCards by M Sajeel🤖 > Add Prompts to set it up.")
        return

    # Get the index of the currently focused field from the browser editor
    field_index = editor.currentField
    if field_index is None:
        # This might happen if the click wasn't directly in a field's content area
        showWarning("Could not determine the focused field in the browser editor. Please right-click directly within the text area of the field.")
        return

    # Get the content of the focused field (HTML content)
    # Note: Browser editor might require flushing changes first if edited manually
    editor.web.eval("focusManager.flush();") # Ensure latest content is available
    original_html = editor.note.fields[field_index]

    # Get the model name
    model_name = cfg.get("model_name", "gemini-2.5-flash-preview-04-17")

    # --- Use the same threading mechanism ---
    global current_thread, current_worker

    # --- Setup Progress Dialog (parent is browser window) ---
    # Use mw.app.activeWindow() as a more reliable parent than browser directly
    progress_dialog = QProgressDialog(
        "Pixel fairies are painting your card…",
        None, 0, 0, mw.app.activeWindow()
    )
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setWindowTitle("AutoCards Processing")
    progress_dialog.setCancelButton(None)

    # --- Setup Worker and Thread ---
    current_thread = QThread()
    current_worker = Worker(original_html, prompt, model_name)
    current_worker.moveToThread(current_thread)

    # --- Define Slot for Handling Result ---
    def handle_api_result(result_text, error):
        logging.info("handle_api_result (Browser) called.") # Log entry
        progress_dialog.close()

        if error:
            logging.error(f"API call (Browser) finished with error: {error}")
            showWarning(f"API call failed: {error}")
        elif result_text is not None:
            logging.info(f"API call (Browser) successful. Result length: {len(result_text)}")
            try:
                logging.info("Converting Markdown to HTML (Browser)...")
                generated_html = markdown.markdown(result_text)
                logging.info("Markdown conversion successful (Browser).")

                # Determine placement based on config
                placement = cfg.get("output_placement", "top") # Default to top
                logging.info(f"Output placement setting (Browser): {placement}")

                # Combine generated content with original content based on placement
                if placement == "replace":
                    combined_html = generated_html
                    logging.info("Combined HTML prepared (Browser - Replace).")
                elif placement == "below":
                    combined_html = original_html + "<br><hr><br>" + generated_html
                    logging.info("Combined HTML prepared (Browser - Below).")
                else: # Default to "top"
                    combined_html = generated_html + "<br><hr><br>" + original_html
                    logging.info("Combined HTML prepared (Browser - Top).")

                # 1. Update the Python Note object directly
                logging.info(f"Updating editor.note.fields[{field_index}] directly (Browser)...")
                editor.note.fields[field_index] = combined_html
                logging.info("Python note field updated (Browser).")

                # 2. Use JS to update the visual representation in the webview
                escaped_html = combined_html.replace('\\', '\\\\').replace("'", "\\'").replace('`', '\\`').replace('\n', '\\n')
                js_code = f"""
                    (function() {{
                        var field = document.getElementById('f{field_index}');
                        if (field) {{
                            field.innerHTML = `{escaped_html}`;
                            // Trigger blur event after setting innerHTML in browser
                            field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        }} else {{
                            console.error('AutoCards (Browser): Could not find field f{field_index} to set innerHTML.');
                        }}
                    }})();
                """
                logging.info(f"Executing JS to set innerHTML for f{field_index} (Browser)...")
                editor.web.eval(js_code)
                logging.info("JS execution for innerHTML attempted (Browser).")

            except Exception as update_err:
                logging.error(f"Error updating field in browser after successful API call: {update_err}", exc_info=True)
                showWarning(f"Error updating field in browser after successful API call: {update_err}")
        # Clean up thread
        current_thread.quit()
        current_thread.wait()

    # --- Connect Signals and Start Thread ---
    current_worker.finished.connect(handle_api_result)
    current_thread.started.connect(current_worker.run)
    current_thread.start()
    progress_dialog.show()