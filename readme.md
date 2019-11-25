# Sean's week two project

### Intro:

My name is Sean Mitchell. I am an adult student at a coding bootcamp in Vietnam.

I'm originally from New Zealand and run my own business in technology. Connect with me on Linkedin [here](linkedin.com/in/seanwmitchell/).

The institute is [CoderSchool](https://www.coderschool.vn/en/) in Ho Chi Minh city (Saigon).

The course is 3 months long and focused on Artficial Intelligence and Machine Learning. More info [here](https://bootcamp.coderschool.vn/ml/)

### This project

This project relates to our second week on the course. It brings together all the concepts we learnt in the last week.

This week we learnt:
+ Sort algorithms
+ Object orientated programming
+ Regex and string manipulation
+ Relational database concepts
+ The SQL language and PostgreSQL database

### Technologies used

The project is written in :snake: Python.

The following libraries were used:
+ Flask
    + A commonly used Python library to serve dynamic web applications.
+ Datetime
    + A built in Python library that we used in the project to calculate a delta. Which is the time difference between two timestamps.
+ Requests
    + A Python library that downloads a file from the internet over the http or https protocol. In this project we used it to download a HTML file into memory.
+ BeautifulSoup
    + A Python library that can parse through complex documents or code, like an XML or HTML file for content. This content can then be used in code or saved into a database for later use.
+ Psycopg2
    + A library in Python that is used to connect to a PostgreSQL database.

### Project requirements

+ Create a PostGresSQL database. :white_check_mark:
+ Make a function to connect to your database. :white_check_mark:
+ Create table to store your data, please remember that the number of columns in your table should fit with the shape of your data. Otherwise there would be information mismatch problems. :white_check_mark:
+ Make a function to crawl the link of the categories and return a list of category URLs. :white_check_mark:
+ Your main function should be able to do the following things:
    + Take in two inputs: the list of category URLs and number of pages. :white_check_mark:
    + Loop through the catergory urls list. :white_check_mark:
    + In each loop, extract data in each page, until there is no data left or reached the predefined number of pages. :white_check_mark:
    + Repeat until you have go through every category URLs in the list. :white_check_mark:
    + The extracted data should be transfered directly to your database. :white_check_mark:
+ Finally, use the data from your database to make analysis about Tiki. Be Creative! :white_check_mark:
