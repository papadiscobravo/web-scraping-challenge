# scrape_mars.py

# dependencies
import os
import pandas as pd
import pymongo
import requests
import sys

from bs4 import BeautifulSoup
from IPython.display import Image
from sys import platform
from webdriver_manager.chrome import ChromeDriverManager

# import Splinter and set the chromedriver path
from splinter import Browser

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

data = {}

# 0
# Create a function called scrape that will execute all of your scraping 
# code from above and return one Python dictionary containing all of the
# scraped data:
# copy-paste the code from Jupyter that does the scraping
def scrape_all():

    # scraping NASA Mars News
    # collect the latest News Title and Paragraph Text from redplanetscience.com...
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Retrieve page with the requests module
    response = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')

    news_title = soup.find("div", class_ = "content_title").get_text()

    news_graf_results = soup.find("div", class_="article_teaser_body").get_text()
    news_graf = news_graf_results

    # scraping JPL Mars Space Images - Featured Image
    # visit spaceimages-mars.com...
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # ...retrieve page with the requests module...
    response = browser.html

    # ...create BeautifulSoup object; parse with 'html.parser'...
    soup = BeautifulSoup(response, 'html.parser')

    # ...and find the URL of the current Featured Mars Image 
    # and assign the url string to a variable called featured_image_url.
    featured_image_relative_url = soup.find("a", class_="showimg fancybox-thumbs")
    featured_image_relative_url = featured_image_relative_url.get("href")
    featured_image_url = f"{url}{featured_image_relative_url}"

    # scraping Mars Facts
    # visit galaxyfacts-mars.com
    url = "https://galaxyfacts-mars.com"
    browser.visit(url)
    HTML_tables = pd.read_html(url)
    df_from_html_table = HTML_tables[0]
    html_from_df = df_from_html_table.to_html(classes="table table-striped")
    # df_from_html_table.to_html("table.html")

    url = "https://marshemispheres.com"
    browser.visit(url)
    hemisphere_images = []
    image_links = browser.find_by_css("a.product-item img")

    for i in range( len(image_links)):
        each_image = {}
        # A search for hrefs associated with "Hemisphere Enhanced"
        browser.find_by_css("a.product-item img")[i].click()
        # should return four URLs
        # can loop through clicking on each one
        # and on the new page that opens, scrape the URL associated with "Sample"
        hemisphere_links = browser.links.find_by_partial_text("Sample").first
        print(hemisphere_links)
        hemisphere_links["href"]
        title = browser.find_by_css("h2.title").text
        each_image["title"] = title
        each_image["link"] = hemisphere_links["href"]
        hemisphere_images.append(each_image)
        browser.back()

        # close the session
        browser.quit()

    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define database and collection
    db = client.mars_db
    collection = db.facts

    # put together dictionary of each of the other elements I scraped
    # and insert them one at a time into the MongoDB called collection

    data = {
        "news_title": news_title,
        "news_graf": news_graf,
        "featured_image": featured_image_url,
        "data_table": html_from_df,
        "hemisphere_images": hemisphere_images
        }

    collection.update({}, data, upsert = True)