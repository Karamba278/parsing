# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacancy140920

    def process_item(self, item, spider):
        salary_min = None
        salary_max = None
        salary_currency = None

        salary = item['salary']

        if spider.name == 'hhru':

            for salary_one in range(len(salary)):
                if salary[salary_one] == 'от ':
                    salary_min = salary[salary_one+1]
                    salary_min = salary_min.replace(u'\xa0', u'')
                if salary[salary_one] == ' до ':
                    salary_max = salary[salary_one+1]
                    salary_max = salary_max.replace(u'\xa0', u'')
                if salary[salary_one] == 'USD' or salary[salary_one] == 'руб.':
                    salary_currency = salary[salary_one]

        if spider.name == 'superjob_ru': # Тут в отличие от hh.ru - так же компактно не получится алгоритм поиска макс/мин/валюты реализовать
            # так как много различных вариантов написания зарплаты, но способ тот же будем использовать.
            for salary_one in range(len(salary)):
                salary[salary_one] = salary[salary_one].replace(u'\xa0', u'')
            for salary_one in range(len(salary)): #Тут пока так же как и с hhru действуем
                if salary[salary_one] == 'от':
                    salary_min = salary[salary_one+2]
                if salary[salary_one] == 'до':
                    salary_max = salary[salary_one+2]
                if salary[salary_one] == 'USD' or salary[salary_one] == 'руб.':
                    salary_currency = salary[salary_one]
            if  salary_min == None and salary_max == None: #А вот тут обрабатываем как раз другие варианты записи salary
                if salary[0].isdigit() == True and salary[1].isdigit() == True:
                    salary_min = salary[0]
                    salary_max = salary[1]
                elif salary[0].isdigit()==True and salary[1].isdigit()==False:
                    salary_min = salary[0]

        item['min_salary'] = salary_min
        item['max_salary'] = salary_max
        item['curency'] = salary_currency

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
