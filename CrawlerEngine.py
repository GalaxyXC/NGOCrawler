import os
import json
from lxml import html    #这里我们用lxml，也就是xpath的方法
import psycopg2

import config as cfg

__procedure__ = \
"""
1. setup conn. to db

3. prepare "visited" list

4. for i in range(total_pge)
        crawl page -> parse ngo email
        sim click 'next page'
"""


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

    def create_job_queue(self, max_page, conn):
        cursor = conn.cursor()

        sql_count_row = "SELECT COUNT(*) FROM basic_info;"
        cursor.execute(sql_count_row)
        count_row = cursor.fetchone()

        sql_existing = "SELECT credit_id FROM basic_info;"
        cursor.execute(sql_existing)
        existing_org_ids = set(cursor.fetchmany(count_row))

        job_queue = []

        for i in range(max_page):
            full_request = cfg.REQUEST_PART1 + str(i+1)
            orgs, urls = NGOUrlSpider(full_request)  # TODO call spider parsing $max_page
            for i in range(len(orgs)):
                if orgs[i] in existing_org_ids:
                    continue
                else:
                    job_queue.append(urls[i])

        cursor.close()
        return job_queue

    def crawl_basic_info(self, job_queue, conn,
                         checkpoint=50):
        q = job_queue
        cur = conn.cursor()
        task_count = 0
        while q:
            url = q.pop()
            try:
                data = parse_url(url) # TODO need parser here
                sql_insert = """INSERT INTO basic_info
                                VALUES (?)
                """
                cur.execute(sql_insert, data)
            except:
                print("Fail to retrieve: ", url)
                continue

            task_count += 1
            if task_count % checkpoint == 0:
                conn.commit()

        cur.close()
        return task_count

    def inDatabase(self, conn, ):\
        pass

    def disconnect(self, conn):
        conn.close()

if __name__ == '__main__':
    engine = CrawlerEngine()
    conn = engine.connect()
    # engine.create_table_basic_info(conn)




    engine.disconnect(conn)