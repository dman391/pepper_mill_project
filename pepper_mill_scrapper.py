#trade me a dynamic website so need to do more things 

#currently on works for first page need new function to go through each page 
import time
from urllib.parse import urljoin
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
import pandas as pd 
import re
from pint import UnitRegistry


main_url = "https://www.trademe.co.nz/a/marketplace/home-living/kitchen/tableware-linen/salt-pepper-shakers/search?search_string=pepper%20mill&condition=new&user_region=70"

def page_viewer(url):

    driver = webdriver.Chrome()
    driver.get(url)
    html_code = driver.page_source
    time.sleep(1)
    driver.quit()
    return html_code

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
        html_code = page_viewer(link)
        info_soup = BeautifulSoup(html_code, "html.parser")
        listing_title = info_soup.find("h1", class_ = "tm-marketplace-buyer-options__listing_title").get_text()
        listing_price = info_soup.find("p", class_ = "tm-buy-now-box__price p-h1").get_text()  
        listing_views = info_soup.find("div", class_ = "tm-share-listing-link__info-block").get_text()
        
        pattern = r"(\d+(?:\.\d+)?)\s*(cm|inches|inch|in|mm)"
        size = re.search(pattern,listing_title)
        if size != None:
            ureg_object = UnitRegistry()
            size_unknown_unit = ureg_object.Quantity(size.group(1)+size.group(2))
            size_list.append(size_unknown_unit.to("cm").magnitude) #always adds units in cm to the list
            
        else:
            size_list.append(None)
        pattern = r"(\d+(?:\.\d+)?)"
        price = re.search(pattern,listing_price)
        price_list.append(float(price.group(1)))
        
        pattern = r"(\d+)"
        views = re.search(pattern,listing_views)
        views_list.append(int(views.group(1)))
        
    return size_list, price_list, views_list

def page_selector():




html_code = page_viewer(main_url)

v1 = page_url_finder(html_code)

raw_data = page_information_scrapper(v1[5:7])

#making data frame and exporting to excel sheet

data = {"size_cm" : raw_data[0], "price_nzd" : raw_data[1], "views" : raw_data[2]}
df = pd.DataFrame(data)
df.to_excel("pepper_mill_data.xlsx", index = False)
print("finish.here")
