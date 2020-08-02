import pickle
import os.path

import pandas as pd

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class DataFetcher:
    def __init__(self, spreadsheet_id, token_file, credentials_file):
        self.SPREADSHEET_ID = spreadsheet_id
        self._SHEETS_SERVICE = self._get_sheets_service(
            self._get_credentials(token_file, credentials_file)
        )
        self._DATA_RANGES = {
            'Temperature': 'Temperature!A1:D',
            'Events': 'Events!A1:C',
        }

    @staticmethod
    def _get_credentials(token_file, credentials_file):
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    @staticmethod
    def _get_sheets_service(credentials):
        service = build('sheets', 'v4', credentials=credentials)
        return service.spreadsheets()

    def get_temperatures(self):
        result = (
            self._SHEETS_SERVICE.values()
            .get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=self._DATA_RANGES['Temperature'],
            )
            .execute()
        )
        values = result.get('values', [])

        if not values:
            raise ValueError('No temperature values found.')

        temperatures = pd.DataFrame(values[1:], columns=values[0])
        temperatures['Date'] = pd.to_datetime(temperatures['Date'])
        temperatures['Temperature'] = temperatures['Temperature'].astype(float)

        return temperatures

    def get_events(self):
        result = (
            self._SHEETS_SERVICE.values()
            .get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=self._DATA_RANGES['Events'],
            )
            .execute()
        )
        values = result.get('values', [])

        if not values:
            raise ValueError('No events found.')

        # Filter out events that haven't ended yet
        values = [val for val in values if len(val) == 3]

        events = pd.DataFrame(values[1:], columns=values[0])
        events['StartDate'] = pd.to_datetime(events['StartDate'])
        events['EndDate'] = pd.to_datetime(events['EndDate'])

        return events
