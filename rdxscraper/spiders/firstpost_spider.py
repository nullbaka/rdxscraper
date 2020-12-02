import scrapy
from w3lib.html import remove_tags
from unidecode import unidecode
from ..items import FirstpostItem
from twisted.internet.defer import Deferred


class FirstpostSpider(scrapy.Spider):
    name = "firstpost"
    custom_settings = {
        'ITEM_PIPELINES': {
            'rdxscraper.pipelines.FirstpostPipeline': 300,
        }
    }

    def __init__(self, category="all", *args, **kwargs):
        super(FirstpostSpider, self).__init__(*args, **kwargs)
        self.category = category
        if category in ('business', 'sports'):
            self.start_urls = [
                f"https://www.firstpost.com/category/{category}/",
            ]
        elif category=='news':
            self.start_urls = [
                "https://www.firstpost.com/category/india/",
                "https://www.firstpost.com/category/world/",
                "https://www.firstpost.com/category/politics/",
            ]
        elif category=='all':
            self.start_urls = [
                "https://www.firstpost.com/category/india/",
                "https://www.firstpost.com/category/world/",
                "https://www.firstpost.com/category/politics/",
                "https://www.firstpost.com/category/business/",
                "https://www.firstpost.com/category/sports/",
            ]
        else:
            print("----------Category not supported----------")
            Deferred()

    def parse(self, response):
        for post in response.css('.big-thumb'):
            url = post.css('.main-title a::attr(href)').get()
            yield scrapy.Request(url=url, callback=self.parse_article)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        author_info = response.css(".author-info span::text")
        headline = response.css("#headlineitem::text").get()
        if headline is not None:
            headline = headline.strip()
        subtitle = response.css(".inner-copy::text").get()
        if subtitle is not None:
            subtitle = subtitle.strip()
        data = {
            "headline": headline,
            "subtitle": subtitle,
            "image_url": response.css('.article-img img::attr(src)').get(),
            "author": author_info.get().strip(),
            "datetime": author_info[1].get().strip(),
            "text": unidecode(remove_tags(response.css('div.article-full-content').get()).strip()),
            "links": [a.get() for a in response.css('div.article-full-content a::attr(href)')],
            "tags": [tag.get().strip() for tag in response.css('ul.tags-list a::text')]
        }
        item = FirstpostItem(data)
        yield item
