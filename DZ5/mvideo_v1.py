from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.mvideo.ru')

try:
    hit_sale = driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]')

except:
    print('No hit-goods')

while True:
    try:
        next_button = WebDriverWait(hit_sale, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')))

        driver.execute_script("$(arguments[0]).click();", next_button)

    except:
        break

goods = hit_sale.find_elements_by_css_selector('li.gallery-list-item')

mvideo_goods = []

for good in goods:

    to_mvideo = {}

    title = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('innerHTML')

    link = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')

    price = float(good.find_element_by_css_selector('div.c-pdp-price__current').get_attribute('innerHTML').replace('&nbsp;', '').replace('¤', ''))

    image_link = good.find_element_by_css_selector('img[class="lazy product-tile-picture__image"]').get_attribute('src')

    to_mvideo['title'] = title
    to_mvideo['link'] = link
    to_mvideo['price'] = price
    to_mvideo['image_link'] = image_link

    mvideo_goods.append(to_mvideo)

driver.close()

pprint(mvideo_goods)