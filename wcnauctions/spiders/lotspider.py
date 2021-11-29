import scrapy
from wcnauctions.items import WcnauctionsItem
from scrapy.loader import ItemLoader

class LotSpider(scrapy.Spider):
    name = 'lot'
    start_urls = ['https://wcn.pl/eauctions/%d' %(n+7) for n in range(210701, 211125)]

    def parse(self, response):
        #item = WcnauctionsItem()
        for lot in response.css('table.items tbody > tr'):
            l = ItemLoader(item = WcnauctionsItem(), selector=lot)

            coinName = lot.css('td:nth-child(2) a::text').get().split(',',maxsplit=2)[1]
            l.add_value('name', coinName)

            coinCat = lot.css('td:nth-child(2) a::text').get().split(',',maxsplit=2)[0]
            l.add_value('category', coinCat)

            l.add_css('condition', 'td:nth-child(3)')
            l.add_css('price', 'td:nth-child(4) p:first-child')
            l.add_css('est_price', 'td:nth-child(4) p:nth-child(2)')
            l.add_css('bids', 'td:nth-child(5)')
            l.add_css('views', 'td:nth-child(4) p:last-child')
            #l.add_css('photoUrl', 'td:first-child a::attr(href)')
            #l.add_css('link', 'td:nth-child(2) a::attr(href)')

            photoUrl = lot.css('td:nth-child(2) a::attr(href)').get()
            l.add_value('photoUrl', 'https:/'+photoUrl)

            fullUrl = lot.css('td:nth-child(2) a::attr(href)').get()
            l.add_value('link', 'https://wcn.pl'+fullUrl)

            yield l.load_item()

        next_page = response.css("#content .pagination a[rel='next']").attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)