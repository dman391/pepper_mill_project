#goal : getting multiple links from a page 
import requests
from bs4 import BeautifulSoup

main_url = "https://www.nzherald.co.nz/nz/kaitaia-homicide-nz-first-pays-tribute-to-far-north-businessman-monty-knight/TQBENVT5WZCYVD4HODE7XBUH5Q/"

main_page = requests.get(main_url)
my_soup = BeautifulSoup(main_page.text, "html")

all_links = my_soup.find_all("a", href = True)


final_external_links = []

for element in all_links:
    #element not string by bs4 element tag so can do following
    if element["href"][0:8] == "https://":
        final_external_links.append(element["href"])



print(final_external_links)
