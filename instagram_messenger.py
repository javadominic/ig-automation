#!/usr/bin/env python3
"""
Instagram Direct Message Automation Script

⚠️ WARNING: This script is for educational purposes only.
- Using automation violates Instagram's Terms of Service
- Your account may be banned or suspended
- Instagram has strict rate limits (recommended: max 20-50 messages per day)
- Use at your own risk

SETUP:
1. Install requirements: pip install -r requirements.txt
2. Install ChromeDriver matching your Chrome version
3. Run the script: python instagram_messenger.py
4. Follow the interactive prompts
"""

import os
import sys
import csv
import time
import random
import logging
import getpass
from datetime import datetime
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from apscheduler.schedulers.blocking import BlockingScheduler

# Configuration
LOG_FILE = "instagram_messenger.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class InstagramMessenger:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Initialize Chrome WebDriver with options"""
        logger.info("Setting up Chrome WebDriver...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            logger.error("Make sure ChromeDriver is installed and in PATH")
            raise

    def random_delay(self, min_seconds: float = 2, max_seconds: float = 5):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def login(self):
        """Login to Instagram"""
        try:
            logger.info("Navigating to Instagram login page...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.random_delay(3, 5)

            # Handle cookie consent if present
            try:
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]")
                cookie_button.click()
                self.random_delay(1, 2)
            except NoSuchElementException:
                pass

            # Wait for and fill username
            logger.info("Entering credentials...")
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            self.random_delay(1, 2)

            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            self.random_delay(1, 2)

            # Click login button
            password_input.send_keys(Keys.RETURN)
            logger.info("Login submitted, waiting for response...")
            self.random_delay(5, 7)

            # Check for 2FA
            if self.check_2fa():
                self.handle_2fa()

            # Handle "Save Your Login Info" prompt
            self.handle_save_login_prompt()

            # Handle "Turn on Notifications" prompt
            self.handle_notifications_prompt()

            logger.info("✓ Login successful!")
            return True

        except Exception as e:
            logger.error(f"✗ Login failed: {e}")
            return False

    def check_2fa(self) -> bool:
        """Check if 2FA prompt is present"""
        try:
            self.driver.find_element(By.NAME, "verificationCode")
            logger.info("2FA prompt detected")
            return True
        except NoSuchElementException:
            return False

    def handle_2fa(self):
        """Handle 2FA verification"""
        logger.info("⚠️  Two-Factor Authentication required")
        print("\n" + "="*60)
        print("TWO-FACTOR AUTHENTICATION REQUIRED")
        print("="*60)
        print("Please check your authentication app or SMS for the code.")
        code = input("Enter the 6-digit 2FA code: ").strip()
        print("="*60 + "\n")

        try:
            code_input = self.driver.find_element(By.NAME, "verificationCode")
            code_input.send_keys(code)
            self.random_delay(1, 2)
            code_input.send_keys(Keys.RETURN)
            logger.info("2FA code submitted, waiting for verification...")
            self.random_delay(5, 7)
        except Exception as e:
            logger.error(f"Failed to submit 2FA code: {e}")
            raise

    def handle_save_login_prompt(self):
        """Handle 'Save Your Login Info' prompt"""
        try:
            not_now_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now') or contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            logger.info("Dismissed 'Save Login Info' prompt")
            self.random_delay(2, 3)
        except TimeoutException:
            logger.info("No 'Save Login Info' prompt found")

    def handle_notifications_prompt(self):
        """Handle 'Turn on Notifications' prompt"""
        try:
            not_now_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            not_now_button.click()
            logger.info("Dismissed notifications prompt")
            self.random_delay(2, 3)
        except TimeoutException:
            logger.info("No notifications prompt found")

    def get_following_list(self) -> List[str]:
        """Navigate to profile and scrape following list"""
        following_usernames = []

        try:
            logger.info("Navigating to your profile...")
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            self.random_delay(3, 5)

            logger.info("Opening following list...")
            following_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{self.username}/following')]"))
            )
            following_link.click()
            self.random_delay(3, 5)

            logger.info("Loading following list...")
            following_dialog = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )

            logger.info("Scrolling to load all users (this may take a while)...")
            last_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 50

            while scroll_attempts < max_scroll_attempts:
                scrollable_div = self.driver.find_element(By.XPATH, "//div[@role='dialog']//div[contains(@class, 'x')]")
                user_links = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//a[contains(@href, '/')]")
                current_count = len(user_links)

                logger.info(f"Found {current_count} users so far...")

                if current_count == last_count:
                    scroll_attempts += 1
                    if scroll_attempts >= 3:
                        break
                else:
                    scroll_attempts = 0

                last_count = current_count
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                self.random_delay(2, 3)

            logger.info("Extracting usernames...")
            user_links = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//a[contains(@href, '/') and not(contains(@href, '/explore/')) and not(contains(@href, '/reels/')) and not(contains(@href, '/p/'))]")

            seen_usernames = set()
            for link in user_links:
                href = link.get_attribute('href')
                if href:
                    username = href.replace('https://www.instagram.com/', '').strip('/')
                    if username and '/' not in username and username != self.username:
                        if username not in seen_usernames:
                            following_usernames.append(username)
                            seen_usernames.add(username)

            logger.info(f"✓ Successfully extracted {len(following_usernames)} following users")

            try:
                close_button = self.driver.find_element(By.XPATH, "//div[@role='dialog']//button[contains(@aria-label, 'Close')]")
                close_button.click()
                self.random_delay(1, 2)
            except:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                self.random_delay(1, 2)

            return following_usernames

        except Exception as e:
            logger.error(f"Failed to get following list: {e}")
            return []

    def send_message_to_username(self, username: str, message: str) -> bool:
        """Send a message to a specific username via Direct Messages"""
        try:
            logger.info(f"Sending message to @{username}...")

            self.driver.get("https://www.instagram.com/direct/inbox/")
            self.random_delay(3, 4)

            try:
                new_message_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Send message') or contains(text(), 'Send Message')]"))
                )
                new_message_button.click()
                self.random_delay(2, 3)
            except:
                try:
                    new_message_button = self.driver.find_element(By.XPATH, "//svg[@aria-label='New message']/ancestor::div[@role='button']")
                    new_message_button.click()
                    self.random_delay(2, 3)
                except:
                    logger.error("Could not find 'New Message' button")
                    return False

            try:
                to_field = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search...' or @name='queryBox']"))
                )
                to_field.click()
                to_field.send_keys(username)
                self.random_delay(2, 3)

                user_option = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@role, 'button') and contains(., '{username}')]"))
                )
                user_option.click()
                self.random_delay(1, 2)

                chat_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat') or contains(text(), 'Next')]"))
                )
                chat_button.click()
                self.random_delay(2, 3)

            except Exception as e:
                logger.error(f"Failed to select user {username}: {e}")
                return False

            try:
                message_box = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Message...' or @placeholder='Message']"))
                )

                logger.info("Typing message...")
                for char in message:
                    message_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))

                self.random_delay(1, 2)

                try:
                    send_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
                    send_button.click()
                except:
                    message_box.send_keys(Keys.RETURN)

                logger.info(f"✓ Message sent successfully to @{username}")
                self.random_delay(2, 3)
                return True

            except TimeoutException:
                logger.error("Could not find message input box")
                return False

        except Exception as e:
            logger.error(f"✗ Failed to send message to @{username}: {e}")
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()


