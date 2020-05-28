import psycopg2.pool as pool


db_pool = pool.SimpleConnectionPool(0,5,dbname="Plemiona", user="rafsaf", password="123")

