import os
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from Selenium import chrome
from Ttn import new_ttn
import re
# from connection import new_connection
from dotenv import load_dotenv

load_dotenv()

# Файл, полученный в Google Developer Console

from selenium.common.exceptions import TimeoutException



# старое подключение через оф библиотеку гугла(принимает данные пакетами)
def connection():
    CREDENTIALS_FILE = 'creds.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = os.getenv('TOKEN')

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # чтение страницы ОПТ, а именно строк ТТН(его присудствие Код/размер	ФИО / НП / Г. / Номер	Статус	Оплата\Наша цена
    purchasesOPT = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="ОПТ!A2499:H3100",
        majorDimension='ROWS'
    ).execute()

    # чтение страницы ОПТ НАЛОЖКИ, а именно строк ТТН(его присудствие Код/размер	ФИО / НП / Г. / Номер	Статус
    # Оплата\Наша цена
    purchasesOPT_NAL = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="ОПТ Наложки!A3100:I3500",
        majorDimension='ROWS'
    ).execute()

    # розница
    # чтение страницы розница, а именно строк ТТН(его присудствие Код/размер	ФИО / НП / Г. / Номер	Статус	Оплата\Наша цена
    purchases_roz = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="Розница!A1200:J1400",
        majorDimension='ROWS'
    ).execute()

    # чтениe размера коробок
    boxparams = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="коробки!A2:B900",
        majorDimension='ROWS'
    ).execute()

    return purchasesOPT, purchasesOPT_NAL, purchases_roz, boxparams


purchasesOPT, purchasesOPT_NAL, purchases_roz, boxparams = connection()

infosize = boxparams["values"]

purchasesOPT = purchasesOPT["values"]
purchasesOPT_NAL = purchasesOPT_NAL["values"]
purchases_roz = purchases_roz["values"]


# ищем кодтовара и его параметры коробки


def get_sizebox(vendcode):  # если не работает то дело в boxparams
    try:
        for size in infosize:
            if vendcode in size:
                param = size[1]  # параметры коробки
                if 'x' in param:
                    param = param.split('x')  # это "хэ" и "икс"
                elif 'х' in param:
                    param = param.split('х')  # выходя из функции теряются данные
                param = tuple(list(param))
                hight = param[0]
                lenth = param[1]
                width = param[2]
                return [str(hight), str(lenth), str(width)]
    except IndexError:
        print(vendcode + ' RINA NE VNESLA')


# отправляем данные на заполнение страницы
def sendOPT():
    idnewttn = {}
    try:
        for elem in purchasesOPT:
            id = elem[0]

            hight2 = 0
            lenth2 = 0
            width2 = 0

            hight3 = 0
            lenth3 = 0
            width3 = 0

            nal_opt = elem[-2]
            status = elem[3]
            if nal_opt != "Закрыт":
                continue
            if status:
                continue

            clientinfo = elem[5].split(' ')

            if clientinfo[-1] == '':
                clientinfo = clientinfo[0:-2]

            surname = clientinfo[0]
            name = clientinfo[1]

            number = clientinfo[-1]

            operator = number[0:3]
            phonenumber = number[3::]
            npdepartment = clientinfo[-2]

            city = ' '.join(clientinfo[2:-3])
            if 'й' in city:
                city = re.sub('й', 'й', city)

            if 'ї' in city:
                city = re.sub('ї', 'ї', city)
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            # другое Ё
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            if 'пгт' in city:
                city = re.sub('пгт', 'смт', city)

            price = elem[-1]
            vendcode = str(elem[4]).split(' ')
            idelement = elem[4]

            hight, lenth, width = get_sizebox(vendcode[0][0:4])

            if 2 < len(vendcode):
                hight2, lenth2, width2 = get_sizebox(vendcode[2])
                if 4 < len(vendcode):
                    hight3, lenth3, width3 = get_sizebox(vendcode[4])

            if len(status) == 0:
                newttn = chrome.avto_field(hight, lenth, width, hight2, lenth2, width2, hight3, lenth3, width3, price,
                                           idelement, surname, name, operator, phonenumber, city, npdepartment, nal_opt)
                newttn = re.sub(' ', '', newttn)
                newttn = re.sub("'", '', newttn)
                print(newttn, surname, name)
                idnewttn[str(id)] = str(newttn)
    except TimeoutException:
        print(id)
        pass
    finally:
        new_ttn.field_ttn("ОПТ", "D", idnewttn)


