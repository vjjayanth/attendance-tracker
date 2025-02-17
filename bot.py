import telebot
import requests

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
GITHUB_REPO = "username/repo-name"  # Replace with your repo
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['check_attendance'])
def check_attendance(message):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/attendance.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main"}  # Change branch name if needed

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 204:
        bot.reply_to(message, "✅ Attendance check started! You'll get a notification soon.")
    else:
        bot.reply_to(message, f"❌ Failed to trigger GitHub Actions: {response.text}")

bot.polling()
