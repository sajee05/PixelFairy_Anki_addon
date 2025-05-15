# Pixel Fairy (by M Saajeel) ⭐

Pixel Fairy is an Anki addon designed to supercharge your flashcard creation process by leveraging the power of the Google Gemini API. Select text or images within your card fields, choose a custom prompt, and let Pixel Fairy generate relevant content for you, seamlessly integrating it back into your cards.

## Features

* **Custom Prompts:**
  * Configure up to three distinct custom prompts (referred to as "Prompt 1", "Prompt 2", "Prompt 3").
  * Easily set up your prompts via the "Add Prompts" dialog (accessible from Tools > Pixel Fairy (by M Saajeel) ⭐ > Add Prompts).
  * Each prompt is linked to dedicated editor buttons (🤖1, 🤖2, 🤖3) and keyboard shortcuts for quick access.
* **Multiple API Key Management:**
  * Supports up to five Google Gemini API keys.
  * Configure your API keys via the "API and Model Settings" dialog (Tools > Pixel Fairy (by M Saajeel) ⭐ > API and Model Settings).
  * **API Key Rotation:** Automatically rotates through your provided API keys to distribute usage, helping to mitigate rate limits and improve reliability.
* **Image Handling:**
  * Processes `<img>` tags found in your card's field HTML.
  * Sends image data along with any selected text to the Gemini API for context-aware generation (e.g., "describe this image" or "what questions can be asked about this image?").
  * Skips Data URIs and oversized images to ensure efficient processing.
* **Keyboard Shortcuts:**
  * `Ctrl+1`: Trigger Prompt 1.
  * `Ctrl+2`: Trigger Prompt 2.
  * `Ctrl+3`: Trigger Prompt 3.
* **Configurable Output Placement:**
  * Choose where the AI-generated content is inserted relative to your selection/original content.
  * Options: "Replace", "On Top", "Below the input".
  * Configure via the Tools > Pixel Fairy (by M Saajeel) ⭐ > Output Placement menu. 
* **Markdown to HTML Conversion:**
  * The addon expects Markdown formatted responses from the Gemini API and automatically converts them to HTML for proper rendering in Anki fields. 

## Installation

1. Download the addon package (e.g., `PixelFairy.ankiaddon`) from the AnkiWeb addon page or GitHub releases.
2. In Anki, go to Tools > Add-ons.
3. Drag and drop the `PixelFairy.ankiaddon` file onto the Add-ons window, or click "Install From File..." and select it.
4. Restart Anki.

Alternatively, you might be able to install by using an AnkiWeb ID if provided on the addon page.

## Configuration

**IMPORTANT FIRST STEPS: For Pixel Fairy to function, you MUST configure your Google Gemini API keys and your custom prompts.** 

