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









config = {}
config['psql'] = psql

with open("config.json", 'w') as f:
    json.dump(config, f)

# Sample json converting ocdes:
# import json
# dict to string: s = json.dumps(dct)
# string to JSON: j = json.loads(s)