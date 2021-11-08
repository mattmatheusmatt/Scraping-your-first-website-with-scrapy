import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        title = response.xpath('//h3/a/@title').getall()
        price = response.xpath('//p[@class="price_color"]/text()').getall()

        books = zip(title,price)

        for book in books:
            yield {
                'title':book[0],
                'price':book[1]
            }

        button = response.xpath('//li[@class="next"]/a/@href').get()

        if button:
            new_link = f'https://books.toscrape.com/catalogue/{button}'
            yield scrapy.Request(url = new_link,callback = self.parse)