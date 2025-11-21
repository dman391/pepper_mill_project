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



def page_viewer(url):

    driver = webdriver.Chrome()
    driver.get(url)
    html_code = driver.page_source
    time.sleep(30)
    driver.quit()
    return html_code

#for each page gets the listings 
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


#gets the stuff we want
def page_information_scrapper(links):
    size_list = []
    price_list = []
    views_list = []
    link_list = []
    for link in links:
        print(link)
        try:
            html_code = page_viewer(link)
            info_soup = BeautifulSoup(html_code, "html.parser")
            listing_title = info_soup.find("h1", class_ = "tm-marketplace-buyer-options__listing_title").get_text()
            listing_price = info_soup.find("p", class_ = "tm-buy-now-box__price p-h1").get_text()  
            listing_views = info_soup.find("div", class_ = "tm-share-listing-link__info-block").get_text()
            link_list.append(link)
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
        except:
            pass
    return size_list, price_list, views_list, link_list

#gets all the pages
def page_selector():
    base_url = "https://www.trademe.co.nz/a/marketplace/home-living/kitchen/tableware-linen/salt-pepper-shakers/search?search_string=pepper%20mill&condition=new&user_region=70"
    main_page_html = page_viewer(base_url)
    soup = BeautifulSoup(main_page_html, "html.parser")
    end_number = int((soup.find("span", class_="o-pagination__current").get_text())[10:])
    total_url = ["https://www.trademe.co.nz/a/marketplace/home-living/kitchen/tableware-linen/salt-pepper-shakers/search?search_string=pepper%20mill&condition=new&user_region=70&page=" + str(num) for num in range(1,end_number+1)]

    
    return total_url


all_pages = page_selector()
all_pages_links = [] #gives all listings

for page in all_pages:
    html_code = page_viewer(page)
    all_pages_links += page_url_finder(html_code)


#print(all_pages_links)
raw_data = page_information_scrapper(all_pages_links)

  

#making data frame and exporting to excel sheet

data = {"size_cm" : raw_data[0], "price_nzd" : raw_data[1], "views" : raw_data[2], "link" : raw_data[3]}
df = pd.DataFrame(data)
df.to_excel("pepper_mill_data.xlsx", index = False)
print("finish.here")
