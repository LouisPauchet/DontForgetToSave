import keyboard
import time
import threading
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import json
import random

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Global variable to track the last time "Ctrl + S" was pressed
last_save_time = time.time()
debug = True  # Set this to False to disable debug prints

def debug_print(message):
    if debug:
        print(message)

def check_save_reminder():
    while True:
        if is_word_active():
            current_time = time.time()
            reminder_delay = random.uniform(config['min_delay'], config['max_delay'])
            if current_time - last_save_time > reminder_delay:
                debug_print(f"{reminder_delay / 60:.2f} minutes have passed since the last save.")
                show_save_reminder(reminder_delay / 60)
        else:
            debug_print("Microsoft Word is not the active window.")
        time.sleep(10)  # Check every 10 seconds

def is_word_active():
    try:
        active_window = gw.getActiveWindowTitle()
        if active_window:
            debug_print(f"Active window title: {active_window}")
            if "word" in active_window.lower():
                return True
    except Exception as e:
        debug_print(f"Error checking active window: {e}")
    return False

def show_save_reminder(minutes):
    debug_print("Displaying save reminder popup.")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Ensure the window is on top

    # Function to handle the save action
    def on_ok():
        debug_print("User chose to save the document.")
        root.destroy()
        simulate_ctrl_s()

    # Get the message in the configured language
    message_template = config['messages'].get(config['language'], config['messages']['en'])
    message = message_template.format(minutes=int(minutes))
    
    # Create and display the message box
    response = tk.messagebox.askokcancel("Save Reminder", message, parent=root)

    if response:
        on_ok()
    else:
        debug_print("User chose not to save the document.")
        root.destroy()

def simulate_ctrl_s():
    debug_print("Simulating Ctrl+S keypress.")
    keyboard.press_and_release('ctrl+s')
    on_ctrl_s()

def on_ctrl_s():
    global last_save_time
    last_save_time = time.time()
    debug_print("Ctrl+S was pressed. Updating last save time.")

def main():
    debug_print("Starting the save reminder script.")
    keyboard.add_hotkey('ctrl+s', on_ctrl_s)
    reminder_thread = threading.Thread(target=check_save_reminder)
    reminder_thread.daemon = True
    reminder_thread.start()
    keyboard.wait('esc')  # Keep the script running until 'esc' is pressed
    debug_print("Script has been terminated.")

if __name__ == "__main__":
    main()
