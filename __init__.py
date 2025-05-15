# -*- coding: utf-8 -*-

"""
An Anki addon to generate flashcard content using the Gemini API.
"""

import os
import sys

# Add vendor directory to sys.path FIRST for dependencies
addon_path = os.path.dirname(__file__)
vendor_path = os.path.join(addon_path, "vendor")
if vendor_path not in sys.path:
    sys.path.insert(0, vendor_path)

# Import necessary Anki modules AFTER setting path
from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.editor import Editor
from aqt.gui_hooks import editor_did_init_buttons, profile_did_open, browser_will_show_context_menu # Changed browser hook
from aqt.qt import QAction, QMenu, QActionGroup # Added QMenu and QActionGroup
from aqt.browser import Browser # Added Browser import

# Import custom modules
from . import config
from . import gui
from . import logic

# Add menu items
def add_menu_items():
    addon_manager = mw.addonManager
    addon_name = addon_manager.addonName(__name__)

    # Create submenu
    addon_menu = mw.form.menuTools.addMenu(f"Pixel Fairy (by M Saajeel) ⭐")

    # Add Prompts settings action
    action_prompts = QAction("Add Prompts", mw)
    qconnect(action_prompts.triggered, gui.show_prompt_settings_dialog)
    addon_menu.addAction(action_prompts)

    # API and Model settings action
    action_api = QAction("API and Model Settings", mw)
    qconnect(action_api.triggered, gui.show_api_settings_dialog)
    addon_menu.addAction(action_api)
    addon_menu.addSeparator() # Add a separator

    # --- Output Placement Submenu ---
    placement_menu = addon_menu.addMenu("Output Placement")
    placement_group = QActionGroup(placement_menu) # Group to ensure exclusivity

    # Define handler function
    def update_output_placement(placement_value):
        config.update_config({"output_placement": placement_value})
        # Optional: showInfo(f"Output placement set to: {placement_value}")

    # Create actions
    action_replace = QAction("Replace", mw, checkable=True)
    action_top = QAction("On Top", mw, checkable=True)
    action_below = QAction("Below the input", mw, checkable=True)

    # Add actions to group and menu
    placement_group.addAction(action_replace)
    placement_group.addAction(action_top)
    placement_group.addAction(action_below)
    placement_menu.addAction(action_replace)
    placement_menu.addAction(action_top)
    placement_menu.addAction(action_below)

    # Connect signals
    qconnect(action_replace.triggered, lambda: update_output_placement("replace"))
    qconnect(action_top.triggered, lambda: update_output_placement("top"))
    qconnect(action_below.triggered, lambda: update_output_placement("below"))

    # Set initial check state
    current_placement = config.get_config().get("output_placement", "top") # Default to 'top' if missing
    if current_placement == "replace":
        action_replace.setChecked(True)
    elif current_placement == "below":
        action_below.setChecked(True)
    else: # Default to "top"
        action_top.setChecked(True)


# Add buttons to editor toolbar
def add_editor_buttons(buttons, editor):
    # Button 1
    btn1 = editor.addButton(
        id="autocards_btn1", # Use id= for clarity
        icon=None, # No specific icon path needed if using label
        cmd="autocards_cmd1", # Define a command name
        func=lambda e=editor: logic.on_autocards_button_click(e, 1),
        tip="AutoCards: Generate with Prompt 1 (Ctrl+1)", # Update tooltip
        label="🤖1", # New label
        keys="Ctrl+1" # Add shortcut
    )
    buttons.append(btn1)

    # Button 2
    btn2 = editor.addButton(
        id="autocards_btn2", # Use id= for clarity
        icon=None, # No specific icon path needed if using label
        cmd="autocards_cmd2", # Define a command name
        func=lambda e=editor: logic.on_autocards_button_click(e, 2),
        tip="AutoCards: Generate with Prompt 2 (Ctrl+2)", # Update tooltip
        label="🤖2", # New label
        keys="Ctrl+2" # Add shortcut
    )
    buttons.append(btn2)

    # Button 3
    btn3 = editor.addButton(
        id="autocards_btn3",
        icon=None,
        cmd="autocards_cmd3",
        func=lambda e=editor: logic.on_autocards_button_click(e, 3),
        tip="AutoCards: Generate with Prompt 3 (Ctrl+3)",
        label="🤖3",
        keys="Ctrl+3"
    )
    buttons.append(btn3)

    return buttons

# Add context menu items to Browser editor fields
def add_browser_context_menu_items(browser: Browser, menu: QMenu):
    # This hook (`browser_will_show_context_menu`) is called for various context menus in the browser.
    # We need to check if the context is specifically the editor's webview.
    # The editor instance is typically available via browser.editor when the context is right.
    editor = getattr(browser, "editor", None)
    if not editor or not editor.web: # Check if editor and its webview exist
        return

    # A heuristic check: if the menu has actions related to standard editing (cut/copy/paste),
    # it's likely the editor's context menu. This isn't foolproof but often works.
    action_texts = [action.text() for action in menu.actions()]
    if "Cut" not in action_texts and "Copy" not in action_texts and "Paste" not in action_texts:
         return # Probably not the editor field's context menu

    current_field_index = editor.currentField # Get the index of the field clicked in

    if current_field_index is None:
        return # No field selected

    # Create AutoCards submenu
    submenu = menu.addMenu("Pixel Fairy (by M Saajeel) ⭐")

    # Add actions for each prompt
    for i in range(1, 4): # Buttons 1, 2, 3
        action = QAction(f"Generate with Prompt {i} (🤖{i})", browser)
        # Pass browser, editor instance, and button number to the handler
        qconnect(action.triggered, lambda checked=False, b=browser, e=editor, num=i: logic.on_autocards_browser_menu_action(b, e, num))
        submenu.addAction(action)

    # --- Add Keyboard Shortcuts to Browser Window (Run Once Per Browser Instance) ---
    # Use a flag to prevent adding actions multiple times for the same browser window
    if not getattr(browser, "_autocards_shortcuts_added", False):
        # Create actions specifically for shortcuts
        shortcut_actions = []
        for i in range(1, 4):
            action = QAction(browser) # Parent is the browser window
            action.setShortcut(QKeySequence(f"Ctrl+{i}"))
            # Important: Connect to a lambda that captures the CURRENT editor state when triggered
            # We need to ensure browser.editor is valid when the shortcut is pressed.
            # The logic handler already gets the editor instance.
            qconnect(action.triggered, lambda checked=False, b=browser, num=i: trigger_browser_shortcut_action(b, num))
            shortcut_actions.append(action)
            browser.addAction(action) # Add action to the browser window widget

        setattr(browser, "_autocards_shortcuts_added", True) # Set flag

# --- Helper function to trigger browser action from shortcut ---
# This ensures we fetch the *current* editor state when the shortcut is used
def trigger_browser_shortcut_action(browser: Browser, button_number: int):
    editor = getattr(browser, "editor", None)
    if editor and editor.currentField is not None:
        # Call the existing logic handler, passing the browser and editor
        logic.on_autocards_browser_menu_action(browser, editor, button_number)
    else:
        # Optional: Provide feedback if the editor or field isn't focused
        # showInfo("Please click into a field in the browser editor first.")
        pass # Silently ignore if editor/field not ready

# Initialize addon
def init_addon():
    config.load_config() # Load configuration on profile open
    add_menu_items()
    editor_did_init_buttons.append(add_editor_buttons)
    browser_will_show_context_menu.append(add_browser_context_menu_items) # Use correct hook

# Connect initialization to profile open hook
profile_did_open.append(init_addon)