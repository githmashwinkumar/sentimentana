pip install gspread oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

#scope = ['https://spreadsheets.google.com/feeds']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive"]
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets'+"https://www.googleapis.com/auth/drive"+"https://www.googleapis.com/auth/drive"

creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('Y:/Ashwin/ds', 'SAFromPython-.json'), SCOPES)
client = gspread.authorize(creds)

sheet = client.open("Polarity").sheet1

#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)
sheet.update_cell(2, 1, "I just wrote to a spreadsheet using Python!")