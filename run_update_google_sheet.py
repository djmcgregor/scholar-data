from os import getenv
import pandas as pd
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def update_sheet():
    spreadsheet_id = getenv("SPREADSHEET_ID")
    range_name = 'Sheet1!A1:B3'

    # Load the CSV data into a DataFrame
    df = pd.read_csv('data/total_metrics.csv')

    # Convert DataFrame to a list of lists
    values = df.values.tolist()

    # Prepare the request body
    body = {
        'values': values
    }

    # Update google sheet
    service_account_info = json.loads(getenv("GOOGLE_SERVICE_ACCOUNT_KEY"))
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_info(service_account_info,
                                                        scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()


if __name__ == "__main__":
    update_sheet()
