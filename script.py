from bs4 import BeautifulSoup
import requests
import gspread
from gspread.exceptions import *
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def scrape(url, worksheet):
    html = requests.get(url)
    #取得したHTMLをパース
    soup = BeautifulSoup(html.content, "html.parser")

    r = next_available_row(worksheet)

    datetimestr = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    worksheet.update_acell('A' + str(r), datetimestr)
    worksheet.update_acell('B' + str(r), soup.title.get_text())

    start_ascii = 66
    for i in range(1, 7):
        elems = soup.find_all('h' + str(i))
        text_list = []
        for elem in elems:
            text_list.append(elem.get_text())
        text = ','.join(text_list)
        worksheet.update_acell(chr(start_ascii + i) + str(r), text)
    
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))  # fastest
    return str(len(str_list) + 1)

def get_gspread_book(secret_key, book_name):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_key, scope)
    gc = gspread.authorize(credentials)
    book = gc.open(book_name)
    return book

''' メイン処理 '''
if __name__ == '__main__':
    url = 'https://qiita.com/rusarusa/items/d7f014ba80d6fe7a3e07'
    secret_key = 'secret_key/lancers01-e93298c251a1.json'
    book_name = 'metadata'
    sheet_name = 'result'

    sheet = get_gspread_book(secret_key, book_name).worksheet(sheet_name)
    scrape(url, worksheet)

    
    