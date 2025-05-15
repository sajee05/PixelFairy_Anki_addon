# ✨ Pixel Fairy (by M Saajeel) ⭐: Your AI Assistant for Anki Card Creation!

Tired of manually typing out definitions, explanations, or questions for your Anki cards? Let **Pixel Fairy** do the heavy lifting! This addon integrates the power of the **Google Gemini API** directly into your Anki editor, helping you create richer, more effective flashcards faster than ever.

## 🌟 Why You'll Love Pixel Fairy 🌟

* **AI-Powered Content Generation:** Select text or an image in your card, choose a custom instruction (prompt), and watch Pixel Fairy generate definitions, explanations, summaries, questions, and more!
* **Your Prompts, Your Control:** Craft up to three unique prompts tailored to your study needs. Want definitions? Explanations? Questions about an image? You decide what the AI does!
* **Image-to-Text Magic:** Pixel Fairy can "see" images in your cards! Ask it to describe an image, generate questions about it, or extract text.
* **Flexible & Efficient:**
  * Supports up to **5 Google Gemini API keys** with automatic rotation to help manage usage and avoid rate limits.
  * Choose where the AI-generated content goes: **replace** your selection, add it **on top**, or place it **below**.
* **Seamless Workflow:**
  * Quick access buttons (🤖1, 🤖2, 🤖3) directly in the Anki editor.
  * Handy keyboard shortcuts (`Ctrl+1`, `Ctrl+2`, `Ctrl+3`) for lightning-fast use.
  * Works from the Anki browser's context menu too!

## 🚀 How to Get Started (Setup - Very Important!) 🚀

1. **Install Pixel Fairy:**
   
   * Download the addon from this page (look for a `.ankiaddon` file or an addon ID).
   * In Anki, go to `Tools > Add-ons`.
   * If you have the file, drag & drop it onto the Add-ons window or use "Install From File...". If you have an ID, use "Get Add-ons...".
   * Restart Anki.

2. **🔑 Add Your Google Gemini API Key(s):**
   
   * Pixel Fairy needs a Google Gemini API key to work. You can get one from [Google AI Studio](https://aistudio.google.com/).
   * In Anki, go to: `Tools > Pixel Fairy (by M Saajeel) ⭐ > API and Model Settings`.
   * Enter your API key(s) (up to 5).
   * **This step is crucial! Without an API key, Pixel Fairy cannot function.**

3. **✍️ Create Your Custom Prompts:**
   
   * This is where you tell Pixel Fairy what you want the AI to do!
   * In Anki, go to: `Tools > Pixel Fairy (by M Saajeel) ⭐ > Add Prompts`.
   * Set up "Prompt 1", "Prompt 2", and/or "Prompt 3".
   * **Examples:**
     * `"Explain the selected text simply:"`
     * `"Generate 3 questions about this:"`
     * `"Describe this image for a flashcard:"`
   * **The default prompts are BLANK. You MUST set your own prompts for the addon to be useful!**

4. **(Optional) Configure Model & Output:**
   
   * In `API and Model Settings`, you can specify the Gemini model (e.g., `gemini-pro`).
   * In `Tools > Pixel Fairy (by M Saajeel) ⭐ > Output Placement`, choose if new content replaces, goes above, or below your selection.

## 💡 How to Use Pixel Fairy 💡

1. In the Anki editor, **select some text** in a field, or make sure an **image (`<img>` tag)** is present.
2. Click one of the **Pixel Fairy buttons (🤖1, 🤖2, 🤖3)** or use the shortcuts (`Ctrl+1`, `Ctrl+2`, `Ctrl+3`).
3. A "Working..." dialog will appear.
4. Voilà! The AI-generated content appears in your card, formatted and ready!

## ✨ Unlock Your Card Creation Superpowers! (Use Cases) ✨

* **Generate Definitions:** Quickly get definitions for new vocabulary.
* **Create Questions:** Turn notes into cloze deletions, short answer, or multiple-choice questions.
* **Summarize Text:** Condense long articles or paragraphs.
* **Explain Concepts:** Get simplified explanations of complex topics.
* **Translate:** Instantly translate text snippets.
* **Describe Images:** Get textual descriptions of images in your cards.
* **Ask About Images:** Generate questions based on visual content.
* ...and much more! Experiment with your prompts!

## ⚠️ Important Notes ⚠️

* **You NEED your own Google Gemini API key(s).** The addon does not come with one.
* **You MUST set up your own custom prompts.** The default prompts are empty and will not generate useful content.
* The addon uses the Google Gemini API. Your usage of the API may be subject to Google's terms of service and pricing (though they often have a generous free tier). Please check Google's official documentation for details.
* Image processing works with standard `<img>` tags. It skips Data URIs and very large images.

---

We hope Pixel Fairy helps you create amazing Anki cards more efficiently!
If you have issues or feedback, please check the GitHub repository by clicking on "Contact Author"