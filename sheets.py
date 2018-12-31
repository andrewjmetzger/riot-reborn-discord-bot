import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

_credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "config/credentials.json",
    [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
)

_client = gspread.authorize( _credentials )


def _get_client():
    if _credentials.access_token_expired:
        _client.login()

    return _client


def get_sheet():
    _sheet = json.load(open("config/credentials.json"))
    return _get_client().open_by_key(_sheet["spreadsheet_key"])


def get_player_sheet():
    sheet = get_sheet()

    return sheet.get_worksheet( 0 )
