import scrapy

OUTPUT_DIR = "crawled/"

# crawl static contents
class NGOBasicInfoSpider(scrapy.Spider):
    name = "ngo_basic"

    def start_requests(self):
        urls = [
            "http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0&pageNo=1"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = OUTPUT_DIR + 'NGOBasicInfo_%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)