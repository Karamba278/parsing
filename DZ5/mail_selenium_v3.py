from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://mail.ru/')

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172@mail.ru')

try:
    pass_button = driver.find_element_by_id("mailbox:submit-button")
except exceptions.NoSuchElementException:
    print('Mail login not found')

pass_button.click()

passw = driver.find_element_by_id('mailbox:password-input')
passw.send_keys('NextPassword172')

try:
    enter_button = driver.find_element_by_id("mailbox:submit-button")
except exceptions.NoSuchElementException:
    print('Mail login not found')

enter_button.click()

time.sleep(20)

try:
    for i in range(40): #
        time.sleep(3)
        articles = driver.find_elements_by_xpath('//a[@data-id]')
        actions = ActionChains(driver)
        actions.move_to_element(articles[-1])
        actions.perform()
except:
    pass
time.sleep(5)
letters = driver.find_elements_by_xpath('//a[@data-id]')
print(len(letters)) # Это счетчик найденных письмем при помощи find_elements_by_xpath, в теории он должен равняться количеству входящих писем, но нет.
# Вот этот момент мне не очень понятен, т.к. программа проматывает скролл до конца, т.е. письма загружаются все.
# Но при этом письма при помощи find_elements_by_xpath все не находятся.
# Заметил некоторую зависимость от времени, если поставить время ожидания больше, 15 секунд, например, то находится больше элементов, 24. Но все равно не все письма находятся.
mailru = []

for letter in letters:
    info = {}
    try:
        fromWho = letter.find_element_by_class_name('ll-crpt')
        fromWho_adress = fromWho.get_attribute('title')
        letter_name_sel = letter.find_element_by_class_name('ll-sj__normal')
        letter_name = letter_name_sel.text
        short_descrition = letter.find_element_by_class_name('ll-sp__normal').text
        date_info = letter.find_element_by_xpath(".//div[@class='llc__content']/div[@class='llc__item llc__item_date']")
        date = date_info.text

    except:
        print('Ошибочка вышла')

    info['fromWho_adress'] = fromWho_adress
    info['letter_name'] = letter_name
    info['short_descrition'] = short_descrition
    info['date'] = date
    mailru.append(info)
driver.close()
pprint(mailru)