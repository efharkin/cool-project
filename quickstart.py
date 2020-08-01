import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import matplotlib.pyplot as plt

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = 'secret'
SAMPLE_RANGE_NAME = 'Temperature!A2:D'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Shets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    df = pd.DataFrame(values)
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    df.iloc[:, -1] = df.iloc[:, -1].astype(float)

    ax = plt.subplot(111)
    for location in df.iloc[:, 1].unique():
        subset = df.loc[df.iloc[:, 1] == location, :]
        plt.plot(subset.iloc[:, 0], subset.iloc[:, -1], '.-', label=location)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time')
    plt.legend()
    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()