1. **Setting up Google Gemini API Keys:**
   
   * You need at least one Google Gemini API key. You can obtain these from [Google AI Studio](https://aistudio.google.com/) or the [Google Cloud Console](https://console.cloud.google.com/).
   * In Anki, go to **Tools > Pixel Fairy (by M Saajeel) ⭐ > API and Model Settings**.
   * Enter your API key(s) in the provided fields. You can add up to five keys from five different accounts.
   * The addon will rotate through these keys for API calls.

2. **Setting up Custom Prompts:**
   
   * Pixel Fairy allows you to define up to three custom prompts. These are the instructions you will send to the AI.
   * In Anki, go to **Tools > Pixel Fairy (by M Saajeel) ⭐ > Add Prompts**.
   * Enter your desired prompt text for "Prompt 1", "Prompt 2", and/or "Prompt 3".
   * **Example Prompts:**
     * "Explain this concept in simple terms:"
     * "Generate three multiple-choice questions about the following text:"
     * "Describe the key elements in this image."
     * "Translate the following text to Spanish:"

3. **Choosing a Gemini Model:**
   
   * In the **Tools > Pixel Fairy (by M Saajeel) ⭐ > API and Model Settings** dialog, you can specify the Gemini model you wish to use (e.g., `gemini-2.0-flash`, etc). Ensure the model name is compatible with the Gemini API and your API key's permissions.

4. **Output Placement:**
   
   * Configure how the generated content is inserted:
     * Go to **Tools > Pixel Fairy (by M Saajeel) ⭐ > Output Placement**.
     * Select one of the options:
       * **Replace:** Replaces the selected text/content.
       * **On Top:** Inserts the generated content above the selected text/original content.
       * **Below the input:** Inserts the generated content below the selected text/original content.

All configuration settings are managed by [`config.py`](config.py) and stored in [`config.json`](config.json) in the addon's directory.

## Usage

1. Open the Anki card editor for a note.
2. Select text or an image within a field that you want to use as input for the AI. If no text is selected, the addon might process the entire field content or behave based on the prompt's nature.
3. Click one of the editor buttons (🤖1, 🤖2, 🤖3) corresponding to your pre-configured custom prompts, or use the keyboard shortcuts:
   * `Ctrl+1` for Prompt 1
   * `Ctrl+2` for Prompt 2
   * `Ctrl+3` for Prompt 3
4. Alternatively, when using the Anki browser, you can right-click on selected notes to access the Pixel Fairy prompts via the context menu.
5. A progress dialog will appear while Pixel Fairy communicates with the Google Gemini API.
6. Once the API responds, the generated content (converted from Markdown to HTML) will be inserted into the field according to your "Output Placement" setting.

## Use Cases

Pixel Fairy can be used for a wide variety of card creation tasks, including:

* **Automated Content Generation:**
  * Generate definitions for vocabulary.
  * Create explanations for complex topics.
* **Question Generation:**
  * Formulate cloze deletions.
  * Create key questions based on provided text.
  * Generate multiple-choice questions.
* **Summarization:** Condense long passages of text.
* **Elaboration/Explanation:** Expand on brief notes or concepts.
* **Translation:** Translate selected text into different languages.
* **Image-to-Text:**
  * Generate descriptions for images.
  * Create questions based on the content of an image.

## API Key Rotation

The addon supports up to five Google Gemini API keys. If you provide multiple keys:

* Pixel Fairy will cycle through them for subsequent API requests.
* This helps distribute the load and can mitigate issues with API rate limits if you are a heavy user.

## Troubleshooting/FAQ

* **Q: The addon isn't doing anything, or I'm getting errors.**
  
  * **A:** The most common reason is missing configuration.
    1. **Ensure you have entered valid Google Gemini API key(s)** in Tools > Pixel Fairy (by M Saajeel) ⭐ > API and Model Settings.
    2. **Ensure you have configured at least one custom prompt** in Tools > Pixel Fairy (by M Saajeel) ⭐ > Add Prompts. The default prompts are empty and will not work.
    3. Check your internet connection.
    4. Verify that the Gemini model name you've specified is correct and accessible with your API key.

* **Q: How do I get Google Gemini API Keys?**
  
  * **A:** You can obtain API keys for the Google Gemini API by visiting the [Google AI Studio](https://aistudio.google.com/) or the [Google Cloud Console](https://console.cloud.google.com/). Follow Google's instructions for generating an API key.

* **Q: An image in my card field isn't being processed.**
  
  * **A:** Pixel Fairy processes `<img>` tags with `src` attributes pointing to image files or accessible URLs. It will skip images embedded as Data URIs (e.g., `data:image/png;base64,...`) and may also skip extremely large images to prevent errors or excessive processing times. Ensure your image is correctly formatted.

* **Q: Can I use this addon for free?**
  
  * **A:** The addon itself is free. However, usage of the Google Gemini API may be subject to Google's pricing and free tier limits. Please refer to Google's official Gemini API documentation for details on usage costs.

---

Enjoy using Pixel Fairy to enhance your Anki workflow!

Crafted with passion by M Saajeel!
## Showcase and tutorial
&lt;a href="https://youtu.be/R19qORouQ_4?feature=shared" target="_blank"&gt;
  &lt;img src="https://i.ibb.co/gZ4Yp2g/Pixel-Fairy-Showcase-Tutorial.png" alt="Showcase and tutorial" style="max-width: 560px;"&gt;
&lt;/a&gt;

&lt;a href="https://www.buymeacoffee.com/he7cules" target="_blank"&gt;&lt;img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" &gt;&lt;/a&gt;
&lt;script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="he7cules" data-color="#FFDD00" data-emoji=""  data-font="Arial" data-text="Support the Creator" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" &gt;&lt;/script&gt;