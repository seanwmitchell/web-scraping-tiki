# libraries for scraping
from bs4 import BeautifulSoup
import requests

# libraries for database connectivity
import psycopg2
from psycopg2 import sql

def scrape_check():

    # a function to check if we need to scrape or not

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()
    cur.execute('SELECT * FROM categories LIMIT 1;')
    if cur.fetchone() == None:

        # If no data exists, then start scraping

        scrape_main_categories()
        scrape_sub_categories()
        scrape_products()
    else:
        print("***** no scrapping needed.")

def parse(url):

    # a commonly used function for using beautiful soup

    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, features="html.parser")
        return response
    except Exception as err:
        print(f'ERROR: {err}')

def scrape_main_categories():

    # a top level category scraping function

    BASEURL = "https://tiki.vn/"

    soup = parse(BASEURL)
    
    for i in soup.findAll('a',{'class':'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        
        cat_id = None
        name = i.find('span',{'class':'text'}).text 
        url = i['href'] + "&page=1"

        query = f"""
            INSERT INTO categories (name, url) 
            VALUES (%s, %s);
        """

        # I decided not to return the saved ID number, as I'm not using it.

        val = (name, url)

        conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
        cur = conn.cursor()
        cur.execute(query, val)
        conn.commit()

    # note - I am closing the database

    cur.close()
    print("***** main categories scraped.")

def scrape_sub_categories():

    # function that gets all main categories and starts the utility function for scraping sub cat

    print("***** starting to scrape sub categories")

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()
    cur.execute('SELECT * FROM categories;')
    categories = cur.fetchall()
    conn.close()
    for category in categories:
        _scrape_sub_categories(category)

    print("***** sub categories scraped.")

def _scrape_sub_categories(category):

    # a utility function for scraping sub categories

    cat_id = category[0]
    name = category[1]
    url = category[2]
    sub_categories = []

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()

    try:
        div_containers = parse(url).find_all('div', attrs={"class": "list-group-item is-child"})
        for div in div_containers:
            name = div.a.text.split('(')[0].strip()
            url = 'https://tiki.vn' + div.a.get('href')
            parent_id = cat_id
                        
            query = f"""
                INSERT INTO sub_categories (name, url, parent_id) 
                VALUES (%s, %s, %s);
            """

            # I decided not to return the saved ID number, as I'm not using it.

            val = (name, url, parent_id)
                
            cur.execute(query, val)
            conn.commit()

    except Exception as err:
        print(f'ERROR: {err}')

    conn.close()

def scrape_products():

    # function that gets all sub categories and starts the utility function for scraping products

    print("***** starting to scrape products")

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()
    cur.execute('SELECT sub_id, url FROM sub_categories;')
    categories = cur.fetchall()
    conn.close()
    for category in categories:
        _scrape_products(category)

    print("***** all products scraped.")


def _scrape_products(category):

    # a utility function for scraping products

    sub_id = category[0]
    url = category[1]

    soup = parse(url)

    products = soup.find_all('div', class_='product-item')

    conn = psycopg2.connect("dbname=sean_tiki user=seanm password=")
    cur = conn.cursor()

    for i in range(len(products)):

        try:
            title = products[i].find('p', class_='title').text.replace("...", "").replace(" - ", "").strip(), 
            image = products[i].img['src'],
            price = products[i].find('span', class_='final-price').next.strip("").replace("đ","").replace(".",""),
            url = products[i].a['href'],
            rating = 4
            # int(str(products[i].find('span', class_='rating-content').span["style"]).replace("width:", "").replace("%", ""))//20,
            discount = products[i].find('span', class_='sale-tag sale-tag-square').next.replace("-","").replace("%",""),
            tikinow = str(len(products[i].find_all('i', class_='tikicon icon-tikinow')) > 0),
            comments = products[i].find('p', class_='review').string,

            query = f"""
                INSERT INTO products (title, image, price, url, rating, discount, tikinow, comments, sub_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # I decided not to return the saved ID number, as I'm not using it.

            val = (title, image, price, url, rating, discount, tikinow, comments, sub_id)
            
            cur.execute(query, val)
            conn.commit()
        except:
            pass
    
    cur.close()
    print("***** category scraped for products.")