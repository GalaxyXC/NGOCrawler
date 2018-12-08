import scrapy

from CrawlerEngine import inDatabase

OUTPUT_DIR = "crawled/"

# TODO Test this crawler
# crawl static contents
class NGOUrlSpider(scrapy.Spider):
    name = "ngo_urls"
    start_urls = ["http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0&pageNo=1"]

    def parse(self, response):
        n_records = len(response.xpath("//a"))
        codes_parsed = response.xpath("//a/text()").extract()
        url_parsed = response.xpath("//a/@href").extract()
        assert len(codes_parsed) == len(url_parsed), "Length of urls and org's did not match."

        org_codes = []
        org_urls = []
        for i in range(n_records):
            if i%2 == 1:
                continue

            code = codes_parsed[i]
            if not inDatabase(code):
                org_codes.append(code)
                org_urls.append(url_parsed[i])

        page = self.start_urls.split('=')[-1]
        filename = OUTPUT_DIR + 'URLs_to_crawl_%s.csv' % page
        with open(filename, 'wb') as f:
            for line in range(len(org_codes)):
                f.write(org_codes[line] + ", ")
                f.write(org_urls[line] + "\n")

        self.log('Saved file %s' % filename)
        return org_codes, org_urls