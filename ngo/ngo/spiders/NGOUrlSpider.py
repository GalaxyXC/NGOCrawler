import os

import scrapy

OUTPUT_DIR = "crawled/"
REQUEST_PART1 = "http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0&pageNo="
MAX_PAGE = 344
START_PAGE = 1
with open(OUTPUT_DIR + "existing_ids.txt", 'r') as f:
    EXISTING_ORG_IDS_STR = f.read()
print(EXISTING_ORG_IDS_STR[:100])

class NGOUrlSpider(scrapy.Spider):
    name = "ngo_urls"
    start_urls = [REQUEST_PART1+str(i+START_PAGE) for i in range(MAX_PAGE)]
    org_ids = set(EXISTING_ORG_IDS_STR.split(','))

    def parse(self, response):
        n_records = len(response.xpath("//a"))
        codes_parsed = response.xpath("//a/text()").extract()
        url_parsed = response.xpath("//a/@href").extract()

        assert len(codes_parsed) == len(url_parsed), "Length of urls and org's did not match."

        print(f'{n_records} records parsed.')

        org_codes = []
        org_urls = []
        for i in range(0, n_records, 2):
            code = codes_parsed[i]
            self.log(f"code is {code}")
            if code not in self.org_ids:
                org_codes.append(codes_parsed[i])
                org_urls.append(url_parsed[i].split('\r')[0])

        if not org_codes and not org_urls:
            print("All code existed in DB from this page")
        else:
            page = len(os.listdir(OUTPUT_DIR))-3  #['existing_id.txt', 'NGOBasic_info_trial', 'static_contents']
            filename = OUTPUT_DIR + 'URLs_to_crawl_%s.csv' % page
            with open(filename, 'w') as f:
                for line in range(len(org_codes)):
                    f.write(org_codes[line] + ", ")
                    f.write(org_urls[line] + "\n")

            self.log('Saved file %s' % filename)