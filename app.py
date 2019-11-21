from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__, static_url_path='/static')

def get_connection():
    connection = psycopg2.connect(user = "seanm",
                                  password = '',
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "tiki")
    return connection

@app.route('/')
def index():

    #using request we ingest the html
    try:
        BASE_URL = 'https://tiki.vn/dien-thoai-may-tinh-bang/'
        response = requests.get(BASE_URL)
    except Exception as err:
        print(f'ERROR: {err}')

    #we use the beautifulSoup library to parse the HTML
    soup = BeautifulSoup(response.text, features="html.parser")

    #we specify the object from within the HTML
    products = soup.find_all('div', class_='product-item')

    #we create empty columns
    titles, images, prices, urls, ratings, discounts, tikinow, comments, category = [], [], [], [], [], [], [], [], []

    #we parse the content and append into the columns
    for i in range(len(products)):
        titles.append(products[i].find('p', class_='title').text.replace("...", "").replace(" - ", ""))
        images.append(products[i].img['data-src'])
        prices.append(products[i].find('span', class_='final-price').next)
        urls.append(products[i].a['href'])
        ratings.append(int(str(products[i].find('span', class_='rating-content').span["style"]).replace("width:", "").replace("%", ""))//20)
        discounts.append(products[i].find('span', class_='sale-tag sale-tag-square').next)
        tikinow.append(len(products[i].find_all('i', class_='tikicon icon-tikinow')) > 0)
        comments.append(products[i].find('p', class_='review').string)
        category.append(BASE_URL.replace("https://tiki.vn/","").replace("/","").replace("-"," ").capitalize())

    #we combine the columns
    final_products = list(
        zip(titles, images, prices, urls, ratings, discounts, tikinow, comments, category))

    #returning the html with our list of products
    return render_template('index.html', final_products=final_products)

if __name__ == '__main__':
    app.run(debug=True)