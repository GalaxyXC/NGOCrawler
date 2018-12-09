import os
import json
import time

from lxml import html    #这里我们用lxml，也就是xpath的方法
import psycopg2
import scrapy
from scrapy.crawler import CrawlerProcess

import config as cfg
import ngo.ngo.spiders.NGOUrlSpider as UrlSpider
import ngo_basic_info.ngo_basic_info.spiders.BasicInfoSpider as BasicSpider

JOB_QUEUE_OUTPUT_DIR = "ngo/crawled/"



class CrawlerEngine(object):
    def __init__(self, config="config.json"):
        with open(config, 'r') as f:
            self.config = json.load(f) # stores DB connection arguments

    def connect(self):
        # setup conn. with db
        psql = self.config['psql']

        print('Connecting to the PostgreSQL database...')
        try:
            conn = psycopg2.connect(database=psql['database'],
                                    user=psql['user'],
                                    password=psql['password'],
                                    host=psql['host'],
                                    port=psql['post'])
        except:
            print("psycopg2 Failed to connect to db")
            return None

        return conn

    def create_table_basic_info(self, conn):
        cursor = conn.cursor()

        sql_create_table = """CREATE TABLE IF NOT EXISTS basic_info(
                                name            TEXT    NOT NULL,    
                                credit_id       VARCHAR(30) NOT NULL UNIQUE PRIMARY KEY, 
                                found_date      DATE,    
                                registered_at   TEXT,   
                                tax_exempt      CHAR(8), 
                                tax_exempt_date VARCHAR(30),    
                                fundraising     CHAR(8), 
                                approval_date   DATE,    
                                address         TEXT,    
                                executive       TEXT,    
                                org_description TEXT,    
                                email           TEXT,    
                                website         TEXT,    
                                fax             VARCHAR(30), 
                                telephone       VARCHAR(30)
        );"""
        cursor.execute(sql_create_table)
        conn.commit()

        cursor.close()

    # DEPRECATED: used pgAdmin's import to populate basic_info with 4850 rows from cfg.BASE_FILE
    def __populate(self, conn):
        # sql_import = "COPY sample_table FROM 'path/to/file' DELIMITER ',' CSV HEADER;
        pass

    def prepare_job_queue(self, conn):
        cursor = conn.cursor()

        sql_count_row = "SELECT COUNT(*) FROM basic_info;"
        cursor.execute(sql_count_row)
        count_row = cursor.fetchone()
        print(f"Database now has {count_row[0]} records.")

        sql_existing = "SELECT credit_id FROM basic_info;"
        cursor.execute(sql_existing)
        existing_org_ids = set(cursor.fetchmany(count_row[0]))

        with open(JOB_QUEUE_OUTPUT_DIR + "existing_ids.txt", 'w') as f:
            f.write(",".join([i[0] for i in existing_org_ids]))

        cursor.close()
        return existing_org_ids

    # Deprecated: call spider from command line console
    def crawl_basic_info(self, job_queue):
        q = job_queue
        task_count = 0
        while q:
            url = q.pop()
            try:
                process = CrawlerProcess({
                    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
                })
                process.crawl(BasicSpider)
                process.start()  # the script will block here until the crawling is finished
                time.sleep(2)  # TODO need parser here
                task_count += 1
            except:
                print("Fail to retrieve: ", url)
                continue

            print("Successfully retrived %s records", task_count)
        return task_count

    def disconnect(self, conn):
        conn.close()

if __name__ == '__main__':
    engine = CrawlerEngine()
    conn = engine.connect()
    # engine.create_table_basic_info(conn)
    queue = engine.prepare_job_queue(conn)



    engine.disconnect(conn)