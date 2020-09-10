from pprint import pprint
from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://yandex.ru'
response = requests.get(main_link)

dom = html.fromstring(response.text)

items = dom.xpath("//ol//li")
yandex = []
for item in items:
    news = {}
    name = 'Яндекс-Новости'
    text = item.xpath(".//span[@class='news__item-content ']/text()")
    link = item.xpath(".//a[@class='home-link list__item-content list__item-content_with-icon home-link_black_yes']/@href")
    response_link =requests.get(link[0])
    dom2 = html.fromstring(response_link.text)
    date = dom2.xpath("//div[1][@class='mg-snippet__wrapper']//span[@class='news-snippet-source-info__time']/text()")
    if date == []:
        date = dom2.xpath("//div[1][@class='news-card-snippet snippet']//span[@class='news-card-snippet__time']/text()")
    if date == []:
        date = dom2.xpath("//div[1][@class='mg-snippet mg-snippet_without-text news-story__snippet']//span[@class='news-snippet-source-info__time']/text()")
    # По дате пришлось с условием делать, т.к. на разных выборках новостей - в разных местах даты находятся. Не получилось общий путь подобрать
    #print(date)
    news['name'] = name
    news['text'] = text
    news['link'] = link
    news['data'] = date
    yandex.append(news)

pprint(yandex)
