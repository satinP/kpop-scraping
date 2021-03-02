from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import sqlalchemy

# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath("__file__")))
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'kpop.db')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

engine_sql = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}")


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 500)
# pd.set_option('display.max_colwidth', -1)

url = 'https://en.wikipedia.org'

groups = []
description_group = []


def data_to_db(data, engine, table):
    '''Realiza o INSERT de dados conferindo se o ID já existe'''
    ids = ",".join([f"'{i}'" for i in data['id'].values])
    try:
        engine.execute(f"DELETE FROM {table} AS t1 WHERE t1.id in ({ids});")
    except:
        pass
    data.to_sql(table, engine, if_exists="append", index=False)
    return None


def get_group_descripton(relative_url):
    ''' Search group main description based on relative url '''
    full_url = url + relative_url

    response = urlopen(full_url)
    html = response.read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    p_tags = soup.find('p')
    for match in p_tags.findAll('sup'):
        match.replaceWith('')

    return p_tags.get_text()


def get_group_names(path='/w/index.php?title=Category:K-pop_music_groups'):
    ''' Search all group names and wikipedia relative url for group page '''
    full_url = url + path

    response = urlopen(full_url)
    html = response.read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    soup.find('div', {'class': 'mw-category-group'}).get_text()
    group_list = soup.find('div', {'class': 'mw-category'}).findAll("li")

    for gl in group_list:
        group = {}
        group['id'] = len(groups) + 1
        group['name'] = gl.get_text()
        group['relative_url'] = gl.find('a').get("href")
        groups.append(group)

    href_pages = soup.find('a', {'title': 'Category:K-pop music groups'})

    if href_pages.get_text() == 'next page':
        get_group_names(href_pages.get("href"))

    return pd.DataFrame(groups)


pd = get_group_names()


''' Validations to search group description '''
execution_min_hour = '23:00:00'
current_time = format(datetime.datetime.now().time())
if current_time > execution_min_hour:
    for index, row in pd.T.iteritems():
        group = {}
        group['id'] = row['id']
        group['description'] = get_group_descripton(row['relative_url'])
        description_group.append(group)

#engine_sql.execute("SELECT * FROM kpop").fetchall()
data_to_db(pd, engine_sql, 'kpop')
