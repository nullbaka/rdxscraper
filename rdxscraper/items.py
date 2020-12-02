import scrapy


class FirstpostItem(scrapy.Item):
    headline = scrapy.Field()
    subtitle = scrapy.Field()
    image_url = scrapy.Field()
    author = scrapy.Field()
    datetime = scrapy.Field()
    text = scrapy.Field()
    links = scrapy.Field()
    tags = scrapy.Field()


class IndianExpressItem(scrapy.Item):
    headline = scrapy.Field()
    subtitle = scrapy.Field()
    subcategory = scrapy.Field()
    image_url = scrapy.Field()
    editor = scrapy.Field()
    datetime = scrapy.Field()
    text = scrapy.Field()
    links = scrapy.Field()
    tags = scrapy.Field()


class TimesOfIndiaItem(scrapy.Item):
    headline = scrapy.Field()
    text = scrapy.Field()
    image_url = scrapy.Field()


class MoneyControlItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    datetime = scrapy.Field()
    text = scrapy.Field()
    links = scrapy.Field()
    tags = scrapy.Field()
