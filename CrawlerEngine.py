import os
import json

import psycopg2

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

    # Generate a csv file with existing credit_id's from DB
    def _prepare_job_queue(self, conn):
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

    def _prepare_url_queue(self, folder, prefix):
        file_list = os.listdir(folder)
        url_files = [f for f in file_list if f.startswith(prefix)]
        url_queue = []

        for url_file in url_files:
            with open(folder + url_file, 'r') as f:
                text = f.readlines()
                for line in text:
                    url = line.split(', ')[1]
                    url_queue.append(url)

        with open(folder + "URL_QUEUE.csv", 'w') as f:
            f.write(",".join(url_queue))

        return url_queue

    def disconnect(self, conn):
        conn.close()

if __name__ == '__main__':
    engine = CrawlerEngine()
    # conn = engine.connect()
    # engine.create_table_basic_info(conn)
    # Use pgAdmin4 to import existing data into DB
    # queue = engine._prepare_job_queue(conn)

    urls = engine._prepare_url_queue(JOB_QUEUE_OUTPUT_DIR, "URLs_to_crawl_")
    # engine.disconnect(conn)