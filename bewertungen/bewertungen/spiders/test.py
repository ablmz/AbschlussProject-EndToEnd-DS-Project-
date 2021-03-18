import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['klinikbewertungen.de']
    start_urls = ['https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-kreis-und-stadtkrankenhaus-alfeld']

    def parse(self, response):
        next_page = response.xpath("//a[@class='raquo button']/@href").get()
        if next_page:
            full_link = response.urljoin(next_page)
            # full_link = f"https://www.klinikbewertungen.de{next_page}"
            yield scrapy.Request(url=full_link, callback=self.parse) 

        #Fixed Values -one output
        bewertungen = response.xpath("//*[@class='block']/header/h1/text()").get()
        klinik_name = response.xpath("//header/h1/text()").get()

        # Mehr values
        all_reviews = response.xpath("//div[@class='list ratinglist']/article")

        for review in all_reviews:            
            review_title = review.xpath(".//header[@style='float:left;']/h2/text()").get()
            review_date = review.xpath(".//time/text()").get()

            fachbereich = review.xpath(".//span[@class='right']/a/text()").get()
            if fachbereich:
                fachbereich=fachbereich
            else:
                fachbereich = review.xpath(".//span[@class='right']/text()").get()

           
            yield{
                'Name der Klinik':klinik_name,
                'bewertungen':bewertungen.strip(),
                'Title':review_title,
                'Datum der Bewertung':review_date,
                'fachbereich':fachbereich.strip()
            }