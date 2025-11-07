# Playwright Cricket Scorecard Scraper

A Python automation script that uses Playwright to search for cricket match scorecards on Bing and automatically navigate to the scorecard page, capturing screenshots and HTML snapshots.

## 📋 Overview

This script automates the following workflow:
1. Opens Bing search engine in a browser
2. Searches for cricket match scorecards (e.g., "IND vs SA final scorecard")
3. Intelligently selects the most relevant result (prioritizing cricbuzz.com and espncricinfo.com)
4. Navigates to the scorecard page
5. Captures a full-page screenshot
6. Saves the HTML content for offline inspection

## 🎯 Features

- **Bing Search Integration**: More reliable than Google for headless automation
- **Smart Result Selection**: Prioritizes cricket-specific websites (Cricbuzz, ESPNcricinfo)
- **Consent Handling**: Automatically dismisses cookie consent popups
- **Headless/Headful Modes**: Run with visible browser or in background
- **Screenshot Capture**: Full-page screenshots with timestamps
- **HTML Snapshot**: Save complete page HTML for detailed analysis
- **Slow-Mo Mode**: Watch the automation steps in real-time (50ms delay)

## 📁 Project Structure

```
playwright_assignment/
│
├── src/
│   └── scorecard.py       # Main automation script
│
├── .venv/                 # Virtual environment
│
├── requirements.txt       # Python dependencies
│
├── README.md             # This file
│
└── scorecard_*.png       # Generated screenshots (timestamped)
└── scorecard_*.html      # Generated HTML snapshots (timestamped)
```

## 🚀 Setup Instructions

### Prerequisites

- macOS (or any OS supporting Python 3.11+)
- Python 3.11 or higher
- Internet connection

