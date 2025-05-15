# -*- coding: utf-8 -*-

"""
GUI elements for the AutoCards addon settings.
"""

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, showWarning, qconnect

from . import config

# --- Prompt Settings Dialog ---

class PromptSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AutoCards: Prompt Settings")
        self.setMinimumWidth(400)

        self.config = config.get_config()

        layout = QVBoxLayout()

        # Prompt 1
        label1 = QLabel("Prompt for 🤖1:")
        layout.addWidget(label1)
        self.prompt1_edit = QTextEdit()
        self.prompt1_edit.setPlaceholderText("Enter the prompt for button 1...")
        self.prompt1_edit.setText(self.config.get("prompt1", ""))
        layout.addWidget(self.prompt1_edit)

        # Prompt 2
        label2 = QLabel("Prompt for 🤖2:")
        layout.addWidget(label2)
        self.prompt2_edit = QTextEdit()
        self.prompt2_edit.setPlaceholderText("Enter the prompt for button 2...")
        self.prompt2_edit.setText(self.config.get("prompt2", ""))
        layout.addWidget(self.prompt2_edit)

        # Prompt 3
        label3 = QLabel("Prompt for 🤖3:")
        layout.addWidget(label3)
        self.prompt3_edit = QTextEdit()
        self.prompt3_edit.setPlaceholderText("Enter the prompt for button 3...")
        self.prompt3_edit.setText(self.config.get("prompt3", ""))
        layout.addWidget(self.prompt3_edit)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel) # Corrected roles
        qconnect(button_box.accepted, self.save_settings) # Pass the signal directly
        qconnect(button_box.rejected, self.reject)       # Pass the signal directly
        layout.addWidget(button_box)

        self.setLayout(layout)

    def save_settings(self):
        """Saves the prompt settings."""
        new_config_data = {
            "prompt1": self.prompt1_edit.toPlainText(),
            "prompt2": self.prompt2_edit.toPlainText(),
            "prompt3": self.prompt3_edit.toPlainText() # Add prompt 3
        }
        config.update_config(new_config_data)
        showInfo("Prompt settings saved successfully.")
        self.accept()

def show_prompt_settings_dialog():
    """Shows the prompt settings dialog."""
    dialog = PromptSettingsDialog(mw.app.activeWindow())
    dialog.exec() # Use exec() instead of exec_()

# --- API and Model Settings Dialog ---

class ApiSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AutoCards: API and Model Settings")
        self.setMinimumWidth(400)

        self.config = config.get_config()

        layout = QVBoxLayout()

        # API Keys (up to 5)
        self.api_key_edits = []
        layout.addWidget(QLabel("Gemini API Keys (at least 1, max 5):"))
        for i in range(5):
            label_text = f"API Key {i+1}"
            if i > 0:
                label_text += " (Optional)"
            label = QLabel(label_text + ":")
            layout.addWidget(label)
            api_key_edit = QLineEdit()
            api_key_edit.setEchoMode(QLineEdit.EchoMode.Password) # Corrected EchoMode
            api_key_edit.setPlaceholderText(f"Enter API Key {i+1}")
            # Load existing keys, handle index out of bounds
            if i < len(self.config.get("api_keys", [])):
                 api_key_edit.setText(self.config["api_keys"][i])
            self.api_key_edits.append(api_key_edit)
            layout.addWidget(api_key_edit)

        # Model Name
        layout.addWidget(QLabel("Gemini Model Name:"))
        self.model_name_edit = QLineEdit()
        self.model_name_edit.setPlaceholderText("e.g., gemini-2.5-flash-preview-04-17")
        self.model_name_edit.setText(self.config.get("model_name", "gemini-2.5-flash-preview-04-17"))
        layout.addWidget(self.model_name_edit)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel) # Corrected roles
        qconnect(button_box.accepted, self.save_settings) # Pass the signal directly
        qconnect(button_box.rejected, self.reject)       # Pass the signal directly
        layout.addWidget(button_box)

        self.setLayout(layout)

    def save_settings(self):
        """Saves the API and Model settings."""
        api_keys = [edit.text().strip() for edit in self.api_key_edits if edit.text().strip()]
        if not api_keys:
            showWarning("Please enter at least one API key.")
            return

        new_config_data = {
            "api_keys": api_keys,
            "model_name": self.model_name_edit.text().strip()
        }
        # Reset current_api_key_index if the list of keys changed significantly
        current_index = self.config.get("current_api_key_index", 0)
        if current_index >= len(api_keys):
             new_config_data["current_api_key_index"] = 0

        config.update_config(new_config_data)
        showInfo("API and Model settings saved successfully.")
        self.accept()

def show_api_settings_dialog():
    """Shows the API and Model settings dialog."""
    dialog = ApiSettingsDialog(mw.app.activeWindow())
    dialog.exec() # Use exec() instead of exec_()