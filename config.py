import json

# Create config.json file


# postgreSQL
psql = {}
psql["database"] = "ngo_cn"
psql["user"] = "admin"
psql["password"] = "AquaMod1s"
psql["host"] = "127.0.0.1" # localhost
psql["post"] = "5432"
# database="db0", user="postgres", password="AquaMod1s", host="127.0.0.1", port="5432"

# Directories & Paths

BASE_FILE = "original_files/3_orig.csv"
REQUEST_PART1 = "http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaDoSort.html?aaee0102_03=&field=aaee0103&sort=desc&flag=0&pageNo="
# http://www.networkinghowtos.com/howto/common-user-agent-list/
USER_AGENT_STRINGS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
                      "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                      "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
                      "Wget/1.15 (linux-gnu)"
                      ]








config = {}
config['psql'] = psql

with open("config.json", 'w') as f:
    json.dump(config, f)

# Sample json converting ocdes:
# import json
# dict to string: s = json.dumps(dct)
# string to JSON: j = json.loads(s)