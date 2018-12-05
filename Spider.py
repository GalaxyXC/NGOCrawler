import os
from lxml import html    #这里我们用lxml，也就是xpath的方法
import psycopg2

__procedure__ = \
"""
1. setup conn. to db

2. setup phantomJS etc. to simulate click

3. prepare "visited" list

4. for i in range(total_pge)
        crawl page -> parse ngo email
        sim click 'next page'
        

"""

conn = psycopg2.connect(database="db0", user="postgres", password="AquaMod1s", host="127.0.0.1", port="5432")