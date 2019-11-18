from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import json
import random

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    try:
        BASE_URL = 'https://tiki.vn/dien-thoai-may-tinh-bang/'
        response = requests.get(BASE_URL)
    except Exception as err:
        print(f'ERROR: {err}')

    soup = BeautifulSoup(response.text, features="html.parser")

    articles = soup.find_all('div', class_='product-item')

    titles, images, prices, urls, ratings, discounts, tikinow, comments, category = [], [], [], [], [], [], [], [], []
    for i in range(len(articles)):
        titles.append(articles[i].find('p', class_='title').text.replace("...", "").replace(" - ", ""))
        images.append(articles[i].img['data-src'])
        prices.append(articles[i].find('span', class_='final-price').next)
        urls.append(articles[i].a['href'])
        ratings.append(int(str(articles[i].find('span', class_='rating-content').span["style"]).replace("width:", "").replace("%", ""))//20)
        discounts.append(articles[i].find('span', class_='sale-tag sale-tag-square').next)
        tikinow.append(len(articles[i].find_all('i', class_='tikicon icon-tikinow')) > 0)
        comments.append(articles[i].find('p', class_='review').string)
        category.append(BASE_URL.replace("https://tiki.vn/","").replace("/","").replace("-"," ").capitalize())

    final_articles = list(
        zip(titles, images, prices, urls, ratings, discounts, tikinow, comments, category))

    return render_template('index.html', final_articles=final_articles)

if __name__ == '__main__':
    app.run(debug=True)