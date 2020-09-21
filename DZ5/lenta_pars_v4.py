from pprint import pprint
from lxml import html
import requests
import re

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link)
dom = html.fromstring(response.text)
items = dom.xpath("//div[@class='item']")
lenta = []
for item in items:
    news = {}
    name = 'Новости Lenta.ru'
    text = item.xpath("./a/text()")
    text[0] = text[0].replace("\xa0", "")
    link = item.xpath("./a/@href")
    if re.search(r'\bru\b', link[0]):
        pass
    else:
        link[0] = 'https://lenta.ru' + link[0]
    response_link = requests.get(link[0])
    dom2 = html.fromstring(response_link.text)
    date = dom2.xpath("//div[@class='b-topic__info']/time[@datetime]/@datetime")
    if date == []:
        date = dom2.xpath("//div[@class='jsx-149585235 jsx-932351741 time']/text()")
    news['name'] = name
    news['text'] = text
    text = []
    news['link'] = link
    news['data'] = date
    lenta.append(news)
pprint(lenta)
