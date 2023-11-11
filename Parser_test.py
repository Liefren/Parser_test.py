import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Set the Google Sheets credentials path
credentials_path = 'D:/123.json'  # Replace with your actual credentials path

def soup2list(src, list_, attr=None):
    if attr:
        for val in src:
            list_.append(val[attr])
    else:
        for val in src:
            list_.append(val.get_text())
reviews_data = []
users = []
userReviewNum = []
ratings = []
locations = []
dates = []
reviews = []

from_page = 1
to_page = 60

for i in range(from_page, to_page + 1):
    response = requests.get(f"https://www.trustpilot.com/review/www.google.com?page={i}")
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")

    for e in soup.select('article'):
        reviews_data.append({
            'review_title':e.h2.text,
            'review_date_original': e.select_one('[data-service-review-date-of-experience-typography]').text.split(': ')[-1],
            'review_rating':e.select_one('[data-service-review-rating] img').get('alt'),
            'review_text': e.select_one('[data-service-review-text-typography]').text if e.select_one('[data-service-review-text-typography]') else None,
            'page_number':i
        })

# Create a DataFrame from the reviews data
df = pd.DataFrame(reviews_data)

# Authenticate with the Google Sheets API
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet_title = "444555"
spreadsheet = gc.open(spreadsheet_title)

# Select a specific worksheet (Sheet1 in this case)
worksheet = spreadsheet.get_worksheet(0)

# Write data to Google Sheets
worksheet.update(values=[df.columns.values.tolist()] + df.values.tolist(), range_name="A1", value_input_option='USER_ENTERED')

print("Reviews have been uploaded to Google Sheets.")