import os
import csv
import requests

def read_notification_file():
    """Reads the notification.csv file and formats data as a message."""
    NOTIFICATION_FILE_PATH = "notification.csv"
    message_lines = ["📢 *Attendance Notification*\n"]
    try:
        with open(NOTIFICATION_FILE_PATH, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                date, subject, status = row
                if "Overall" in subject:
                    message_lines.append(f"\n⚡ *{subject}:* {status}")
                else:
                    emoji = "✅" if status.strip().lower() == "present" else "❌"
                    message_lines.append(f"{emoji} *{subject}:* {status}")
        return "\n".join(message_lines)
    except Exception as e:
        return f"⚠ Error reading notification file: {str(e)}"

def send_telegram_message():
    """Sends the attendance notification to Telegram."""
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    message = read_notification_file()
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Notification sent successfully!")
    else:
        print(f"❌ Failed to send notification: {response.text}") 