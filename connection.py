import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)


# попытка нового подключения через библиотеку gspread

def new_connection():
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    # sheet = client.open("NEW CRM GINGER.WEBSTORE").worksheet("ОПТ")
    # purchasesOPT = sheet.get_all_values()
    #
    # sheet = client.open("NEW CRM GINGER.WEBSTORE").worksheet("ОПТ Наложки")
    # purchasesOPT_NAL = sheet.get_all_values()
    #
    # sheet = client.open("NEW CRM GINGER.WEBSTORE").worksheet("Розница")
    # purchases_roz = sheet.get_all_values()

    sheet = client.open("NAME").worksheet("коробки")
    boxparams = sheet.get_all_values()

    return boxparams
    # return purchasesOPT, purchasesOPT_NAL, purchases_roz, boxparams

#
def binary_search(boxparams, vencode):
    low = 0
    high = len(boxparams) - 1
    print(high)
    while low <= high:
        mid = low + high
        guess = boxparams[mid[0:4]]
        if guess == vencode:
            return vencode
        if guess > vencode:
            high = mid - 1
        else:
            low = mid + 1
        return None


def get_sizebox(vendcode):  # если не работает то дело в boxparams
    try:
        for size in infosize:
            if vendcode in size:
                param = size[1]  # параметwры коробки
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
        print(vendcode + 'NE VNESLA')


# hight, lenth, width = get_sizebox(vendcode[0][0:4])
boxparams = new_connection()
print(type(boxparams))
vencode = input("vencode:")
binary_search(boxparams, vencode)