def sendOPT_NAL():
    idnewttn = {}
    try:
        for elem in purchasesOPT_NAL:
            id = elem[0]

            hight2 = 0
            lenth2 = 0
            width2 = 0

            hight3 = 0
            lenth3 = 0
            width3 = 0

            nal_opt = elem[-3]

            if nal_opt != 'Оформлен(НП)':
                continue

            clientinfo = elem[5].split(' ')

            if clientinfo[-1] == '':
                clientinfo = clientinfo[0:-2]

            status = elem[2]
            if status:
                continue

            surname = clientinfo[0]
            name = clientinfo[1]
            number = clientinfo[-1]
            if number == '':
                number = clientinfo[-2]
            operator = number[0:3]
            phonenumber = number[3::]
            npdepartment = clientinfo[-2]

            city = ' '.join(clientinfo[2:-3])
            price = elem[-1]

            if 'й' in city:
                city = re.sub('й', 'й', city)
            if 'ї' in city:
                city = re.sub('ї', 'ї', city)
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            # другое Ё
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            if 'пгт' in city:
                city = re.sub('пгт', 'смт', city)
            idelement = elem[4]

            vendcode = str(elem[4]).split(' ')
            hight, lenth, width = get_sizebox(vendcode[0][0:4])
            if 2 < len(vendcode) <= 4:
                hight2, lenth2, width2 = get_sizebox(vendcode[2])
                if 4 < len(vendcode):
                    hight3, lenth3, width3 = get_sizebox(vendcode[4])

            if len(status) == 0:
                newttn = chrome.avto_field(hight, lenth, width, hight2, lenth2, width2, hight3, lenth3, width3, price,
                                           idelement, surname, name, operator, phonenumber, city, npdepartment, nal_opt)
                newttn = re.sub(' ', '', newttn)
                idnewttn[str(id)] = str(newttn)
                print(newttn, surname, name)
    except TimeoutException:
        print(id)
    finally:
        new_ttn.field_ttn("ОПТ Наложки", "C", idnewttn)


def send_roz():
    idnewttn = {}
    try:
        for elem in purchases_roz:
            id = elem[0]

            hight2 = 0
            lenth2 = 0
            width2 = 0

            hight3 = 0
            lenth3 = 0
            width3 = 0

            nal_opt = elem[6]

            if nal_opt == "Null":
                continue
            clientinfo = elem[5].split(' ')

            if clientinfo[-1] == '':
                clientinfo = clientinfo[0:-2]

            status = elem[2]
            if status:
                continue

            surname = clientinfo[0]
            name = clientinfo[1]

            number = clientinfo[-1]
            operator = number[0:3]
            phonenumber = number[3::]

            npdepartment = clientinfo[-2]
            city = ' '.join(clientinfo[2:-3])
            
            price = elem[-1]

            if 'й' in city:
                city = re.sub('й', 'й', city)
            if 'ї' in city:
                city = re.sub('ї', 'ї', city)
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            # другое Ё
            if 'ё' in city:
                city = re.sub('ё', 'е', city)
            if 'пгт' in city:
                city = re.sub('пгт', 'смт', city)

            idelement = elem[3]

            vendcode = str(elem[3]).split(' ')
            hight, lenth, width = get_sizebox(vendcode[0][0:4])
            if 3 < len(vendcode):
                hight2, lenth2, width2 = get_sizebox(vendcode[2][0:4])
                if 4 < len(vendcode):
                    hight3, lenth3, width3 = get_sizebox(vendcode[4][0:4])

            if len(status) == 0:
                newttn = chrome.avto_field(hight, lenth, width, hight2, lenth2, width2, hight3, lenth3, width3, price,
                                           idelement, surname, name, operator, phonenumber, city, npdepartment, nal_opt)
                newttn = re.sub(' ', '', newttn)
                print(newttn, surname, name)
                idnewttn[str(id)] = str(newttn)
    except TimeoutException:
        print(id)
    finally:
        new_ttn.field_ttn("Розница", "C", idnewttn)


chrome.avto_login()
#chrome.sms_novaposhta()
# chrome.avtologin_cookie()
sendOPT()
sendOPT_NAL()
send_roz()
retry = input("еще раз?")
if retry == "1" or retry == "da":
    connection()
    sendOPT()
    sendOPT_NAL()
    send_roz()
else:
    chrome.driver.quit()
