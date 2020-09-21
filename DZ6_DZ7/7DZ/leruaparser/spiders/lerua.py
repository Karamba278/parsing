import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

#https://www.avito.ru/rossiya?q=porsche
class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self,search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&family=00b9b5a0-faeb-11e9-810b-878d0b27ea5b&suggest=true']

    #[f'https://leroymerlin.ru/search/?q={search}&family=00b9b5a0-faeb-11e9-810b-878d0b27ea5b&suggest=true']


    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//uc-plp-item-new/@href")
        for link in ads_links:
            yield response.follow(link, callback= self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(),response=response)
        loader.add_xpath('name',"//h1/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price',"//span[@xpath='1']/text()")
        loader.add_xpath('photo', "//source[@itemprop='image']/@data-origin") #"//picture[@slot='pictures']/@img"
        loader.add_xpath('info_name', '//dt/text()')
        loader.add_xpath('info', '//dd/text()')
        yield loader.load_item()




