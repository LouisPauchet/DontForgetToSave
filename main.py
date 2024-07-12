import time
import threading
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import json
import random
import pystray
from PIL import Image, ImageDraw
import keyboard
from threading import Event
import os
from datetime import datetime

# Load main configuration
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Load language configuration
lang_file_path = os.path.join('./locals', f"{config['language']}.json")
with open(lang_file_path, 'r', encoding='utf-8') as f:
    lang_config = json.load(f)

# Global variables
last_save_time = time.time()
debug = True  # Set this to False to disable debug prints
terminate_event = Event()
numberSave = 0
autoSave = 0

def debug_print(message):
    if debug:
        print(message)

def show_exit_stats():
    global numberSave
    global autoSave

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Ensure the window is on top

    messagebox.showinfo(
        lang_config["exit_title"], 
        lang_config["exit_message"].format(user_saves=numberSave - autoSave, auto_saves=autoSave),
        parent=root
    )
    root.destroy()

    # Log the saves to save.log
    username = os.getlogin()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('save.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{current_time} - {username} - User saves: {numberSave - autoSave}, Auto saves: {autoSave}\n")

def check_save_reminder():
    while not terminate_event.is_set():
        if is_app_active():
            current_time = time.time()
            reminder_delay = random.uniform(config['min_delay'], config['max_delay'])
            if current_time - last_save_time > reminder_delay:
                debug_print(f"{reminder_delay / 60:.2f} minutes have passed since the last save.")
                show_save_reminder(reminder_delay / 60)
        else:
            debug_print("None of the specified applications is the active window.")
        time.sleep(10)  # Check every 10 seconds

def is_app_active():
    try:
        active_window = gw.getActiveWindowTitle()
        if active_window:
            debug_print(f"Active window title: {active_window}")
            for app in config['applications']:
                if app.lower() in active_window.lower():
                    return True
    except Exception as e:
        debug_print(f"Error checking active window: {e}")
    return False

def show_save_reminder(minutes):
    global autoSave
    debug_print("Displaying save reminder popup.")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Ensure the window is on top

    def on_ok():
        global autoSave
        debug_print("User chose to save the document.")
        root.destroy()
        simulate_ctrl_s()
        autoSave += 1

    message = lang_config["save_reminder_message"].format(minutes=int(minutes))
    response = messagebox.askokcancel(lang_config["save_reminder_title"], message, parent=root)

    if response:
        on_ok()
    else:
        debug_print("User chose not to save the document.")
        root.destroy()

def simulate_ctrl_s():
    if is_app_active():
        debug_print("Simulating Ctrl+S keypress.")
        keyboard.press_and_release('ctrl+s')
        on_ctrl_s()

def on_ctrl_s():
    if is_app_active():
        global last_save_time
        global numberSave
        last_save_time = time.time()
        numberSave += 1
        debug_print("Ctrl+S was pressed. Updating last save time.")

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10), fill="black")
    return image

def on_exit(icon, item):
    debug_print("Exiting script.")
    show_exit_stats()
    terminate_event.set()
    icon.stop()

def setup_tray_icon():
    icon_image = create_image()
    icon = pystray.Icon("Save Reminder", icon_image, "Save Reminder", menu=pystray.Menu(
        pystray.MenuItem("Exit", on_exit)
    ))
    icon.run()

def main():
    debug_print("Starting the save reminder script.")
    keyboard.add_hotkey('ctrl+s', on_ctrl_s)
    reminder_thread = threading.Thread(target=check_save_reminder)
    reminder_thread.daemon = True
    reminder_thread.start()
    tray_thread = threading.Thread(target=setup_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()
    while not terminate_event.is_set():
        time.sleep(1)
    debug_print("Script has been terminated.")

if __name__ == "__main__":
    main()
