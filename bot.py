import telebot
import requests

# Constants
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GITHUB_REPO = "vjjayanth/attendance-tracker"  # Replace with your GitHub repo
GITHUB_TOKEN = os.getenv("GIT_TOKEN")  # GitHub Token stored as a secret

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['check_attendance'])
def check_attendance(message):
    """Trigger GitHub Actions workflow for attendance tracking."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/automate_attendance_tracking.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main"}  # Change branch if needed

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 204:
        bot.reply_to(message, "✅ Attendance check started! You will receive a notification soon.")
    else:
        bot.reply_to(message, f"❌ Failed to trigger GitHub Actions: {response.text}")

bot.polling()
