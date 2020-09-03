from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def hh(main_link, find_text, page_number):
#https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_field=name&text=data+scientist&page=1
    response = requests.get(main_link+'/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_field=name&text='+find_text+'&page=0', headers = headers)

    soup = bs(response.text,'html.parser')

    hh_jobs = []

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

                salary = job.find('div',{'class':'vacancy-serp__vacancy-compensation'})

                job_data['link'] = job_link

                job_data['name'] = job_name

                job_data['salary'] = salary

                job_data['site'] = 'HeadHunter'

                hh_jobs.append(job_data)

        next_btn_find = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        next_btn_link = next_btn_find['href']
        response = requests.get(main_link + next_btn_link, headers=headers).text
        soup = bs(response, 'html.parser')

    pprint( hh_jobs)

    return  hh_jobs

find_text = 'Data Scientist'

page_number = 2  # Времени не хватило цикл сделать от первой до последней страницы, поэтому пока вот такое "топорное" решение

hh('https://hh.ru', find_text, page_number)

