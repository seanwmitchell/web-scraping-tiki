from flask import Flask, render_template
import psycopg2
from psycopg2 import sql
from db_admin import db_check
from scrape_admin import scrape_check
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

def initialise():

    # a quick initialisation function

    db_check()
    scrape_check()

initialise()

@app.route('/')
def index():

    # we access the products and a couple of static fields from the database

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()
    cur.execute('SELECT * FROM products ORDER BY price DESC LIMIT 24;')
    products = cur.fetchall()
    cur.execute('SELECT * FROM products ORDER BY discount DESC LIMIT 1;')
    high_disc_prod = cur.fetchall()
    cur.execute('SELECT name, url FROM categories;')
    categories = cur.fetchall()
    
    cur.execute('SELECT name, url FROM sub_categories;')
    sub_categories = cur.fetchall()

    cat_count = len(categories)
    sub_count = len(sub_categories)
    cur.execute('SELECT COUNT(product_id) FROM products;')
    prod_count = f'{cur.fetchall()[0][0]:,}'
    cur.execute('SELECT min(created_at), max(created_at) FROM products;')
    times = cur.fetchall()
    cur.execute('SELECT AVG(discount) FROM products;')
    avg_disc = round(cur.fetchall()[0][0],0)
    sc_time = (times[0][1] - times[0][0]).seconds
    stats = [cat_count, sub_count, prod_count, sc_time, avg_disc]
    conn.close()

    # returning the html with our data

    return render_template('index.html', products=products, categories=categories, sub_categories=sub_categories, high_disc_prod=high_disc_prod, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)