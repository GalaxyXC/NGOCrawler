import os

import scrapy

OUTPUT_DIR = "crawled/"
REQUEST_PART1 = "http://cishan.chinanpo.gov.cn/biz/ma/csmh/e/csmhedoSort.html?aafx0103=&field=aafx0104&sort=desc&pageNo="
MAX_PAGE = 9
START_PAGE = 1

class TrustUrlSpider(scrapy.Spider):
    name = "trust_urls"
    start_urls = [REQUEST_PART1+str(i+START_PAGE) for i in range(MAX_PAGE)]

    def parse(self, response):
        n_records = len(response.xpath("//a"))
        codes_parsed = response.xpath("//a/text()").extract()
        url_parsed = response.xpath("//a/@href").extract()

        assert len(codes_parsed) == len(url_parsed), "Length of urls and org's did not match."

        print(f'{n_records} records parsed.')

        org_codes = []
        org_urls = []
        for i in range(0, n_records, 1):
            code = codes_parsed[i]
            self.log(f"name is {code.strip()}")
            org_codes.append(codes_parsed[i])
            org_urls.append(url_parsed[i].split('\r')[0])

        if not org_codes and not org_urls:
            print("WARNING: Crawled nothing.")
        else:
            filename = OUTPUT_DIR + 'URLs_to_crawl.csv'
            with open(filename, 'a', encoding='utf-8') as f:
                for line in range(len(org_codes)):
                    f.write(org_codes[line].strip() + ",")
                    f.write(org_urls[line] + "\n")
                f.write("-,-\n")

            self.log('Saved file %s' % filename)