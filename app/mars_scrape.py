# Import dependencies and setup

import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run scrape and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Close webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Visit/scrape Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_element = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_element.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_element.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click full image button
    full_image_element = browser.find_by_tag('button')[1]
    full_image_element.click()

    # Parse the resulting html with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        image_url_rel = image_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    image_url = f'https://spaceimages-mars.com/{image_url_rel}'

    return image_url


def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url + 'index.html')

    # Click the link, find the sample anchor, return the href
    hemisphere_image_urls = []
    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item img")[i].click()
        hemisphere_data = scrape_hemisphere(browser.html)
        hemisphere_data['image_url'] = url + hemisphere_data['image_url']
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere_data)
        # Navigate back
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    # parse html text
    hemisphere_soup = soup(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_element = None
        sample_element = None

    hemispheres = {
        "title": title_element,
        "image_url": sample_element
    }

    return hemispheres


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
