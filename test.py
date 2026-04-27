import requests
from bs4 import BeautifulSoup
import lxml


response = requests.get(url='https://free-proxy-list.net/ru/' )
soup = BeautifulSoup(response.text, 'lxml')

table = soup.find('table', class_ = 'table table-striped table-bordered')
rows = table.find_all('tr')
raw_proxies = []
for row in rows[1:]:
    raw_proxies.append(
                        f"{row.find_all('td')[0].text}:{row.find_all('td')[1].text}")
print(raw_proxies)
