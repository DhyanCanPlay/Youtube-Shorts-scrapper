import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import random

def upload_random_short(yshorts_folder, email, password):
    """Uploads a random short from the specified folder and deletes it."""

    try:
        video_files = [f for f in os.listdir(yshorts_folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.webm'))]
        if not video_files:
            print("No video files found in the YShorts folder.")
            return
        random_video = random.choice(video_files)
        video_file_path = os.path.join(yshorts_folder, random_video)
        driver = uc.Chrome()
        driver.get("https://www.youtube.com/upload")
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        upload_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_button.send_keys(os.path.abspath(video_file_path))

        # Wait for upload to begin (adjust time as needed)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "title-textarea")))

        # Navigate to Visibility tab
        visibility_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "step-badge-3")))
        visibility_button.click()

        # Wait for the visibility tab to load.
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//tp-yt-paper-radio-button[@name='PUBLIC']")))

        # Select the "Public" radio button
        public_radio_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-radio-button[@name='PUBLIC']")))
        public_radio_button.click()

        # Wait for a moment before attempting to click the "Publish" button
        time.sleep(5)

        # Click the "Publish" button to publish
        publish_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Publish']")))
        publish_button.click()

        # Wait for publish to finish.
        time.sleep(10)

        print(f"Upload of '{random_video}' started. Please monitor the browser.")
        driver.quit()

        os.remove(video_file_path)
        print(f"Deleted: {video_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
         #only uncomment when testing is complete.
        pass

def main():
    yshorts_folder = "YShorts"
    email = input("Enter your YouTube/Google email: ")
    password = input("Enter your YouTube/Google password: ")
    upload_random_short(yshorts_folder, email, password)

if __name__ == "__main__":
    main()
