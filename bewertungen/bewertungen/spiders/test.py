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

            gesamtzufriedenheit = ((review.xpath(".//section/dl/dd/img/@class").get()).split("-"))[1]
            text_gesamtzufriedenheit = review.xpath(".//section/dl/dd/text()").get()

            q_der_beratung = ((review.xpath(".//section/dl/dd[2]/img/@class").get()).split("-"))[1]
            text_q_der_beratung = review.xpath(".//section/dl/dd[2]/text()").get()

            m_behandlung = ((review.xpath(".//section/dl/dd[3]/img/@class").get()).split("-"))[1]
            text_m_behandlung = review.xpath(".//section/dl/dd[3]/text()").get()

            v_und_ableufe = ((review.xpath(".//section/dl/dd[4]/img/@class").get()).split("-"))[1]
            text_v_und_ableufe = review.xpath(".//section/dl/dd[4]/text()").get()

            a_und_gestaltung = ((review.xpath(".//section/dl/dd[5]/img/@class").get()).split("-"))[1]
            text_a_und_gestaltung = review.xpath(".//section/dl/dd[5]/text()").get()

            if (gesamtzufriedenheit=='null'):
                gesamtzufriedenheit='Kein Info'

            if (q_der_beratung=='null'):
                q_der_beratung='Kein Info'

            if (m_behandlung=='null'):
                m_behandlung='Kein Info'

            if (v_und_ableufe=='null'):
                v_und_ableufe='Kein Info'

            if (a_und_gestaltung=='null'):
                a_und_gestaltung='Kein Info'

            pro = review.xpath(".//section[@class='report']/dl/dd[1]/text()").get()
            kontra = review.xpath(".//section[@class='report']/dl/dd[2]/text()").get()
            krankheitsbild = review.xpath(".//section[@class='report']/dl/dd[3]/text()").get()
            erfahrungsbericht = review.xpath(".//section[@class='report']/dl[2]/dd/p/text()").getall()

            

            yield{
                'Name der Klinik':klinik_name,
                'bewertungen':bewertungen.strip(),
                'Title':review_title,
                'Datum der Bewertung':review_date,
                'fachbereich':fachbereich.strip(),
                'Gesamtzufriedenheit':gesamtzufriedenheit,
                'Textuell Gesamtzufriedenheit':text_gesamtzufriedenheit.strip(),
                'Qualität der Beratung':q_der_beratung,
                'Textuell Qualität der Beratung':text_q_der_beratung.strip(),
                'Mediz. Behandlung':m_behandlung,
                'Textuell Mediz. Behandlung':text_m_behandlung.strip(),
                'Verwaltung und Abläufe':v_und_ableufe,
                'Textuell Verwaltung und Abläufe':text_v_und_ableufe.strip(),
                'Ausstattung und Gestaltung':a_und_gestaltung,
                'Textuell Ausstattung und Gestaltung':text_a_und_gestaltung.strip(),
                'Pro':pro,
                'Kontra':kontra,
                'Krankheitsbild':krankheitsbild,
                'Erfahrungsbericht':erfahrungsbericht
                
            }