import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_db():
    conn = psycopg2.connect("dbname=postgres user=seanm password=")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE DATABASE sean_tiki\
            ").format(sql.Identifier('sean_tiki')))
    print("***** sean_tiki database is setup now.")
    conn.close()
    create_products_table()
    create_categories_table()

def create_products_table():
    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE TABLE products(\
        product_id serial PRIMARY KEY,\
        title VARCHAR NOT NULL,\
        images VARCHAR NOT NULL,\
        price VARCHAR NOT NULL,\
        url VARCHAR NOT NULL,\
        rating VARCHAR NOT NULL,\
        discount VARCHAR NOT NULL,\
        tikinow BOOLEAN,\
        comments VARCHAR NOT NULL,\
        category VARCHAR NOT NULL\
        ); ").format(sql.Identifier('sean_tiki')))
    print("***** products tables is setup now.")
    conn.close()

def create_categories_table():
    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE TABLE categories(\
        category_id serial PRIMARY KEY,\
        name VARCHAR(150) NOT NULL\
        ); ").format(sql.Identifier('sean_tiki')))
    print("***** categories tables is setup now.")
    conn.close()