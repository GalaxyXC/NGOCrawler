import os
import json
from lxml import html    #这里我们用lxml，也就是xpath的方法
import psycopg2

from config import BASE_FILE, REQUEST_PART1

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
            self.config = json.load(f)

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
        cur = conn.cursor()

        sql_create_table = """CREATE TABLE IF NOT EXISTS basic_info(
                                name            TEXT    NOT NULL,    
                                credit_id       VARCHAR(30) NOT NULL UNIQUE PRIMARY KEY, 
                                found_date      DATE,    
                                registered_at   TEXT,   
                                tax_exempt      BOOLEAN, 
                                tax_exempt_date DATE,    
                                fundraising     BOOLEAN, 
                                approval_date   DATE,    
                                address         TEXT,    
                                executive       TEXT,    
                                org_description TEXT,    
                                email           TEXT,    
                                website         TEXT,    
                                fax             VARCHAR(15), 
                                telephone       VARCHAR(15)
        );"""
        cur.execute(sql_create_table)
        conn.commit()

        cur.close()

    def populate(self):
        with open(BASE_FILE, 'r', encoding="UTF-8") as f:
            existing = f.read()

        # populate records into DB

    def create_job_queue(self, max_page, conn):
        job_queue = []
        cur = conn.cursor()

        # TODO finish logic here
        for i in range(max_page):
            full_request = REQUEST_PART1 + str(i+1)
            organizations = crawl_and_parse(full_request) #TODO (need another parser)
            for org.id in organizations:
                sql_search = """
                """

                cur.execute(sql_search)
                exist = cur.fetchone

                if not exist:
                    job_queue.append(org.href)

        conn.commit()
        cur.close()
        return job_queue

    def crawl_basic_info(self, job_queue, conn,
                         checkpoint=50):
        q = job_queue
        cur = conn.cursor()
        task_count = 0
        while q:
            url = q.pop()
            try:
                response = parse_url(url) # TODO need parser here
                sql_insert = """
                """


                cur.execute(sql_insert)
            except:
                print("Fail to retrieve: ", url)
                continue
            
            task_count += 1
            if task_count % checkpoint == 0:
                conn.commit()

        cur.close()
        return task_count



    def disconnect(self):
        conn.close()

if __name__ == '__main__':
    engine = CrawlerEngine()
    conn = engine.connect()
    # engine.create_table_basic_info(conn)




    engine.disconnect(conn)