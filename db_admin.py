# Libraries to import for database access

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def db_check():

    # a function to check if we have the database established already. If no, call the setup functions.

    try:
        conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
        conn.close()
    except:
        create_database()
        create_categories_table()
        create_sub_categories_table()
        create_products_table()

def create_database():

    # a function to initially establish the database

    conn = psycopg2.connect("dbname=postgres user=seanm password=")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE DATABASE sean_tiki\
            ").format(sql.Identifier('sean_tiki')))
    conn.close()
    print("***** database setup.")

def create_categories_table():

    # a function to create the categories table in the new db

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql.SQL("""CREATE TABLE categories(
            cat_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""))
    conn.close()
    print("***** categories table setup.")

def create_sub_categories_table():

    # a function to create the sub categories table in the new db

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql.SQL("""CREATE TABLE sub_categories(
            sub_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            url TEXT,
            parent_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""))
    conn.close()
    print("***** sub categories table setup.")

def create_products_table():

    # a function to create the products table in the new db

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql.SQL("""CREATE TABLE products(
        product_id serial PRIMARY KEY,
        title VARCHAR UNIQUE NOT NULL,
        image VARCHAR NOT NULL,
        price INTEGER NOT NULL,
        url VARCHAR NOT NULL,
        rating SMALLINT NOT NULL,
        discount SMALLINT NOT NULL,
        tikinow BOOLEAN,
        comments VARCHAR NOT NULL,
        sub_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ); """).format(sql.Identifier('sean_tiki')))
    conn.close()
    print("***** products table setup.")