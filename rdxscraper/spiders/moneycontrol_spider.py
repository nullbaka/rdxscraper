import scrapy
from w3lib.html import remove_tags
from unidecode import unidecode
from ..items import MoneyControlItem
from twisted.internet.defer import Deferred


class MoneyControlSpider(scrapy.Spider):
    name = "moneycontrol"
    custom_settings = {
        'ITEM_PIPELINES': {
            'rdxscraper.pipelines.MoneyControlPipeline': 300,
        }
    }

    def __init__(self, category=None, pages=5, *args, **kwargs):
        super(MoneyControlSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.pages = int(pages)
        if category=="mutual-funds":
            self.scrape_url = ["https://www.moneycontrol.com/news/business/mutual-funds/"]
        elif category=="markets":
            self.scrape_url = ["https://www.moneycontrol.com/news/business/markets/"]
        elif category==None:
            self.scrape_url = ["https://www.moneycontrol.com/news/business/mutual-funds/",
                               "https://www.moneycontrol.com/news/business/markets/"]
        else:
            print("----------Category not supported----------")
            Deferred()

    def start_requests(self):
        for url in self.scrape_url:
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(base_url=url, page=''))

    def parse(self, response, base_url, page):
        if page=='':
            page = str(2)
        elif int(page) > self.pages - 1:
            return
        else:
            page = str(int(page)+1)
        if response.status != 404:
            for news in response.css('#left ul li h2 a::attr(href)'):
                url = news.get()
                a = url.split('/')
                if a[-2]=='mutual-funds' or a[-2]=='markets':
                    yield scrapy.Request(url=url, callback=self.parse_news)
            next_page = base_url+'page-'+str(page)
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=dict(base_url=base_url, page=page))

    def parse_news(self, response):
        text = [p.get() for p in response.css(".content_wrapper p")]
        text = unidecode(remove_tags(' '.join(text)))
        datetime = response.css('.article_schedule::text').get()
        try:
            datetime = datetime.strip()
        except:
            pass
        data = {
            "title": response.css('.article_title::text').get(),
            "description": response.css('.article_desc::text').get(),
            "datetime": datetime,
            "text": text,
            "links": [link.get() for link in response.css(".content_wrapper p a::attr(href)")],
            "tags": [tag.get().replace('#','') for tag in response.css('.tags_first_line a::text')]
        }
        item = MoneyControlItem(data)
        yield item
