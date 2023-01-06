import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)


def field_ttn(tabble, letter, idnewttn):  # приходит словарь
    try:
        if tabble == 'ОПТ':
            sheet = client.open("nameSheets").sheet1
        if tabble == 'ОПТ Наложки':
            sheet = client.open("nameSheets").get_worksheet(1)
        if tabble == 'Розница':
            sheet = client.open("nameSheets").get_worksheet(2)
        for key in idnewttn:
            cell = sheet.find(key)
            cellrow = (letter + str(cell.row))
            sheet.update(cellrow, idnewttn[key])

    except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
        print('проблема в перетасовке таблиц')