### Step 1: Navigate to Project Directory

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/playwright_assignment
```

### Step 2: Create Virtual Environment

```bash
# Create a new virtual environment
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows (if needed):
# .venv\Scripts\activate
```

You should see `(.venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- playwright==1.55.0
- beautifulsoup4==4.14.2
- lxml==6.0.2
- And other dependencies

### Step 5: Install Playwright Browsers

```bash
# Install browser binaries (Chromium, Firefox, WebKit)
playwright install
```

This downloads the necessary browser engines (~300MB total).

### Step 6: Configure VS Code (Optional)

Create or verify `.vscode/settings.json` exists with:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

## 📖 Usage

### Basic Execution (Headful Mode - Recommended)

Run with visible browser to watch the automation:

```bash
python src/scorecard.py
```

This will:
- Open a Chromium browser window
- Navigate to Bing
- Search for the cricket scorecard
- Show you each step with a 50ms delay (slow_mo)
- Save outputs to current directory

### Headless Mode

Run in background without visible browser:

```bash
python src/scorecard.py --headless
```

**Note:** Headful mode is recommended for debugging and first-time runs.

### Using Virtual Environment Path Directly

To ensure you're using the correct Python interpreter:

```bash
# Headful
/Users/kanda/Learning/GenAI/gen-ai-learning/playwright_assignment/.venv/bin/python src/scorecard.py

# Headless
/Users/kanda/Learning/GenAI/gen-ai-learning/playwright_assignment/.venv/bin/python src/scorecard.py --headless
```

## 🔧 Customization

### Changing the Search Query

Edit the `QUERY` variable in `src/scorecard.py`:

```python
QUERY = "sa vs ind final scorecard"  # Change to your desired search
```

Examples:
- `"ind vs aus test scorecard"`
- `"england vs new zealand odi scorecard"`
- `"ipl 2024 final scorecard"`

### Changing the Browser

Edit the browser launch line in `src/scorecard.py`:

```python
# Use Firefox
browser = p.firefox.launch(headless=headless, slow_mo=50)

# Use WebKit
browser = p.webkit.launch(headless=headless, slow_mo=50)

# Use Chromium (default)
browser = p.chromium.launch(headless=headless, slow_mo=50)
```

### Adjusting Speed

Modify the `slow_mo` parameter:

```python
# Faster (25ms delay)
browser = p.chromium.launch(headless=headless, slow_mo=25)

# Slower (100ms delay - easier to watch)
browser = p.chromium.launch(headless=headless, slow_mo=100)

# No delay (fastest)
browser = p.chromium.launch(headless=headless, slow_mo=0)
```

## 📤 Output Files

After each successful run, the script generates:

### Screenshots
- **Filename Pattern**: `scorecard_<timestamp>.png`
- **Example**: `scorecard_1762492903.png`
- **Content**: Full-page screenshot of the scorecard page

### HTML Snapshots
- **Filename Pattern**: `scorecard_<timestamp>.html`
- **Example**: `scorecard_1762492903.html`
- **Content**: Complete HTML of the scorecard page
- **Usage**: Open in browser for offline viewing or parse for data extraction

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'playwright'`

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: `Executable doesn't exist at /path/to/chromium`

**Solution:** Install browser binaries:
```bash
playwright install
```

### Issue: Timeout on search box selector

**Solution:** 
- Run in headful mode to see what's happening
- Bing might be showing a different layout - check the browser window
- Ensure you have a stable internet connection

### Issue: No search results found

**Solution:**
- Modify the `QUERY` variable to be more specific
- Check your internet connection
- Try running in headful mode to see the actual search results

### Issue: Script clicking wrong result

**Solution:** The script uses heuristics to select results. You can modify the selection logic in the script:

```python
# Prioritize only Cricbuzz
if "cricbuzz.com" in low_href and "scorecard" in low_href:
    chosen_index = i
    chosen_href = href
    chosen_title = title
    break
```

### Issue: "Import 'bs4' could not be resolved" in VS Code

**Solution:**
1. Ensure VS Code is using the correct Python interpreter:
   - Press `Cmd+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose the one pointing to `.venv/bin/python`
2. Reload VS Code window: `Cmd+Shift+P` → "Developer: Reload Window"

## 🔄 Workflow Example

Complete workflow from start to finish:

```bash
# 1. Navigate to project
cd /Users/kanda/Learning/GenAI/gen-ai-learning/playwright_assignment

# 2. Activate virtual environment
source .venv/bin/activate

# 3. (First time only) Install dependencies
pip install -r requirements.txt
playwright install

# 4. Run the script
python src/scorecard.py

# 5. Check outputs
ls -lh scorecard_*.png scorecard_*.html

# 6. Open the screenshot
open scorecard_*.png

# 7. Open HTML in browser
open scorecard_*.html
```

## 📊 Technical Details

### Search Strategy

The script uses the following priority order when selecting search results:

1. **Highest Priority**: Links containing both "scorecard" and known cricket sites (cricbuzz.com, espncricinfo.com)
2. **Medium Priority**: Links containing "cricket" keyword
3. **Fallback**: First search result

### Browser Configuration

- **Viewport**: 1280x768 pixels
- **User Agent**: Chrome 117 on Windows 10
- **Locale**: en-US
- **Downloads**: Enabled
- **Slow Motion**: 50ms delay between actions

### Consent Handling

The script attempts to dismiss cookie consent popups by looking for:
- `#bnp_btn_accept` (Bing consent button ID)
- Buttons with text: "I agree", "Accept"

## 🎓 Learning Resources

This project demonstrates:
- Web automation with Playwright
- Search engine interaction
- Element selection strategies
- Screenshot and HTML capture
- Error handling and timeouts
- Browser context configuration

## 📝 Requirements

Key dependencies (see `requirements.txt` for full list):

```txt
playwright==1.55.0
beautifulsoup4==4.14.2
lxml==6.0.2
pyee==13.0.0
greenlet==3.2.4
```

## ⚖️ Disclaimer

This script is for educational purposes and personal use only:
- Respect website Terms of Service
- Be mindful of rate limits
- Don't use for commercial scraping without permission
- Use responsibly and ethically

## 🤝 Contributing

To improve this script:
1. Test with different search queries
2. Add error recovery mechanisms
3. Implement data extraction from scorecards
4. Add support for direct URLs (bypass search)
5. Create unit tests

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all prerequisites are met
3. Ensure virtual environment is activated
4. Try running in headful mode to observe behavior

---

**Happy Automating! 🏏**