def get_credentials_from_cli() -> Tuple[str, str, str, str]:
    """Prompt user for credentials, message, and timing via CLI"""
    print("\n" + "="*60)
    print("INSTAGRAM MESSENGER BOT")
    print("="*60)
    print("⚠️  WARNING: Using automation violates Instagram's Terms of Service")
    print("⚠️  Your account may be banned or suspended")
    print("⚠️  Use at your own risk!")
    print("="*60 + "\n")

    username = input("Enter your Instagram username: ").strip()
    password = getpass.getpass("Enter your Instagram password: ").strip()

    print("\n" + "-"*60)
    print("Enter your message (press Enter twice when done):")
    print("-"*60)

    message_lines = []
    empty_line_count = 0

    while empty_line_count < 1:
        line = input()
        if line:
            message_lines.append(line)
            empty_line_count = 0
        else:
            empty_line_count += 1

    message = "\n".join(message_lines).strip()

    if not message:
        print("\n⚠️  No message entered. Using default message.")
        message = "Hello! 👋"

    print("\n" + "-"*60)
    print("SCHEDULING OPTIONS")
    print("-"*60)
    print("1. Run immediately")
    print("2. Schedule for specific time (24-hour format)")
    print("-"*60)

    schedule_choice = input("Choose option (1 or 2): ").strip()

    schedule_time = None
    if schedule_choice == "2":
        while True:
            time_input = input("Enter time to run (HH:MM, e.g., 14:30): ").strip()
            try:
                hour, minute = map(int, time_input.split(':'))
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    schedule_time = time_input
                    print(f"✓ Scheduled for {schedule_time} (daily)")
                    break
                else:
                    print("❌ Invalid time. Hour must be 0-23, minute must be 0-59.")
            except:
                print("❌ Invalid format. Please use HH:MM format (e.g., 14:30)")
    else:
        schedule_time = "now"
        print("✓ Will run immediately")

    print("\n" + "="*60)
    print(f"Username: {username}")
    print(f"Message preview: {message[:50]}{'...' if len(message) > 50 else ''}")
    print(f"Schedule: {schedule_time if schedule_time != 'now' else 'Run immediately'}")
    print("="*60 + "\n")

    confirm = input("Proceed with these settings? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Aborted by user.")
        sys.exit(0)

    return username, password, message, schedule_time


