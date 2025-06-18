# Attendance Tracker

Automate attendance checking and notifications via Telegram using GitHub Actions.

## Setup (GitHub Actions Only)

1. **Fork or clone this repository to your own GitHub account.**
2. **Add your credentials as GitHub Secrets:**
   - Go to your repository on GitHub.
   - Navigate to `Settings` → `Secrets and variables` → `Actions` → `New repository secret`.
   - Add the following secrets:
     - `ATTENDANCE_USERNAME`: Your attendance portal username
     - `ATTENDANCE_PASSWORD`: Your attendance portal password
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
     - `TELEGRAM_CHAT_ID`: Your Telegram chat ID
3. **Configure the workflow schedule if needed:**
   - Edit `.github/workflows/main.yml` or `.github/workflows/attendance.yml` to adjust the schedule or triggers.

## Usage

- **Automated:**
  - The workflow will run automatically based on the schedule defined in the workflow file and send you a Telegram notification.
- **On-demand:**
  - You can manually trigger the workflow from the GitHub Actions tab or via the Telegram bot (see `bot.py`).

## Notes
- Do NOT store your credentials in the code or commit them to the repository.
- This project is intended for use with GitHub Actions only. For local use, additional setup is required. 