# from __future__ import print_function

import os.path
import performance

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
sa_file = "C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\creds_newexample.json"
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4'
SAMPLE_RANGE_NAME = 'b Performance'

credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
service = build('sheets', 'v4', credentials=credentials)

def read(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    # """Shows basic usage of the Sheets API.
    # Prints values from a sample spreadsheet.
    # """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    # service = build('sheets', 'v4', credentials=credentials)
    # if os.path.exists('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\client.json'):
    #     creds = Credentials.from_authorized_user_file('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\client2.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        #service = build('sheets', 'v4', credentials=credentials) #, client_options={"quota_project_id": "example-422910"}

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        columns = values[1]
        data = values[2:]
        df = pd.DataFrame(data, columns=columns)
        return df['FIO'].values
    except HttpError as err:
        print(err)

def write(data, SAMPLE_SPREADSHEET_ID, sheetname):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    #credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\token.json'):
    #     creds = Credentials.from_authorized_user_file('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\client.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        #service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        vr_data = {
            'majorDimension': 'ROWS',
            'values': data
        }
        sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption='USER_ENTERED',
            range=sheetname + '!A3',
            body=vr_data
        ).execute()
        # print(er)
    except HttpError as err:
        print(err)

def test():
    print(__name__)


if __name__ == '__main__':
    # print(__name__)
    # performance.test()
    # credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    # service = build('sheets', 'v4', credentials=credentials)
    for val in read('13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance').values:
        print(val[0])
    # newdata = [['Стрельцов Андрей Александрович', '', "'+", "'+", '', "'+", "'+", "'+", "'+", "'+", '', [], '2024-03-05 23:34:08', '', '', '']]
    # write(newdata, '13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance')
    # listsandsheets = {'a': {'SAMPLE_SPREADSHEET_ID': '1kGblujShU2h1GQ13mXHZQnE3f4vmeaG-fy4PZFQ5kmU',
    #                         'SAMPLE_RANGE_NAME': 'Performance2023'},
    #                   'b': {'SAMPLE_SPREADSHEET_ID': '1-XdadVGTx6L2bVC_B16vJUhjpNQIKht1Ve709n0e6lc',
    #                         'SAMPLE_RANGE_NAME': 'b Performance'}}
    # for key in ['a', 'b']:
    #    print(read(listsandsheets[key]['SAMPLE_SPREADSHEET_ID'], listsandsheets[key]['SAMPLE_RANGE_NAME']))