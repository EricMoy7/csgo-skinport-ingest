import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd

class GoogleSheets:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = ""


    def authenticate(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        client = gspread.authorize(credentials)

        self.client = client

        return client
    
    def push_df(self, df, ss_url):
        spreadsheet = self.client.open_by_url(ss_url)
        worksheet = spreadsheet.sheet1
        gd.set_with_dataframe(worksheet, df)
        