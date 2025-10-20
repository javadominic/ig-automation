# Instagram Messenger Automation

⚠️ **WARNING**: This script is for educational purposes only. Using automation violates Instagram's Terms of Service and may result in account suspension or ban.

## Features

- ✅ Interactive CLI prompts for credentials, message, and timing
- ✅ Automatically fetches your Instagram following list
- ✅ Schedule messages to run immediately or at a specific time
- ✅ 2FA support with manual code entry
- ✅ Random delays to mimic human behavior
- ✅ Detailed logging of all actions
- ✅ Success/failure tracking
- ✅ Rate limit awareness and safety confirmations
- ✅ Message limiting option to avoid bans

## Setup Instructions

### 1. Install Dependencies

```bash
cd "ig automation"
pip install -r requirements.txt
```

### 2. Install ChromeDriver

**Option A: Using Homebrew (macOS)**
```bash
brew install chromedriver
```

**Option B: Manual Installation**
- Download ChromeDriver matching your Chrome version from: https://chromedriver.chromium.org/
- Add it to your PATH

## Usage

### Run the Script

Simply run the script and follow the interactive prompts:

```bash
python instagram_messenger.py
```

### Interactive Prompts

The script will guide you through a series of prompts:

1. **Enter Instagram Username**
   - Your Instagram account username

2. **Enter Instagram Password**
   - Password (hidden for security)

3. **Enter Your Message**
   - Type your message
   - Press Enter twice when finished

4. **Choose Timing**
   - Option 1: Run immediately
   - Option 2: Schedule for specific time (24-hour format, e.g., 14:30)

5. **Confirmation**
   - Review all settings
   - Confirm to proceed

6. **Login & 2FA**
   - Browser opens automatically
   - If 2FA is enabled, enter the code when prompted

7. **Following List**
   - Script automatically collects all users you follow
   - Shows total count

8. **Final Confirmation**
   - Choose to send to all users or limit the number
   - Campaign starts after confirmation

### Example Session

```
INSTAGRAM MESSENGER BOT
============================================================
⚠️  WARNING: Using automation violates Instagram's Terms of Service
⚠️  Your account may be banned or suspended
⚠️  Use at your own risk!
============================================================

Enter your Instagram username: myusername
Enter your Instagram password: 
------------------------------------------------------------
Enter your message (press Enter twice when done):
------------------------------------------------------------
Hey! Hope you're doing well! 😊

------------------------------------------------------------
SCHEDULING OPTIONS
------------------------------------------------------------
1. Run immediately
2. Schedule for specific time (24-hour format)
------------------------------------------------------------
Choose option (1 or 2): 1
✓ Will run immediately

============================================================
Username: myusername
Message preview: Hey! Hope you're doing well! 😊
Schedule: Run immediately
============================================================

Proceed with these settings? (yes/no): yes
```

### Scheduling Feature

When you choose option 2 for scheduling:

```
Choose option (1 or 2): 2
Enter time to run (HH:MM, e.g., 14:30): 15:00
✓ Scheduled for 15:00 (daily)
```

The script will:
- Wait until the specified time
- Automatically start the campaign
- Run daily at the same time
- Keep running until you press Ctrl+C

## Important Notes

### Rate Limits
- Instagram has strict rate limits
- **Recommended: Max 20-50 messages per day**
- The script includes random delays between messages (15-25 seconds)
- Start with a small test (5-10 messages) before sending to all
- Increase delays if you experience issues

### 2FA Handling
- If you have 2FA enabled, the script will pause and ask for your code
- Enter the 6-digit code in the terminal when prompted
- The script will then continue automatically

### Safety Features
- Multiple confirmation prompts before sending messages
- Option to limit the number of recipients
- All actions logged to `instagram_messenger.log`
- Random delays to avoid detection
- Secure password input (not visible when typing)

### Best Practices

1. **Start Small:** Test with 5-10 messages first
2. **Respect Limits:** Don't exceed 20-50 messages per day
3. **Use Natural Messages:** Avoid spam-like content
4. **Monitor Logs:** Check `instagram_messenger.log` for any issues
5. **Take Breaks:** Space out campaigns over multiple days
6. **Be Responsive:** If you get a warning from Instagram, STOP immediately

### Troubleshooting

**"ChromeDriver not found"**
- Install ChromeDriver (see setup instructions)
- Ensure it's in your PATH
- Try: `brew install chromedriver` on macOS

**"Login failed"**
- Check your credentials
- Make sure Instagram isn't blocking automated logins
- Try logging in manually first to verify credentials
- Check if Instagram requires you to verify your identity

**"Could not find 'Message' button"**
- The profile might be private
- The account might have messaging disabled
- You might not be following them

**"Failed to get following list"**
- Make sure you're logged in successfully
- Instagram UI might have changed (selectors may need updating)
- Try running the script again

**Account Issues**
- If Instagram detects automation, they may:
  - Show CAPTCHA challenges
  - Temporarily restrict your account
  - Require password reset
  - Permanently ban your account

## Logs

All activity is logged to `instagram_messenger.log` with timestamps and status for each message.

Example log output:
```
2025-10-20 14:30:00 - INFO - Instagram Messenger Bot Started
2025-10-20 14:30:05 - INFO - ✓ Login successful!
2025-10-20 14:30:10 - INFO - Found 150 users in your following list
2025-10-20 14:30:15 - INFO - [1/10] Processing: @username1
2025-10-20 14:30:20 - INFO - ✓ Message sent successfully to @username1
```

## Files in Project

- `instagram_messenger.py` - Main automation script
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `instagram_messenger.log` - Auto-generated log file

## Technical Details

### How It Works

1. **Authentication:** Uses Selenium WebDriver to automate Chrome browser
2. **Following List:** Scrolls through your following dialog to collect all usernames
3. **Messaging:** Navigates to Direct Messages and sends personalized messages
4. **Delays:** Random delays between actions to appear human-like
5. **Logging:** Comprehensive logging of all actions and errors

### Dependencies

- `selenium` - Web automation
- `apscheduler` - Task scheduling
- `webdriver-manager` - ChromeDriver management

## Legal Disclaimer

This script is provided for educational purposes only. The user assumes all responsibility and risk associated with the use of this script. Using automation tools violates Instagram's Terms of Service and may result in account penalties including permanent ban.

**Use at your own risk.**

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the log file for error details
3. Ensure all dependencies are installed correctly
4. Make sure ChromeDriver matches your Chrome version
5. Verify your Instagram credentials are correct

## License

This project is for educational purposes only. No warranty or support is provided.
