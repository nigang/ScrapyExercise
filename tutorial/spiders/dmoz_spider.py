import scrapy, re, datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from tutorial.items import AQIItem, LotteryRecordItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)


class AQISpider(scrapy.Spider):
    name = "AQI"
    start_urls = [
        "https://aqicn.org/city/chengdu/us-consulate/cn/"
    ]
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    def start_requests(self):
        return [scrapy.Request("https://aqicn.org/city/chengdu/us-consulate/cn/", headers = self.header, meta={'cookiejar':1}, callback=self.parse)]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        item = AQIItem()
        item['value'] = response.xpath('//*[@id="aqiwgtvalue"]/text()').extract_first()
        updated_time = datetime.datetime.now().strftime("%Y%m%d")
        updated_time = updated_time + " " + re.search(r'\d{2}:\d{2}', response.xpath('//*[@id="aqiwgtutime"]/text()').extract_first()).group(0)
        item['updated_time'] = updated_time
        yield item


class Lottery(CrawlSpider):
    name = "Lottery"
    domain = "http://www.lottery.gov.cn/historykj/"
    start_urls = [
        "http://www.lottery.gov.cn/historykj/history.jspx?_ltype=pls"
    ]
    rules = [
        #Rule(LinkExtractor(allow=('history(_)?([1-3])?\.jspx\?_ltype=pls')), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=('history(_\d{1,})?\.jspx\?_ltype=pls')), callback='parse_page', follow=True),
    ]
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    def parse_page(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        item = LotteryRecordItem()
        table_body = response.xpath('/html/body/div[3]/div[2]/div[2]/table/tbody/tr')
        for line in table_body:
            item['hundred'] = line.xpath('td[2]/text()').extract_first().split()[0]
            item['decade'] = line.xpath('td[2]/text()').extract_first().split()[1]
            item['unit'] = line.xpath('td[2]/text()').extract_first().split()[2]
            item['sales'] = line.xpath('td[10]/text()').extract_first()
            item['date'] = line.xpath('td[11]/text()').extract_first()
            yield item

        #new_url = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div/a[3]/@href').extract()[0]
        #new_url = self.domain + new_url
        #yield scrapy.Request(url=new_url, callback=self.parse_page)


