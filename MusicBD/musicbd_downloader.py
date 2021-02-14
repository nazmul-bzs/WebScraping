#Author: Nazmul Hasan
#Date: 14/2/2021

import requests
from bs4 import BeautifulSoup
from clint.textui import progress
import os
from pathlib2 import Path


BASE_URL = 'https://www.music.com.bd/download/'
try:
    main_page = requests.get(BASE_URL)
except ConnectionError:
    print('Check Internet Connection')
soup = BeautifulSoup(main_page.content, 'html.parser')
dir_list = soup.find_all('a', class_='list-group-item')

if Path('downloaded').is_dir():
    os.chdir('downloaded')
else:
    os.mkdir('downloaded')
    os.chdir('downloaded')

def iter_dir(path):
    url = path
    main_page = requests.get(url)
    soup = BeautifulSoup(main_page.content, 'html.parser')
    dir_list = soup.find_all('a', class_='list-group-item')
    for dir in dir_list:
        link = dir.get('href')
        dir_name = dir.contents[2].strip()
        if dir_name.find('Back to Parent Directory') != -1:
            continue
        if dir_name.find('Dossier parent') != -1:
            continue
        if is_dir(link):
            if Path(dir_name).is_dir():
                os.chdir(dir_name)
            else:
                os.mkdir(dir_name)
                os.chdir(dir_name)
            iter_dir(link)
            os.chdir('..')
        else:
            if Path(dir_name).is_file():
                print('Already Downloaded:', dir_name)
                print()
            else:
                download_file(link, dir_name)

def is_dir(path):
    if path.endswith('.html'):
        return False
    return True

def download_file(link, file_name):
    print('Started Downloading:', file_name)
    try:
        down_page = requests.get(link)
    except:
        down_page = requests.get('https:'+link)
    soup = BeautifulSoup(down_page.content, 'html.parser')
    down_link = soup.find('a', class_='btn btn-default btn-lg btn-block btn-dl').get('href')
    resource = requests.get(down_link, stream=True)
    total_length = int(resource.headers.get('content-length'))
    with open(file_name, "wb") as f:
        for chunk in progress.bar(resource.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    print('Finished Downloading:', file_name)
    print()

print('Downloading Started...')
for dir in dir_list:
    link = dir.get('href')
    dir_name = dir.contents[2].strip()
    if Path(dir_name).is_dir():
        os.chdir(dir_name)
    else:
        os.mkdir(dir_name)
        os.chdir(dir_name)
    iter_dir(link)
    os.chdir('..')

os.chdir('..')
print('All Songs Downloaded Successfully')
