from bs4 import BeautifulSoup
import requests 

url = "https://www.example.com/"

my_page = requests.get(url)
soup = BeautifulSoup(my_page.text, "html")

data = soup.find("a")
data = str(data)
#getting url for second link

start_index = data.find('"')
link_end_index = data.rfind('"')

url_2 = data[start_index+1:link_end_index]

sub_link_page = requests.get(url_2)
soup_2 = BeautifulSoup(sub_link_page.text, "html")
