
# coding: utf-8

# ## Mission to Mars

# In[47]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from splinter import Browser
import time
import pandas as pd

def scrape():

    # ## Scraping: NASA Mars News

    # In[42]:

    mission_mars_data = {}
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)
    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results_paragraph = soup.find_all('div', class_='image_and_description_container')
    results_title = soup.find_all('div', class_='content_title')

    for result in results_paragraph:
        try:
            news_p = result.find('div', class_='rollover_description_inner').text
            #print(news_p)
            mission_mars_data["news_p"] = news_p

        except Exception as e:
            print(e)


    # In[45]:


    for result in results_title:
        try:
            news_title = result.find('a').text
            #print(news_title)
            mission_mars_data["news_title"] = news_title

        except Exception as e:
            print(e)


    # ## Scraping: JPL Mars Space Images - Featured Image

    # In[93]:


    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(3)

    results = soup.find_all('li', class_='slide')
    #print(results)
    for result in results:
        try:
            x = result.find('a', class_='fancybox')
            y = x['data-fancybox-href']
            #print(y)
            browser.quit()
        except Exception as e:
            print(e)
            browser.quit()
            
    featured_image_url = "https://www.jpl.nasa.gov" + y
    #print(featured_image_url)
    mission_mars_data["featured_image_url"] = featured_image_url


    # ## Scraping: Mars Weather

    # In[46]:


    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)
    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    mars_tweets = soup.find_all('div', class_='js-tweet-text-container')
    #print(mars_tweets)

    for tweet in mars_tweets:
        try:
            mars_weather = tweet.find('p').text
            #print(mars_weather)
            mission_mars_data["mars_weather"]= mars_weather

        except Exception as e:
            print(e)


    # ## Scraping: Mars Facts

    # In[48]:


    url = 'https://space-facts.com/mars/'

    Mars_Facts = pd.read_html(url)
    Mars_Facts


    # In[58]:


    Mars_Facts_df = Mars_Facts[0]
    Mars_Facts_df


    # In[61]:


    Mars_Facts_df.columns = ['Mars_Profile_Parameter', 'Mars_Profile_Parameter_Value']
    Mars_Facts_df


    # ### DataFrame as HTML

    # In[62]:


    #Pandas also has a `to_html` method that we can use to generate HTML tables from DataFrames.
    Mars_Facts_html_table = Mars_Facts_df.to_html()
    Mars_Facts_html_table


    # In[63]:


    # We need to strip unwanted newlines to clean up the table.
    Mars_Facts_html_table.replace('\n', '')


    # In[64]:


    # Saving the table directly to a file.
    Mars_Facts_df.to_html('Mars_facts_table.html')

    # Reading html file and saving 'td' , 'tr' values into dictionary
    mars_info=[]
    mars_facts={}
    file = open('Mars_facts_table.html', encoding='latin-1')
    html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    for z in soup.table('td'):
        mars_info.append(z.text.strip(':'))
        mars_facts=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
    #print(mars_facts)

    mission_mars_data["mars_facts"] = mars_facts


    # In[65]:


    #get_ipython().system('open Mars_facts_table.html')


    # ## Scraping: Mars Hemisperes

    # In[135]:


    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(3)

    results_title = soup.find_all('div', class_='description')

    hemisphere_image_urls = []

    for result in results_title:
        try:
            title = result.find('h3').text
            #print(des)
            browser.click_link_by_partial_text(title)
            time.sleep(4)
            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            time.sleep(3)
            results_href = soup.find_all('div', class_='downloads')
            for result in results_href:
                img_url = result.find('a')['href']
            #print(img_url)
            
            # Run only if 'description' and 'image_url' are available
            if (title and img_url):
                # Print results
                print('-------------')
                print(title)
                print(img_url)

                # Writing values into Dictionary
                image_urls = {
                    'Title': title,
                    'Image_URL': img_url,
                }
            hemisphere_image_urls.append(image_urls)
            browser.visit(url)
        except Exception as e:
            print(e)
            browser.quit()
    #print(hemisphere_image_urls)
    mission_mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()

    #mission_mars_data["hemisphere_image_urls"]
    #mission_mars_data["Mars_facts"]
    #mission_mars_data["mars_weather"]
    #mission_mars_data["featured_image_url"]
    #mission_mars_data["news_title"]
    #mission_mars_data["news_p"]

    return mission_mars_data

