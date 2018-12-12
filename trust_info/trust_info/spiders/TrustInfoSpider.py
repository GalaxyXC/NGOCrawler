import scrapy

OUTPUT_DIR = "util/"
DOMAIN = "http://cishan.chinanpo.gov.cn"
TEST_URL = "/biz/ma/csmh/e/csmhedetail.html?aafx0101=ff8080816779569f0167962038e9047d"
START_PAGE = 1
MAX_PAGE = 100
with open(r"D:\workspace\NGOCrawler\trust_info\util\URL_QUEUE.csv", 'r') as f:
    URL_STRING = f.read()

class TrustInfoSpider(scrapy.Spider):
    name = "ngo_trust_info"
    start_urls = [DOMAIN + url for url in URL_STRING.split(',')[START_PAGE-1:START_PAGE+MAX_PAGE-1]]

    def parse(self, response):
        info_selectors = response.xpath("//table[@class='djtable']/tbody/tr/td")

        # Change to i%2 == 0 to crawl csv headers, i%2 == 1 for values
        _SELECT = 1
        info_texts = [info_selectors[i].xpath("text()").extract() for i in range(len(info_selectors)) if i%2 == _SELECT]

        info_texts = ["" if not text else text[0].strip().replace("\n", "").replace("\r", "") for text in info_texts]
        if _SELECT:
            info_texts[3] = self.MMDDYYYY_to_date8(info_texts[3])
        print("info_texts: ", info_texts)

        with open(OUTPUT_DIR + "parsed_texts.csv", 'a', encoding='utf-8') as f:
            f.write("|;|".join(info_texts) + "\n")

        self.log('Saved file at trust name: %s' % info_texts[1])

    # Jan 1, 2018  ->  2018-01-01
    def MMDDYYYY_to_date8(self, date_str):
        mapping = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

        MMDD, year = date_str.split(", ")
        month, date = MMDD.split(" ")
        return year + "-" + mapping[month] + "-" + date.zfill(2)