# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars = {}

    # Gathering the Pictures of Mars
    browser.visit('https://spaceimages-mars.com/')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    pic = soup.find('a',class_='fancybox-thumbs',href=True)
    mars['pic0'] = 'https://spaceimages-mars.com/'+pic['href']


    #gathering data for title headline and teaser paragraph
    browser.visit('https://redplanetscience.com/')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', 'content_title')
    para = soup.find_all('div', 'article_teaser_body')
    mars['title'] = title[0].text
    mars['para'] = para[0].text

    #gathering Mars Facts and Creating Table
    browser.visit('https://space-facts.com/mars/')
    html = browser.html
    table = pd.read_html(html)
    facts_df = table[0]
    facts_df.columns =['Description', 'Value']
    mars['marsdf'] = facts_df.to_html('mars_facts_table.html', index=False)

    #Gathering Mars Hemisphere data
    #1
    browser.visit('https://marshemispheres.com/cerberus.html')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    srcs = soup.find_all('img', 'wide-image')
    title = soup.find('h2', 'title').text
    for img in srcs:
        if img.has_attr('src'):
            mars['titlepic1'] = title 
            mars['urlpic1'] = 'https://marshemispheres.com/'+img['src']
            
    #2
    browser.visit('https://marshemispheres.com/schiaparelli.html')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    srcs = soup.find_all('img', 'wide-image')
    title = soup.find('h2', 'title').text
    for img in srcs:
        if img.has_attr('src'):
            mars['titlepic2'] = title 
            mars['urlpic2'] = 'https://marshemispheres.com/'+img['src']
    #3
    browser.visit('https://marshemispheres.com/syrtis.html')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    srcs = soup.find_all('img', 'wide-image')
    title = soup.find('h2', 'title').text
    for img in srcs:
        if img.has_attr('src'):
            mars['titlepic3'] = title 
            mars['urlpic3'] = 'https://marshemispheres.com/'+img['src']
    #4
    browser.visit('https://marshemispheres.com/valles.html')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    srcs = soup.find_all('img', 'wide-image')
    title = soup.find('h2', 'title').text
    for img in srcs:
        if img.has_attr('src'):
            mars['titlepic4'] = title 
            mars['urlpic4'] = 'https://marshemispheres.com/'+img['src']

    from pymongo import MongoClient, collection
    client = MongoClient('localhost', 27017)
    db = client.marsdb
    db.mars.drop()
    db.mars.insert_one(mars)
    return mars