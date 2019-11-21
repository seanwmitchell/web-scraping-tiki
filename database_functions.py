import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def db_setup():
    try:
        conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
        cur = conn.cursor()
        cur.execute('SELECT email FROM students')
        conn.close()
        print("Database is already setup")
    except:
        conn = psycopg2.connect("dbname=postgres user=seanm password=")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE sean_tiki").format(
        sql.Identifier('sean_tiki'))
        )
        print("Database has just been setup.")

db_setup()