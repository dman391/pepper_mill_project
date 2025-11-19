#trade me a dynamic website so need to do more things 


import time
from urllib.parse import urljoin
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import pandas as pd 
import re


main_url = "https://www.trademe.co.nz/a/marketplace/home-living/kitchen/tableware-linen/salt-pepper-shakers/search?search_string=pepper%20mill&condition=new&user_region=70"

driver = webdriver.Chrome()

driver.get(main_url)

html_code = driver.page_source
time.sleep(1)
driver.quit()


def page_url_finder(html_code):
    dirty_links = []
    final_links = []
    soup = BeautifulSoup(html_code, "html.parser")
    
    all_links_tag = soup.find_all("a", rel=True, href = True)   
    
    for tag in all_links_tag:
        dirty_links.append(tag.get("href"))
    
    base_url = "https://www.trademe.co.nz/a/"
    
    for link in dirty_links:
        if link[0:79] == "/a/marketplace/home-living/kitchen/tableware-linen/salt-pepper-shakers/listing/" :
            absolute_url = urljoin(base_url,link)
            final_links.append(absolute_url)
    return final_links


def page_information_scrapper(links):
    size_list = []
    price_list = []
    views_list = []

    for link in links:
        driver = webdriver.Chrome()
        driver.get(link)
        html_code = driver.page_source
        time.sleep(10)
        driver.quit()
        info_soup = BeautifulSoup(html_code, "html.parser")
        listing_title = info_soup.find("h1", class_ = "tm-marketplace-buyer-options__listing_title").get_text()
        listing_price = info_soup.find("p", class_ = "tm-buy-now-box__price p-h1").get_text()  
        listing_views = info_soup.find("div", class_ = "tm-share-listing-link__info-block").get_text()
        
        pattern = r"(\d+(?:\.\d+)?)\s*(cm|inches|inch|in)"
        size = re.search(pattern,listing_title)
        size_list.append(size.group(1))
        
        pattern = r"(\d+(?:\.\d+)?)"
        price = re.search(pattern,listing_price)
        price_list.append(float(price.group(1)))
        
        pattern = r"(\d+)"
        views = re.search(pattern,listing_views)
        views_list.append(int(views.group(1)))
        
        return size_list, price_list, views_list



v1 = page_url_finder(html_code)
print(page_information_scrapper(v1[0:1]))