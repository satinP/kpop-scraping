from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org'
full_data = {}


def url_find(path='/w/index.php?title=Category:K-pop_music_groups'):
    full_url = url + path

    response = urlopen(full_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    keys, values = [], []

    soup.find('div', {'class': 'mw-category-group'}).get_text()
    group_list = soup.find('div', {'class': 'mw-category'}).findAll("li")

    for gl in group_list:
        keys.append(gl.get_text())
        values.append(gl.find('a').get("href"))

    full_data.update(dict(zip(keys, values)))
    href_pages = soup.find('a', {'title': 'Category:K-pop music groups'})

    if href_pages.get_text() == 'next page':
        url_find(href_pages.get("href"))


url_find()
print(full_data)
