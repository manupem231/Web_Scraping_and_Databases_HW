# Mission to Mars

# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from splinter import Browser
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():

    browser = init_browser()

    # Scraping: NASA Mars News

    mission_mars_data = {} # Defining an empty dictionary
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=15&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results_paragraph = soup.find_all('div', class_='image_and_description_container')
    results_title = soup.find_all('div', class_='content_title')

    # Retrieving 'News Paragraph'
    for result in results_paragraph:
        try:
            news_p = result.find('div', class_='rollover_description_inner').text
            #print(news_p)
            mission_mars_data["news_p"] = news_p

        except Exception as e:
            print(e)


    # Retrieving 'News Title'
    for result in results_title:
        try:
            news_title = result.find('a').text
            #print(news_title)
            mission_mars_data["news_title"] = news_title

        except Exception as e:
            print(e)


    # Scraping: JPL Mars Space Images - Featured Image
    #browser = init_browser()
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)

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


    # Scraping: Mars Weather

    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(twitter_url)
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


    # Scraping: Mars Facts
    mars_url = 'https://space-facts.com/mars/'

    Mars_Facts = pd.read_html(mars_url)
    Mars_Facts_df = Mars_Facts[0]
    Mars_Facts_df.columns = ['Mars_Profile_Parameter', 'Mars_Profile_Parameter_Value']

    # DataFrame as HTML
    #Pandas also has a `to_html` method that we can use to generate HTML tables from DataFrames.
    Mars_Facts_html_table = Mars_Facts_df.to_html()
    # We need to strip unwanted newlines to clean up the table.
    facts = Mars_Facts_html_table.replace('\n', '')
    # Saving the table directly to a file.
    Mars_Facts_df.to_html('Mars_facts_table.html')
    mission_mars_data["mars_facts"] = facts

    # Scraping: Mars Hemisperes
    browser = init_browser()
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

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
            browser.visit(hemispheres_url)
        except Exception as e:
            print(e)
            browser.quit()
    #print(hemisphere_image_urls)
    mission_mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()

    return mission_mars_data

