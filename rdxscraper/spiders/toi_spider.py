import scrapy
from w3lib.html import remove_tags
from ..items import TimesOfIndiaItem
from twisted.internet.defer import Deferred


class TimesOfIndiaSpider(scrapy.Spider):
    name = "timesofindia"
    custom_settings = {
        'ITEM_PIPELINES': {
            'rdxscraper.pipelines.TimesOfIndiaPipeline': 300,
        }
    }

    def __init__(self, category="business", pages=5, *args, **kwargs):
        super(TimesOfIndiaSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.pages = int(pages)
        if category=='business':
            self.list_of_urls = [
                "https://timesofindia.indiatimes.com/business/corporate",
                "https://timesofindia.indiatimes.com/business/economy",
                "https://timesofindia.indiatimes.com/business/real-estate",
                "https://timesofindia.indiatimes.com/business/telecom",
                "https://timesofindia.indiatimes.com/business/personal-finance",
                "https://timesofindia.indiatimes.com/business/aviation",
                "https://timesofindia.indiatimes.com/business/india-business",
                "https://timesofindia.indiatimes.com/business/international-business"
            ]
        else:
            print("----------Category not supported----------")
            Deferred()

    def start_requests(self):
        for url in self.list_of_urls:
            yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(base_url=url, page=''))

    def parse(self, response, base_url, page):
        if page == '':
            page='2'
        else:
            if int(page) > self.pages - 1:
                return
            page = str(int(page)+1)
        if response.status != 404:
            for post in response.css("ul.list5 li a::attr(href)"):
                url = post.get()
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse_article)
            url=base_url+'/'+str(page)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(base_url=base_url, page=page))

    def parse_article(self, response):
        data = {
            "headline": response.css('h1::text').get(),
            "text": remove_tags(response.css('.ga-headlines').get()),
            "image_url": response.css('.ga-headlines img::attr(src)').get()
        }
        item = TimesOfIndiaItem(data)
        yield item
