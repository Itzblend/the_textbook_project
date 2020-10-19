from bs4 import BeautifulSoup
import requests
import os
import shutil
import json
import time
import re
import logging

## Logger stuff

logger = logging.getLogger('the_textbook_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs/realpython.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(fh)

baseurl = 'https://realpython.com/tutorials/all/'
html_doc = requests.get(baseurl)
soup = BeautifulSoup(html_doc.content, 'lxml')


links = soup.find_all('a', class_='stretched-link')

def fetch_topics():
    # Collect topics
    topics = []
    for i in links:
        topics.append('https://realpython.com'+i['href'])

    return topics

def fetch_tutorial_links():
    # Collect tutorial links
    topics = fetch_topics()

    tutorials = []
    for topic_page in topics:
        resp = requests.get(topic_page)
        tutorialsoup = BeautifulSoup(resp.content, 'lxml')
        div_tag = tutorialsoup.find_all('div', class_='card border-0')
        for a in div_tag:
            tutorials.append('https://realpython.com'+a.find('a')['href'])
    return tutorials

# Finally crawling tutorials
def fetch_tutorial_data():
    # Get data from tutorials
    tutorials = fetch_tutorial_links()

    #with open('tutorials.txt', 'r') as tutorials:
    for link in tutorials:
        file_prefix = os.path.join(f'data/{link.split("/")[-2]}')
        shutil.rmtree(file_prefix, ignore_errors=True)
        os.makedirs(file_prefix, exist_ok=False)

        logger.info(f'Processing tutorial: {link.split("/")[-2]}')

        resp = requests.get(link.rstrip())
        tutorialsoup = BeautifulSoup(resp.content, 'lxml')
        intro_text = tutorialsoup.find_all('p')


        # Strip description
        meta_tag = tutorialsoup.find('meta', attrs={'name': 'description'})

        description = str(meta_tag)
        description = re.search(r"(?<=meta content=\")(.*)(?=\" name=\"description\")", description)

        if description != None:
            description = description[1]
        else:
            description = ''

        # Strip body
        body = tutorialsoup.find('div', class_='article-body')


        with open(f'{file_prefix}/params.json', 'a', encoding="UTF-8") as params_file:
            params = {}
            params['url'] = resp.url
            params['description'] = description
            json.dump(params, params_file)


        with open(f'{file_prefix}/body.txt', 'a', encoding="UTF-8") as body:
            article = tutorialsoup.find('div', class_='article-body')
            text = article.find_all('p')
            for content in text:
                body.write(content.text)

        time.sleep(1)

def testing():
    with open('tutorials.txt', 'r') as tutorials:
        for link in tutorials:
            resp = requests.get(link.rstrip())
            tutorialsoup = BeautifulSoup(resp.content, 'lxml')

            body = tutorialsoup.find('div', class_='article-body')
            text = body.find_all('p')
            for i in text:
                print(i.text)
            break





#/html/head/meta[2]

if __name__ == "__main__":
    fetch_tutorial_data()
