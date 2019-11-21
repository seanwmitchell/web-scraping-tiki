from flask import Flask, render_template
import psycopg2
from psycopg2 import sql
from db_admin import setup_db
from scrapping import new_scrap

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():

    # setup_db()
    # new_scrap()

    # we access the products from the database
    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    final_products = cur.fetchall()
    conn.close()

    # returning the html with our list of products
    return render_template('index.html', final_products=final_products)

if __name__ == '__main__':
    app.run(debug=True)