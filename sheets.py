import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def append_task(task, description, due_date, status):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    values = [[task, description, due_date, status]]
    body = {'values': values}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:D',
        valueInputOption='RAW',
        body=body
    ).execute()

# THIS MUST BE UNINDENTED
def get_tasks():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:D'
    ).execute()
    return result.get('values', [])
