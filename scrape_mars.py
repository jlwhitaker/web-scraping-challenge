#!/usr/bin/env python
# coding: utf-8

# In[36]:


import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from splinter import Browser
import pymongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# In[82]:
def init_browser():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[38]:
def scrape_info():
    browser = init_browser()

    mars_news_url = 'https://redplanetscience.com/#'

    browser.visit(mars_news_url)

    news_html = browser.html

    news_soup = bs(news_html, 'html.parser')


# In[39]:


    results = news_soup.find_all(class_= 'col-md-8')
    result = results[0]


# In[41]:


    news_title = result.find(class_= "content_title")
    print(news_title)


# In[42]:


    news_p = result.find(class_= "article_teaser_body")
    print(news_p)


# # JPL Mars Space Images - Featured Image

# In[83]:


    space_image_url = 'https://spaceimages-mars.com/#'

    browser.visit(space_image_url)

    image_html = browser.html

    image_soup = bs(image_html, 'html.parser')


# In[87]:


    featured_image = image_soup.find("img", class_="headerimage fade-in")["src"]
    print(featured_image)


# In[95]:


    featured_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'


# # Mars Facts

# In[53]:


    mars_facts_url = 'https://galaxyfacts-mars.com/#'

    response = requests.get(mars_facts_url)

    facts_soup = bs(facts_html, 'html.parser')


# In[55]:


    dfs = pd.read_html(mars_facts_url)

    df = dfs[1]

    print(df)


# In[57]:


    mars_facts_table_html = df.to_html()


# # Mars Hemispheres 

# In[90]:


    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)


# In[91]:


    import time 
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')
    hemisphere_image_url=[]


# In[93]:


    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_url.append(dictionary)
        browser.back()


# In[94]:


    print(hemisphere_image_url)


# In[ ]:

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts_table_html': mars_facts_table_html,
        'hemisphere_image_urls' : hemisphere_image_url
    }


     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


