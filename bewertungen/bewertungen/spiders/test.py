import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['klinikbewertungen.de']
    start_urls = ['https://www.klinikbewertungen.de/klinik-forum/erfahrung-mit-krankenhaus-marienstift-braunschweig']

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

            gesamtzufriedenheit = review.xpath(".//section/dl/dd/img/@class").get()
            text_gesamtzufriedenheit = review.xpath(".//section/dl/dd/text()").get()

            if gesamtzufriedenheit:
                gesamtzufriedenheit = (gesamtzufriedenheit.split("-"))[1]
                text_gesamtzufriedenheit = text_gesamtzufriedenheit
            else:
                gesamtzufriedenheit = 'Kein Info'
                text_gesamtzufriedenheit = 'Kein Info'

            q_der_beratung = review.xpath(".//section/dl/dd[2]/img/@class").get()
            text_q_der_beratung = review.xpath(".//section/dl/dd[2]/text()").get()

            if q_der_beratung:
                q_der_beratung = (q_der_beratung.split("-"))[1]
                text_q_der_beratung = text_q_der_beratung
            else:
                q_der_beratung = 'Kein Info'
                text_q_der_beratung = 'Kein Info'

            m_behandlung = review.xpath(".//section/dl/dd[3]/img/@class").get()
            text_m_behandlung = review.xpath(".//section/dl/dd[3]/text()").get()

            if m_behandlung:
                m_behandlung = (m_behandlung.split("-"))[1]
                text_m_behandlung = text_m_behandlung
            else:
                m_behandlung = 'Kein Info'
                text_m_behandlung = 'Kein Info'

            v_und_ableufe = review.xpath(".//section/dl/dd[4]/img/@class").get()
            text_v_und_ableufe = review.xpath(".//section/dl/dd[4]/text()").get()

            if v_und_ableufe:
                v_und_ableufe = (v_und_ableufe.split("-"))[1]
                text_v_und_ableufe = text_v_und_ableufe
            else:
                v_und_ableufe = 'Kein Info'
                text_v_und_ableufe = 'Kein Info'

            a_und_gestaltung = review.xpath(".//section/dl/dd[5]/img/@class").get()
            text_a_und_gestaltung = review.xpath(".//section/dl/dd[5]/text()").get()

            
            if a_und_gestaltung:
                a_und_gestaltung = (a_und_gestaltung.split("-"))[1]
                text_a_und_gestaltung = text_a_und_gestaltung
            else:
                a_und_gestaltung = 'Kein Info'
                text_a_und_gestaltung = 'Kein Info'


            pro = review.xpath(".//section[@class='report']/dl/dd[1]/text()").get()
            kontra = review.xpath(".//section[@class='report']/dl/dd[2]/text()").get()
            krankheitsbild = review.xpath(".//section[@class='report']/dl/dd[3]/text()").get()
            privatpatient = review.xpath(".//section[@class='report']/dl/dd[4]/text()").get()
            erfahrungsbericht = review.xpath(".//section[@class='report']/dl[2]/dd/p/text()").get()

            nutzer = 'Kein Info'
                        
            if review.xpath(".//div[@class='meta']/span[@itemprop='author']/text()").get():
                nutzer = review.xpath(".//div[@class='meta']/span[@itemprop='author']/text()").get()
            elif review.xpath(".//div[@class='meta']/a/span[@itemprop='author']/text()").get():
                nutzer = review.xpath(".//div[@class='meta']/a/span[@itemprop='author']/text()").get()

            meta = review.xpath(".//div[@class='meta']/text()").getall()
            berichtet_als = (((meta[2].strip()).split('|'))[0]).strip()
            behandlungsjahr = (((meta[2].strip()).split('|'))[1]).strip()

            daumen = 'Kein Info'
            if review.xpath(".//img[@class='js-tooltip']").get():
                daumen = ((review.xpath(".//img[@class='js-tooltip']/@src").get()).split('/'))[4]
                if daumen == 'icon-recommend-me-fill.png':
                    daumen = 'Daumen hoch'
                else:
                    daumen = 'Daumen runter'
            

            

            #print((((xx[2].strip()).split('|')[0])).strip())

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
                'Privatpatient':privatpatient,
                'Erfahrungsbericht':erfahrungsbericht,
                'Nutzername':nutzer,
                'Berichtet als':berichtet_als,
                'Behandlungsjahr':behandlungsjahr,
                'Daumen':daumen
                
            }