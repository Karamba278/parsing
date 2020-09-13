from pprint import pprint
from lxml import html
import requests
import re

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://news.mail.ru/'
response = requests.get(main_link)
dom = html.fromstring(response.text)
items = dom.xpath("//li[@class='list__item']")
mailru = []
for item in items:
    news = {}
    name = 'Новости Mail.ru'
    text = item.xpath(".//a[@class='list__text']/text() | .//span[@class='link__text']/text()")
    text[0] = text[0].replace("\xa0", "")
    link = item.xpath(".//a[@class='list__text']/@href | .//a[@class='link link_flex']/@href")
    if re.search(r'\bru\b', link[0]):
        pass
    else:
        link[0] = 'https://news.mail.ru' + link[0]
    response_link = requests.get(link[0])
    dom2 = html.fromstring(response_link.text)
    date = dom2.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    news['name'] = name
    news['text'] = text
    text = []
    news['link'] = link
    news['data'] = date
    mailru.append(news)
pprint(mailru)
