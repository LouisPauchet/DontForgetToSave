# Save Reminder Application

This application reminds you to save your work at random intervals while specific applications are active. It provides a popup reminder and can simulate a Ctrl+S keypress to automatically save your work. Additionally, it logs the number of user-initiated and automatic saves to a log file.

## Features

- **Active Window Monitoring**: Monitors specified applications and only reminds you to save if they are active.
- **Random Save Reminders**: Displays a save reminder popup at random intervals within a specified range.
- **Automatic Save Simulation**: Can simulate a Ctrl+S keypress to save your work automatically.
- **Tray Icon**: Adds an icon to the system tray with an option to exit the application.
- **Logging**: Logs the number of manual and automatic saves to a log file upon exit.

## Prerequisites

- Python 3.x
- Required Python packages: `time`, `threading`, `tkinter`, `pygetwindow`, `json`, `random`, `pystray`, `PIL`, `keyboard`, `os`, `datetime`

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/save-reminder.git
    cd save-reminder
    ```

2. **Install dependencies**:
    ```bash
    pip install pygetwindow pystray Pillow keyboard
    ```

3. **Configuration**:
    - **config.json**: Main configuration file.
    - **Language Configuration**: Ensure the appropriate language JSON file is available in the `locals` directory.

## Configuration

### config.json

This file contains the main configuration for the application. Below is an example configuration:

```json
{
    "language": "en",
    "min_delay": 300,
    "max_delay": 1800,
    "applications": ["Notepad", "Word", "Excel"]
}
```

- `language`: The language to be used for messages.
- `min_delay`: Minimum delay (in seconds) between save reminders.
- `max_delay`: Maximum delay (in seconds) between save reminders.
- `applications`: List of application names to monitor for activity.

### Language Configuration

Place the appropriate language JSON file in the `locals` directory. Example: `./locals/en.json`.

```json
{
    "save_reminder_title": "Save Reminder",
    "save_reminder_message": "It has been {minutes} minutes since your last save. Do you want to save now?",
    "exit_title": "Save Reminder Stats",
    "exit_message": "You have manually saved {user_saves} times and automatically saved {auto_saves} times."
}
```

## Usage

1. **Run the application**:
    ```bash
    python save_reminder.py
    ```

2. The application will start monitoring the specified applications and display save reminders at random intervals.

3. A tray icon will be added to the system tray. You can exit the application by right-clicking the tray icon and selecting "Exit".

## Logging

Upon exiting the application, the number of manual and automatic saves will be logged to `save.log` with a timestamp and username.

## Debugging

Set the `debug` variable to `True` to enable debug prints, which will output helpful information to the console.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The application uses several Python libraries such as `pygetwindow`, `pystray`, `Pillow`, and `keyboard`.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.
