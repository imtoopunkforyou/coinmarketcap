import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from config import FIRST_PAGE, LAST_PAGE
import csv
from pyexcel.cookbook import merge_all_to_a_book
import glob
import os


url = "https://coinmarketcap.com/?page="


def links_on_page(url):
    all_links_in_page = []
    coins_links = []
    response = requests.get(url)
    time.sleep(3)
    soup = BeautifulSoup(response.text, 'lxml')
    for link in soup.find_all(class_='cmc-link'):
        all_links_in_page.append(link.get('href'))
    for link in all_links_in_page:
        link = link[:-1]
        if 'currencies' in link and link.count('/') == 2:
            if len(coins_links) < 100:
                link = "https://coinmarketcap.com"+link
                coins_links.append(link)
    return coins_links


def parse_info_about_coin(link):
    response = requests.get(link)
    time.sleep(4)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h2').get_text()
    price = soup.find('div', class_='priceValue').get_text()
    watchlists = soup.find_all('div', class_='namePill')[2].get_text()
    watchlists = ''.join(filter(str.isdigit, watchlists))
    return title, link, price, watchlists


def text_date_time():
    delete_symbols = ['-', ' ', '.', ':']
    text_date = str(datetime.today())
    for i in delete_symbols:
        text_date = text_date.replace(i, '_')
    text_date += '.xlsx'
    return text_date


if __name__ == "__main__":
    start_time = time.time()
    all_links = []
    count = 0
    # выделяем ссылки на все монеты на указанных страницах
    for i in range(FIRST_PAGE, LAST_PAGE+1):
        links = links_on_page(url+str(i))
        for link in links:
            all_links.append(link)
    # записываем в файл
    with open("info.csv", 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        header = ['Title', 'Link', 'Price', 'Watchlists']
        writer.writerow(header)
        for link in all_links:
            info = parse_info_about_coin(link)
            writer.writerow(info)
            count += 1
            print("Количество готовых монет: "+str(count)+"\n")
            if count % 10 == 0:
                print("Всего монет: "+str(len(all_links))+"\n")
    print("Преобразую данныe в формат .xlsx \n")
    merge_all_to_a_book(glob.glob("info.csv"), text_date_time())
    os.remove(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'info.csv'))
    print("РАБОТА ОКОНЧЕНА \n")
    print("Прошло времени: %s минут" % str(int((time.time() - start_time)/60)))
