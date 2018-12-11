import os
import re

import scrapy

OUTPUT_DIR = "crawled/"
DOMAIN = "http://cishan.chinanpo.gov.cn"
TEST_URL = "/biz/ma/csmh/a/csmhadetail.html?aaee0101=ff8080816779569f0167958e8b03042c"
START_PAGE = 1
MAX_PAGE = 350
with open("D:/workspace/NGOCrawler/ngo/crawled/URL_QUEUE.csv", 'r') as f:
    URL_STRING = f.read()

class QuotesSpider(scrapy.Spider):
    name = "ngo_basic_info"
    start_urls = [DOMAIN + url for url in URL_STRING.split('\n,')[START_PAGE-1:START_PAGE+MAX_PAGE-1]]

    def parse(self, response):
        info_elements = response.xpath("//table[@class='djtable']/tbody/tr/td").extract()
        # Change to i%2 == 0 to crawl csv headers, i%2 == 1 for values
        info_values_elements = [info_elements[i] for i in range(len(info_elements)) if i%2 == 1]
        # remove tags
        pattern = re.compile("<[/]*td[ \w=\"]*>")
        info_values_text = [re.sub(pattern, "", info_values_elements[i]) for i in range(len(info_values_elements))]

        with open(OUTPUT_DIR + "parsed_texts.csv", 'a', encoding='utf-8') as f:
            f.write("|;|".join(info_values_text) + "\n")

        self.log('Saved file at credit_id: %s' % info_values_text[1])