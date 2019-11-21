from bs4 import BeautifulSoup
import requests
import psycopg2
from psycopg2 import sql


def new_scrap():
    # using request we ingest the html
    try:
        BASE_URL = 'https://tiki.vn/dien-thoai-may-tinh-bang/'
        response = requests.get(BASE_URL)
    except Exception as err:
        print(f'ERROR: {err}')

    # we use the beautifulSoup library to parse the HTML
    soup = BeautifulSoup(response.text, features="html.parser")

    # we specify the object from within the HTML
    products = soup.find_all('div', class_='product-item')

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()

    # we parse the content and insert it into the database
    for i in range(len(products)):
        data = [
            products[i].find('p', class_='title').text.replace("...", "").replace(" - ", "").strip(), 
            products[i].img['data-src'],
            products[i].find('span', class_='final-price').next.strip(),
            products[i].a['href'],
            str(int(str(products[i].find('span', class_='rating-content').span["style"]).replace("width:", "").replace("%", ""))//20),
            products[i].find('span', class_='sale-tag sale-tag-square').next,
            str(len(products[i].find_all('i', class_='tikicon icon-tikinow')) > 0),
            products[i].find('p', class_='review').string,
            BASE_URL.replace("https://tiki.vn/", "").replace("/", "").replace("-", " ").capitalize()
            ]
        query = "INSERT INTO products(title, images, price, url, rating, discount, tikinow, comments, category) VALUES('" + "', '".join(data) + "')"
        cur.execute(query.format(sql.Identifier('sean_tiki')))
        conn.commit()
    
    cur.close()