# WhatsApp Auto-Send Message Script

A Python automation script that sends a predefined message to WhatsApp (Web/Desktop) with a single mouse click.

## 📋 Prerequisites

- macOS (tested on macOS)
- Python 3.7+
- WhatsApp Web or WhatsApp Desktop app
- Accessibility permissions granted

## 🚀 Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Navigate to the project directory
cd pyautogui_assignment

# Create virtual environment (if not already created)
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install required packages
pip install pyautogui pynput pillow pyobjc-core pyobjc-framework-Quartz
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Grant Accessibility Permissions (IMPORTANT!)

This script requires accessibility permissions to monitor mouse clicks and keyboard input.

#### Steps:
1. Open **System Settings** (or System Preferences)
2. Go to **Privacy & Security** → **Accessibility**
3. Click the **lock icon** (bottom left) and authenticate
4. Click the **"+"** button
5. Add your terminal application:
   - **Terminal.app** (if using default Terminal)
   - **iTerm2** (if using iTerm)
   - **Visual Studio Code** (if running from VS Code terminal)
6. **Enable the checkbox** next to the added application
7. **Restart your terminal**

**Quick access command:**
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

## 📖 How to Use

### Step 1: Prepare WhatsApp
1. Open **WhatsApp Web** (web.whatsapp.com) in your browser **OR** open **WhatsApp Desktop** app
2. Navigate to the chat where you want to send messages
3. **CRITICAL:** Click inside the text input box at the bottom of the chat
4. **Make sure the cursor is blinking in the text box**

### Step 2: Run the Script
```bash
python src/send_message.py
```

You should see:
```
== WhatsApp click-to-send script ==
1) Make sure WhatsApp (Web/Desktop) chat is open and the text input box is focused.
2) Each left-click will send the message:
   `Hi Eagle Team`, This is Kanda!. I'm pleased to confirm that the one-week task has been successfully completed, using PyAutoGUI.
3) Press ESC to stop. Move the cursor to the top-left corner to trigger pyautogui fail-safe.
```

### Step 3: Send Messages
- **Left-click anywhere** on the screen to send the message
- The message will be typed and sent automatically
- **Important:** Keep the WhatsApp text input box focused

### Step 4: Stop the Script
- Press **ESC** key to stop the script gracefully
- **OR** move your cursor to the **top-left corner** of the screen (PyAutoGUI fail-safe)

## ⚠️ Important Warnings

### ⚠️ DO NOT CLICK OUTSIDE THE TEXT BOX!

**CRITICAL:** Once the script is running, do NOT click outside the WhatsApp text input box. Here's why:

❌ **What happens if you click elsewhere:**
- If you click on a different app/window, the message will be typed there instead
- If you click on WhatsApp's contact list, it might open a different chat
- If you click on file/media buttons, it might trigger unwanted actions
- The message could be sent to the wrong chat or person

✅ **Best Practice:**
1. Open WhatsApp and select the target chat
2. Click inside the text input box
3. Run the script
4. Keep your cursor away from clickable elements
5. Only click in safe, empty areas of the screen
6. The text box will remain focused as long as you don't click elsewhere

### Safety Features

1. **Debounce Protection:** The script ignores clicks that happen within 0.25 seconds of each other (prevents accidental double-sends)

2. **Fail-Safe:** Move your cursor to the top-left corner of the screen to immediately stop all PyAutoGUI actions

3. **ESC Key:** Press ESC to gracefully exit the script

## 🛠️ Customization

You can customize the script by editing `src/send_message.py`:

```python
# Change the message
MESSAGE = """Your custom message here"""

# Change which mouse button triggers sending
SEND_ON = 'left'   # or 'right' for right-click

# Adjust debounce timing (in seconds)
DEBOUNCE_SECONDS = 0.25
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pyautogui'"
**Solution:** Make sure the virtual environment is activated and packages are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "This process is not trusted! Input event monitoring will not be possible..."
**Solution:** Grant accessibility permissions (see Step 3 in Setup Instructions)

### Issue: Message sent to wrong place
**Solution:** 
- Make sure WhatsApp text input box is focused before running the script
- Don't click on other windows/apps while the script is running
- Stop the script (ESC), refocus the text box, and restart

### Issue: PyAutoGUI fail-safe triggered
**Solution:** This is a safety feature. If you accidentally moved your cursor to the top-left corner, simply restart the script.

## 📁 Project Structure

```
pyautogui_assignment/
│
├── src/
│   └── send_message.py    # Main automation script
│
├── .venv/                 # Virtual environment (created during setup)
│
├── requirements.txt       # Python dependencies
│
└── README.md             # This file
```

## 📝 Requirements

```txt
pyautogui
pynput
pillow
pyobjc-core
pyobjc-framework-Quartz
```

## ⚖️ Disclaimer

This script is for educational purposes and personal use only. Use responsibly and:
- Get consent before sending automated messages
- Follow WhatsApp's Terms of Service
- Don't use for spam or harassment
- Test in a safe environment first

## 🤝 Support

If you encounter issues:
1. Check that all prerequisites are met
2. Verify accessibility permissions are granted
3. Ensure WhatsApp text box is focused
4. Review the Troubleshooting section

---

**Happy Automating! 🚀**
