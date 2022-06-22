import scrapy
from scrapy.crawler import CrawlerProcess

def string_cleaner(text):
    if text != None:
        return ("".join(text.strip()).encode('cp860', 'ignore').decode("cp860"))
    else:
        return None

class Spider(scrapy.Spider):
    name = "aeronautas"
    start_urls = ['https://www.aeronautas.org.br/index.php/noticias']

    def parse(self, response):
        for post in response.css('article'):
            yield {
                'titulo': string_cleaner(post.css('header h2 a ::text').extract_first().replace("\n\t\t\t\t", "")),
                'conteudo': string_cleaner(post.css('section p ::text').extract_first()),
                'data': post.css('time::attr(datetime)').extract_first(),
            }
        next_page = response.css('.pagination li a ::attr(href)').extract()
        next_page = next_page[len(next_page) - 2]
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
process = CrawlerProcess(settings={
    "FEEDS": {
        "posts.csv": {"format": "csv"},
    }
})

process.crawl(Spider)
process.start()
