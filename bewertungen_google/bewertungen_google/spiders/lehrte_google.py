import scrapy
from scrapy_splash import SplashRequest


class LehrteGoogleSpider(scrapy.Spider):
    name = 'lehrte_google'
    def start_requests(self):
       url = 'https://www.google.com/maps/place/KRH+Klinikum+Lehrte/@52.3792233,9.9758272,16.13z/data=!4m7!3m6!1s0x0:0xcdad104f265200f7!8m2!3d52.37997!4d9.9836!9m1!1b1'
       yield SplashRequest(url)

    def parse(self, response):
        kommentars = response.xpath("//*[@id='pane']/div/div[1]/div/div/div[3]/div[10]")
        for kommentar in kommentars:
            product = kommentar.xpath(".//div[@class='section-review ripple-container GLOBAL__gm2-body-2']/div/div/div[2]/text()").get()
            yield{
            'product': product
            }
            
