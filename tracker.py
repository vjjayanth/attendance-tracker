from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import csv
import json
from datetime import datetime
import requests

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Automatically find and use ChromeDriver (No need to install manually)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.google.com")


# Constants
LOGIN_URL = "https://automation.vnrvjiet.ac.in/eduprime3"
JSON_FILE = "attendance.json"  # Stores last attendance
USERNAME = "22071A12C6"
PASSWORD = "Jai@2004"
FILE_NAME = "notification.csv"


# Subject mapping
subjects = {
    "22HS2EN301": "English Lab",
    "22MN6HS301": "ANCIENT WISDOM",
    "22OE1EN302": "OE",
    "22PC1AM202": "DE",
    "22PC1CS302": "WT",
    "22PC1IT302": "ML",
    "22PC2CS302": "WT LAB",
    "22PC2IT302": "DE / ML LAB",
    "22PE1DS303": "PE",
    "22PW4IT301": "INTERNSHIP"
}

# Helper function to compare attendance fractions (🔹 New function for clarity)
def check_attendance_change(previous, current):
    """Compare attendance fractions and determine if the student is Present or Absent."""
    try:
        prev_num, prev_den = map(int, previous.split('/'))
        curr_num, curr_den = map(int, current.split('/'))
        
        # If denominator is unchanged, no need to check further
        if prev_den == curr_den:
            return None  
        
        # If numerator increased proportionally, mark as Present, else Absent
        return "Present" if (curr_num - prev_num) == (curr_den - prev_den) else "Absent"
    except ValueError:
        return None  # Handle invalid data gracefully

# Load previous attendance (🔹 Load JSON once instead of multiple reads)
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as file:
        previous_attendance = json.load(file)
else:
    previous_attendance = {}  # Initialize if no previous data exists

try:
    # Step 1: Log in
    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    password_field = driver.find_element(By.NAME, "xpassword")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.url_changes(LOGIN_URL))
    print("Login successful")
    
    # Wait for the overlay (blockUI) to disappear before clicking
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI"))
    )
    # Step 2: Click on attendance icon
    attendance_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]"))
    )
    attendance_icon.click()

    # Step 3: Wait for the Popup to Appear
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div")))

    # Step 4: Extract Attendance Data
    attendance_table = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div[2]/div/div/div")
    rows = attendance_table.find_elements(By.TAG_NAME, "tr")

    cumulative_attendance = {}
    
    # (🔹 Optimized single loop for extracting attendance)
    for row in rows[1:-1]:  # Skipping header and total row
        columns = row.find_elements(By.XPATH, ".//td | .//th")
        if len(columns) >= 3:
            subject_code = columns[0].text.strip()
            cumulative = columns[2].text.strip()
            
            if subject_code in subjects:
                cumulative_attendance[subjects[subject_code]] = cumulative
            else:
                print(f"Warning: Unknown subject code {subject_code}")

    # Extract overall cumulative attendance
    total_attendance = rows[-1].find_elements(By.XPATH, ".//td | .//th")[2].text.strip()
    print("Updated Attendance Data:", cumulative_attendance)

    # Step 5: Compare Attendance (🔹 Now efficient and clearer)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")  # Added time component
    notification_data = [["Date", "Subject", "Status"]]
    attendance_changed = False

    for subject, curr_attendance in cumulative_attendance.items():
        prev_attendance = previous_attendance.get(subject.strip(), "0 / 0")# Default to avoid errors
        # print(subject, prev_attendance, sep='  ')
        # print("Keys in previous_attendance:", list(previous_attendance.keys()))
        # print("Keys in cumulative_attendance:", list(cumulative_attendance.keys()))

        status = check_attendance_change(prev_attendance, curr_attendance)

        if status:  # Only store changes
            notification_data.append([date_str, subject, status])
            attendance_changed = True

    # Always update total attendance (🔹 Now tracked properly)
    notification_data.append([date_str, "Overall", total_attendance])

    # Step 6: Write to Notification File Only if There Are Changes
    if attendance_changed:
        file_exists = os.path.isfile(FILE_NAME)
        with open(FILE_NAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(notification_data[0])  # Write header only once
            
            writer.writerows(notification_data[1:])  # Write new changes only

        print("⚡ Notification saved!")

    # Step 7: Update JSON File (🔹 Now writes only if needed)
    with open(JSON_FILE, "w") as file:
        json.dump(cumulative_attendance, file)

    print("✅ Attendance comparison done!")

    

    if os.path.exists("notification.csv"):
        print("✅ notification.csv exists!")
    else:
        print("❌ notification.csv NOT FOUND!")




    # Step 8: recieve notifications through telegram
        

    # Replace with your Telegram Bot Token and Chat ID
    TELEGRAM_BOT_TOKEN = "7735591874:AAHxx1ili9rLSV416lQsb2YFiWrVRwWTRkY"
    CHAT_ID = "1623826061"
    NOTIFICATION_FILE_PATH = "notification.csv"  # Update this if your file has a different name


    def read_notification_file():
        """Reads the notification.csv file and formats data as a message."""
        message_lines = ["📢 *Attendance Notification*\n"]
        
        try:
            with open(NOTIFICATION_FILE_PATH, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                
                for row in reader:
                    date, subject, status = row
                    if "Overall" in subject:  # Handle overall attendance separately
                        message_lines.append(f"\n⚡ *{subject}:* {status}")
                    else:
                        emoji = "✅" if status.strip().lower() == "present" else "❌"
                        message_lines.append(f"{emoji} *{subject}:* {status}")

            return "\n".join(message_lines)

        except Exception as e:
            return f"⚠ Error reading notification file: {str(e)}"

    def send_telegram_message():
        """Sends the attendance notification to Telegram."""
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

    # Run the function to send the message
    send_telegram_message()




except Exception as e:
    print("❌ Failed to access the page:", str(e))

# Close browser
driver.quit()
