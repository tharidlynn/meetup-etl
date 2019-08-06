import os
import psycopg2 
from sql.sql_queries import *

def create_database():

    PG_HOST = os.environ.get('PGHOST')
    PG_USERNAME = os.environ.get('PGUSERNAME')
    PG_PASSWORD = os.environ.get('PGPASSWORD')
    PG_DEFAULT_DATABASE = os.environ.get('PGDEFAULTDATABASE')
    PG_DATABASE = os.environ.get('PGDATABASE')
    
    conn = psycopg2.connect(f'host={PG_HOST} dbname={PG_DEFAULT_DATABASE} user={PG_USERNAME} password={PG_PASSWORD}')
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute('DROP DATABASE IF EXISTS meetup;')
    cur.execute('CREATE DATABASE meetup;')

    conn.close()    
    
    # connect to meetup database
    conn = psycopg2.connect(f'host={PG_HOST} dbname={PG_DATABASE} user={PG_USERNAME} password={PG_PASSWORD}')
    cur = conn.cursor()
    
    return cur, conn


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        print('CREATE TABLE')


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        print('INSERT TABLE')

def main():

    cur, conn = create_database()

    try:
        create_tables(cur, conn)
        insert_tables(cur, conn)
    except psycopg2.Error as e:
        print(e)
        
    conn.close()

if __name__ == '__main__':
    main()
