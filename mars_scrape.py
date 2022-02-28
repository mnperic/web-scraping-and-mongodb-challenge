# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time


def init_browser():
    # Capture path to Chrome Driver & Initialise browser
    executable_path = {'executable_path':"/Users/minoperic/Data Analytics/Homework/web-scraping-and-mongo-db-challenge-chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    html = browser.html
    soup = bs(html,"html.parser")

    # Scrape latest news about Mars from NASA
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_paragraph 
    
    # Determine Mars feature image
    nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image)
    time.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    # Use splinter to click on the mars featured image to bring the full res image
    results = browser.find_by_xpath(xpath)
    image = results[0]
    image.click()
    time.sleep(2)
    
    # Get image URL via BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    image_url = soup.find("img", class_="fancybox-image")["src"]
    full_image_url = base_url + image_url
    mars_facts_data["featured_image"] = full_image_url
      
    # #### Mars Weather

    # Get Mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_facts_data["mars_weather"] = mars_weather

    # #### Mars Facts
    url_facts = "https://space-facts.com/mars/"
    time.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    mars_facts_df = table[0]
    mars_facts_df.columns = ["Parameter", "Values"]
    clean_table = mars_facts_df.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table

    # Determine Mars hemisperes
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    # Determine base url
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    hemisphere_image_urls = []
    hemisphere_image_urls

    # Hemisphere #1
    hemisphere_image_urls = []
    results_1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    time.sleep(2)
    cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    cerberus_image = browser.html
    soup = bs(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_image_url = hemisphere_base_url + cerberus_url
    #print(cerberus_image_url)
    cerberus_title = soup.find("h2",class_="title").text
    #print(cerberus_title)
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    cerberus = {"image title":cerberus_title, "image url": cerberus_image_url}
    hemisphere_image_urls.append(cerberus)

    # Hemisphere #2  
    results_2 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    time.sleep(2)
    schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    schiaparelli_image = browser.html
    soup = bs(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_image_url = hemisphere_base_url + schiaparelli_url
    #print(schiaparelli_img_url)
    schiaparelli_title = soup.find("h2",class_="title").text
    #print(schiaparelli_title)
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_image_url}
    hemisphere_image_urls.append(schiaparelli)

    # Hemisphere #3
    results_3 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    time.sleep(2)
    syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    syrtis_major_image = browser.html
    soup = bs(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    syrtis_major_image_url = hemisphere_base_url + syrtis_major_url
    #print(syrtis_major_image_url)
    syrtis_major_title = soup.find("h2",class_="title").text
    #print(syrtis_major_title)
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_image_url}
    hemisphere_image_urls.append(syrtis_major)

    # Hemisphere #4
    results_4 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    time.sleep(2)
    valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    valles_marineris_image = browser.html
    soup = bs(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    valles_marineris_image_url = hemisphere_base_url + syrtis_major_url
    #print(valles_marineris_image_url)
    valles_marineris_title = soup.find("h2",class_="title").text
    #print(valles_marineris_title)
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_image_url}
    hemisphere_image_urls.append(valles_marineris)

    mars_facts_data["hemisphere_image_url"] = hemisphere_image_urls

    return mars_facts_data