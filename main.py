from selenium import webdriver

import time


browser = webdriver.Chrome(
    executable_path="/home/imtoopunkforyou/prog/coinmarketcap/chromedriver")
url = "https://coinmarketcap.com/"
url_for_cycle = "https://coinmarketcap.com/?page=2"

coins_links = []

try:
    browser.get(url)
    time.sleep(5)
    links_elements = browser.find_elements_by_class_name('cmc-link')
    all_links_in_page = []
    for link in links_elements:
        all_links_in_page.append(link.get_attribute('href'))
    for link in all_links_in_page:
        link = link[:-1]
        if 'currencies' in link and link.count('/') == 4:
            coins_links.append(link)
    coins_links.pop()
    print(coins_links)
    print(len(coins_links))
    time.sleep(5000)
except Exception:
    print(Exception)
finally:
    browser.close()
    browser.quit()