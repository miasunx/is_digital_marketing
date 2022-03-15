import scrapy
from scrapy import Request

class GetquotesSpider(scrapy.Spider):
    name = 'getquotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        
        # go to each wrapper, retrieve the info
        for quote in quotes:
            author = quote.xpath('span/small[@class="author"]/text()').extract_first()
            text = quote.xpath('span[@class="text"]/text()').extract_first()[1:-1] # remove " "
            tag = quote.xpath('div[@class="tags"]/meta/@content').extract_first()
            rel_url = quote.xpath('span/a/@href').extract_first()
            abs_url = response.urljoin(rel_url)
            
            yield Request(abs_url, callback=self.parse_page, dont_filter=True,
                          meta={'Author': author, 'Text': text, 'Tag': tag, 'URL': abs_url})
            
        rel_next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        abs_next_url = response.urljoin(rel_next_url)
        
        yield Request(abs_next_url, callback=self.parse)
        
    def parse_page(self, response):
        birth = response.xpath('//span[@class="author-born-date"]/text()').extract_first()
        place = response.xpath('//span[@class="author-born-location"]/text()').extract_first()
        desc = response.xpath('//div[@class="author-description"]/text()').extract_first().strip()
        author = response.meta['Author']
        text = response.meta.get('Text')
        tag = response.meta.get('Tag')
        url = response.meta['URL']
        
        yield {'Author': author, 'Text': text, 'Tag': tag, 'URL': url, 'Birthday': birth,
              'Birth Place': place, 'Description': desc}
        
        
        
        
        
        