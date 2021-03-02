from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org'

full_data = []


def get_group_descripton(relative_url):
    full_url = url + relative_url

    response = urlopen(full_url)
    html = response.read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    p_tags = soup.find('p')
    for match in p_tags.findAll('sup'):
        match.replaceWith('')

    return p_tags.get_text()


def url_find(path='/w/index.php?title=Category:K-pop_music_groups'):
    full_url = url + path

    response = urlopen(full_url)
    html = response.read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    soup.find('div', {'class': 'mw-category-group'}).get_text()
    group_list = soup.find('div', {'class': 'mw-category'}).findAll("li")

    for gl in group_list:
        group = {}
        group['id'] = len(full_data)
        group['name'] = gl.get_text()
        group['relative_url'] = gl.find('a').get("href")
        #group['description'] = get_group_descripton(group['relative_url'])
        full_data.append(group)

    href_pages = soup.find('a', {'title': 'Category:K-pop music groups'})

    if href_pages.get_text() == 'next page':
        url_find(href_pages.get("href"))

    return pd.DataFrame(full_data)


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)
pd = url_find()

# for index, row in pd.T.iteritems():
#    get_group_descripton( row['relative_url'] )
