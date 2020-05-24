import json
import gspread
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

googleAPI = './config/credentials.json'
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials = service_account.Credentials.from_service_account_file(googleAPI)
scopedCreds = credentials.with_scopes(scope)
gc = gspread.Client(auth=scopedCreds)
gc.session = AuthorizedSession(scopedCreds)

_client = gc.session


def get_sheet():
    config = json.load(open("./config/credentials.json"))
    sheet_url = 'https://docs.google.com/spreadsheets/d/' + config['spreadsheet_key'] + '/edit?usp=sharing'
    return gc.open_by_url(sheet_url)


def get_player_sheet():
    sheet = get_sheet()

    return sheet.sheet1
