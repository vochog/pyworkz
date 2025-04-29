#!/usr/bin/env python3

import os
import time
from flask import Flask, render_template, request, redirect, url_for
import gspread
from typing_extensions import Literal
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Google Sheets Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS_FILE = 'credentials.json'  # Replace with your credentials file
SPREADSHEET_ID = 'your-spreadsheet-id'  # Replace with your spreadsheet ID

# Initialize Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Selenium setup
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'  # Update this path

def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    return driver

def scrape_tiktok_video(url):
    driver = setup_selenium()
    try:
        driver.get(url)
        
        # Wait for video to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'video'))
        )
        
        # Get video details (customize based on what you want to scrape)
        video_element = driver.find_element(By.TAG_NAME, 'video')
        # video_src = video_element.get_attribute('src')
        
        # Get other metadata
        # username = driver.find_element(By.XPATH, '//*[@data-e2e="browse-username"]').text
        # username = driver.find_element(By.XPATH, '//*[@data-e2e="href"]').text
        # username = driver.find_element((By.XPATH, '//a[@data-e2e="video-author-avatar"]'))
        # username = driver.find_element(By.XPATH, '..//*[@data-e2e="video-user-name"]').text
        # description = driver.find_element(By.XPATH, '//*[@data-e2e="browse-desc"]').text
        description = driver.find_element(By.XPATH, '//*[@data-e2e="v2t-title"]').text
        # likes = driver.find_element(By.XPATH, '//*[@data-e2e="browse-like-count"]').text
        
        return {
            'url': url,
            # 'video_src': video_src,
            # 'username': username,
            'description': description,
            # 'likes': likes,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"Error scraping TikTok: {e}")
        return None
    finally:
        driver.quit()

def add_to_google_sheets(data):
    if data:
        try:
            sheet.append_row([
                data['timestamp'],
                data['url'],
                # data['username']
                data['description']
                # data['likes'],
                # data['video_src']
            ])
            return True
        except Exception as e:
            print(f"Error adding to Google Sheets: {e}")
            return False
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tiktok_url = request.form.get('tiktok_url')
        if tiktok_url:
            video_data = scrape_tiktok_video(tiktok_url)
            if video_data:
                success = add_to_google_sheets(video_data)
                if success:
                    return redirect(url_for('success'))
        return redirect(url_for('error'))
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
