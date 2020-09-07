from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def hh(main_link, find_text, page_number):
#https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_field=name&text=data+scientist&page=1
    response = requests.get(main_link+'/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_field=name&text='+find_text+'&page=0', headers = headers)

    soup = bs(response.text,'html.parser')

    hh_jobs = []

    page_block = soup.find('div', {'data-qa': 'pager-block'})
    if not page_block:
        page_number = 1
    else:
        page_number = int(page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())

    for number in range(page_number):

        jobs_mass = soup.find('div',{'class':'vacancy-serp'})

        jobs_list = jobs_mass.findChildren(recursive = False)

        for job in jobs_list:

            job_data={}

            data=job.find('span',{'class':'g-user-content'})

            if data != None:

                main_info = data.findChild()

                job_name = main_info.getText()

                job_link = main_info['href']

                salary = job.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})

                if not salary:
                    salary_min = None
                    salary_max = None
                    salary_currency = None
                else:
                    salary = salary.getText() \
                        .replace(u'\xa0', u'')

                    salary = re.split(r'\s|-', salary)

                    if salary[0] == 'до':
                        salary_min = None
                        salary_max = int(salary[1])
                    elif salary[0] == 'от':
                        salary_min = int(salary[1])
                        salary_max = None
                    else:
                        salary_min = int(salary[0])
                        salary_max = int(salary[1])

                    salary_currency = salary[2]

                job_data['salary_min'] = salary_min
                job_data['salary_max'] = salary_max
                job_data['salary_currency'] = salary_currency


                job_data['link'] = job_link

                job_data['name'] = job_name

                job_data['site'] = 'HeadHunter'

                hh_jobs.append(job_data)

        if number == page_number-1:
            break
        else:
            next_btn_find = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
            next_btn_link = next_btn_find['href']
            response = requests.get(main_link + next_btn_link, headers=headers).text
            soup = bs(response, 'html.parser')

    pprint( hh_jobs)

    return  hh_jobs

find_text = 'Data Scientist'

page_number = 2  # Времени не хватило цикл сделать от первой до последней страницы, поэтому пока вот такое "топорное" решение

hh('https://hh.ru', find_text, page_number)

# Домашнее задание 3. Задача 1. Запускаем сервер MongoDB
client = MongoClient('127.0.0.1',27017)
db = client['users_db_new']
hh_db = db.hh

hh_db.insert_many(hh('https://hh.ru', find_text, page_number))

# Задача 2 в условии нужно найти зарплату более введенной суммы. При этом требуется сделать поиск по двум полям.
# Но по идее достаточно по одному - по минимальной ЗП (т.к. какая разница какая максимальная, если нужно найти зарплату
# БОЛЬШЕ чем задано. Ну раз по двум, то по двум.
for number in hh_db.find( {'salary_max':{'$gt':100000}, 'salary_min':{'$gt':50000} } ):
    pprint (number)


# Задача 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
# лучше сразу ее сделать, так удобнее, но сделаем по порядку.

hh_count = hh('https://hh.ru', find_text, page_number)

for number in hh_count:
    hh_db.update_many({'link': number['link']}, {'$set': number}, upsert=True)

# Либо такой вариант:
for number in hh_count:
        repeat = hh_db.find_one(number)
        if repeat is None:
            hh_db.insert_one(number)