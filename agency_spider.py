import scrapy

class AgencySpiderSpider(scrapy.Spider):
    name = 'agency_spider'
    allowed_domains = ['agencyspotter.com']
    start_urls = ['https://www.agencyspotter.com/top/design-agencies']

    def parse(self, response):
        cards_of_agencies = response.xpath('//*[@id="top-agencies"]/li').getall()
        # (//h3[@class ='agency-name'] / a / text())[1]
        for i in range(1, (len(cards_of_agencies) + 1)):
            name = response.xpath(f"(//h3[@class='agency-name']/a/text())[{i}]").get()
            domain = response.xpath(f"(//a[@class='primary-action connect-website-report']/@href)[{i}]").get()
            size = response.xpath(f'(//*[@id="top-agencies"]/li/section/div[1]/ul/li[2]/text())[{i}]').get()
            location = response.xpath(f'(//*[@id="top-agencies"]/li/section/div[1]/ul/li[1]/text())[{i}]').get()

            yield {
                'name': name,
                'domain': domain,
                'location': location,
                'size': size
            }


# scrapy crawl agency_spider -o design.csv

