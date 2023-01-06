from Selenium import chrome

chrome.avto_login()
#chrome.sms_novaposhta()
# chrome.avtologin_cookie()
read_sheet.sendOPT()
read_sheet.sendOPT_NAL()
read_sheet.send_roz()
retry = input("еще раз?")
if retry == "1" or retry == "da":
    read_sheet.connection()
    read_sheet.sendOPT()
    read_sheet.sendOPT_NAL()
    read_sheet.send_roz()
else:
    chrome.driver.quit()