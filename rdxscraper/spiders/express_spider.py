import scrapy
from ..items import IndianExpressItem
from twisted.internet.defer import Deferred


class IndianExpressSpider(scrapy.Spider):
    name = "indianexpress"
    custom_settings = {
        'ITEM_PIPELINES': {
            'rdxscraper.pipelines.ExpressPipeline': 300,
        }
    }

    def __init__(self, category="all", *args, **kwargs):
        super(IndianExpressSpider, self).__init__(*args, **kwargs)
        self.category = category
        if category in ('business', 'sports'):
            self.start_urls = [
                f"https://indianexpress.com/section/{category}/",
            ]
        elif category=='news':
            self.start_urls = [
                "https://indianexpress.com/section/india/",
                "https://indianexpress.com/section/cities/",
            ]
        elif category=='all':
            self.start_urls = [
                "https://indianexpress.com/section/india/",
                "https://indianexpress.com/section/cities/",
                "https://indianexpress.com/section/business/",
                "https://indianexpress.com/section/sports/",
            ]
        else:
            print("----------Category not supported----------")
            Deferred()

    def parse(self, response):
        for post in response.css(".title"):
            url = post.css("a::attr(href)").get()
            yield scrapy.Request(url=url, callback=self.parse_article)

        next_page = response.css('.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_article(self, response):
        text = [p.get() for p in response.css('.full-details p::text')]
        text.pop()
        text.pop()
        text = ' '.join(text)
        links = [link.get() for link in response.css('.full-details p a::attr(href)')]
        links.pop()
        links.pop()
        links.pop()
        subcategory = response.url.split('/')[-3]
        data = {
            "headline": response.css('.native_story_title::text').get(),
            "subtitle": response.css('.synopsis::text').get(),
            "subcategory": subcategory,
            "tags": [tag.get() for tag in response.css('.storytags ul li a::text')],
            "editor": response.css('.editor a::text').get(),
            "datetime": response.css('.editor span::text').get().strip(),
            "text": text,
            "image_url": response.css('.custom-caption img::attr(src)').get(),
            "links": links
        }
        item = IndianExpressItem(data)
        yield item
