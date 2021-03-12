import scrapy


class LehrteSpider(scrapy.Spider):
    name = 'lehrte'
    allowed_domains = ['klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-lehrte']
    start_urls = ['https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-lehrte/']

    def parse(self, response):
        artikels = response.xpath("//div[@class='list ratinglist']/article")
        for artikel in artikels:
            artikel_title = artikel.xpath(".//header/h2/text()").get()
            time = artikel.xpath(".//time/text()").get()
            komment = artikel.xpath(".//p[@itemprop='reviewBody']/text()").get()
            yield{
                'title':artikel_title,
                'time':time,
                'kommentar':komment
            }
            
        next_page = response.xpath("//a[@class='raquo button']/@href").get()
        if next_page:
            full_link = response.urljoin(next_page)
            # full_link = f"https://www.klinikbewertungen.de{next_page}"
            yield scrapy.Request(url=full_link, callback=self.parse) 