def run_messaging_campaign_with_params(username, password, message):
    """Run messaging campaign with pre-set parameters for scheduling"""
    logger.info("="*60)
    logger.info("Instagram Messenger Bot Started (Scheduled)")
    logger.info("="*60)

    messenger = InstagramMessenger(username, password)

    try:
        messenger.setup_driver()
        if not messenger.login():
            logger.error("Login failed. Exiting.")
            return

        logger.info("\n" + "="*60)
        logger.info("Fetching your following list...")
        logger.info("="*60)

        following_list = messenger.get_following_list()

        if not following_list:
            logger.error("No following users found or failed to fetch list. Exiting.")
            return

        logger.info(f"\nFound {len(following_list)} users in your following list")
        logger.info("="*60)

        success_count = 0
        fail_count = 0

        logger.info("\n" + "="*60)
        logger.info("Starting message campaign...")
        logger.info("="*60 + "\n")

        for i, recipient_username in enumerate(following_list, 1):
            logger.info(f"[{i}/{len(following_list)}] Processing: @{recipient_username}")

            if messenger.send_message_to_username(recipient_username, message):
                success_count += 1
            else:
                fail_count += 1

            if i < len(following_list):
                delay = random.uniform(15, 25)
                logger.info(f"Waiting {delay:.1f} seconds before next message...\n")
                time.sleep(delay)

        logger.info("\n" + "="*60)
        logger.info("Campaign Summary")
        logger.info("="*60)
        logger.info(f"Total recipients: {len(following_list)}")
        logger.info(f"✓ Successful: {success_count}")
        logger.info(f"✗ Failed: {fail_count}")
        logger.info("="*60)

    except KeyboardInterrupt:
        logger.info("\n⚠️  Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        messenger.close()
        logger.info("Script completed")


def run_messaging_campaign():
    """Main function to run the messaging campaign"""
    logger.info("="*60)
    logger.info("Instagram Messenger Bot Started")
    logger.info("="*60)

    username, password, message, schedule_time = get_credentials_from_cli()

    if schedule_time != "now":
        scheduler = BlockingScheduler()
        hour, minute = map(int, schedule_time.split(':'))

        def scheduled_job():
            run_messaging_campaign_with_params(username, password, message)

        scheduler.add_job(scheduled_job, 'cron', hour=hour, minute=minute)

        logger.info(f"\n📅 Campaign scheduled to run daily at {schedule_time}")
        logger.info("The bot will start at the scheduled time.")
        logger.info("Press Ctrl+C to cancel the scheduler\n")

        try:
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("\n⚠️  Scheduler stopped by user")
        return

    messenger = InstagramMessenger(username, password)

    try:
        messenger.setup_driver()
        if not messenger.login():
            logger.error("Login failed. Exiting.")
            return

        logger.info("\n" + "="*60)
        logger.info("Fetching your following list...")
        logger.info("="*60)

        following_list = messenger.get_following_list()

        if not following_list:
            logger.error("No following users found or failed to fetch list. Exiting.")
            return

        logger.info(f"\nFound {len(following_list)} users in your following list")
        logger.info("="*60)

        print(f"\n⚠️  About to send messages to {len(following_list)} users")
        print(f"⚠️  Instagram rate limits: Recommended max 20-50 messages per day")
        confirm = input(f"\nProceed with sending to all {len(following_list)} users? (yes/no): ").strip().lower()

        if confirm not in ['yes', 'y']:
            logger.info("Campaign cancelled by user")
            return

        limit = input(f"\nEnter max number of messages to send (or press Enter for all {len(following_list)}): ").strip()
        if limit.isdigit():
            following_list = following_list[:int(limit)]
            logger.info(f"Limited to first {len(following_list)} users")

        success_count = 0
        fail_count = 0

        logger.info("\n" + "="*60)
        logger.info("Starting message campaign...")
        logger.info("="*60 + "\n")

        for i, recipient_username in enumerate(following_list, 1):
            logger.info(f"[{i}/{len(following_list)}] Processing: @{recipient_username}")

            if messenger.send_message_to_username(recipient_username, message):
                success_count += 1
            else:
                fail_count += 1

            if i < len(following_list):
                delay = random.uniform(15, 25)
                logger.info(f"Waiting {delay:.1f} seconds before next message...\n")
                time.sleep(delay)

        logger.info("\n" + "="*60)
        logger.info("Campaign Summary")
        logger.info("="*60)
        logger.info(f"Total recipients: {len(following_list)}")
        logger.info(f"✓ Successful: {success_count}")
        logger.info(f"✗ Failed: {fail_count}")
        logger.info("="*60)

    except KeyboardInterrupt:
        logger.info("\n⚠️  Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        messenger.close()
        logger.info("Script completed")


def main():
    """Main entry point"""
    run_messaging_campaign()


if __name__ == "__main__":
    main()
