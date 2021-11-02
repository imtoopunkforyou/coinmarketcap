import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from config import FIRST_PAGE, LAST_PAGE
import csv
from pyexcel.cookbook import merge_all_to_a_book 
import glob


#options
options = webdriver.ChromeOptions()
options.add_argument("--headless")

url = "https://coinmarketcap.com/?page="


def links_on_page(url):
    browser = webdriver.Chrome(
    executable_path="/home/imtoopunkforyou/prog/coinmarketcap/chromedriver", options=options)
    
    coins_links = []
    browser.get(url)
    time.sleep(4)
    links_elements = browser.find_elements_by_class_name('cmc-link')
    all_links_in_page = []
    for link in links_elements:
        all_links_in_page.append(link.get_attribute('href'))
    for link in all_links_in_page:
        link = link[:-1]
        if 'currencies' in link and link.count('/') == 4:
            coins_links.append(link)
    coins_links.pop()
    browser.close()
    browser.quit()
    return coins_links

def parse_info_about_coin(link):
    response = requests.get(link)
    time.sleep(3)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h2').get_text()
    price = soup.find('div', class_='priceValue').get_text()
    watchlists = soup.find_all('div', class_='namePill')[2].get_text()
    watchlists = ''.join(filter(str.isdigit, watchlists))
    result = []
    result.append(title)
    result.append(link)
    result.append(price)
    result.append(watchlists)
    return result

if __name__ == "__main__":
    start_time = time.time()
    all_links = []
    header = ['Title', 'Link', 'Price', 'Watchlists']
    for i in range(FIRST_PAGE, LAST_PAGE+1):
        links = links_on_page(url+str(i))
        for link in links:
            all_links.append(link)
        with open("info.csv", 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(header)
            count = 0
            for link in all_links:
                info = parse_info_about_coin(link)
                writer.writerow(info)
                count+=1
                if count % 25 == 0:
                    print("Количество готовых строк: " + str(count))
    print("Преобразую данныe в формат .xlsx \n")
    text_date = str(datetime.today())
    text_date = text_date.replace('-', '_')
    text_date = text_date.replace(' ', '_')
    text_date = text_date.replace('.', '_')
    text_date = text_date.replace(':', '_')
    text_date = text_date + '.xlsx'
    merge_all_to_a_book(glob.glob("info.csv"), text_date)
    print("РАБОТА ОКОНЧЕНА \n")
    print("Прошло времени: %s минут" % str(int((time.time() - start_time)/60)))




        

