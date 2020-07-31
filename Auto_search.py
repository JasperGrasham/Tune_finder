
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.request
import youtube_dl
import ffmpeg
from urllib3 import *
import requests
import subprocess
import os

# cd Desktop/Jupyter_files/Tensorflow/Discogs
# python3 -m pip install BeautifulSoup4
# python3 -m pip install urllib3
# python3 -m pip install requests
# python3 -i Auto_search.py

# To run the script replace the searched filtered url link into the base url comment marks and replace the page number
# with '....&page={chapter:02d}'

# This saves a csv file to the same place that this .py file is stored, and the n parameter is used to set the ittaration
# times the program will repeat itself for.

# base_url = "https://www.discogs.com/sell/list?genre=Funk+%2F+Soul&year=1976&format_desc=45+RPM&page={chapter:02d}"

base_url = "https://www.discogs.com/sell/list?style=House&style=Deep+House&format_desc=12%22&year=2003&page={chapter:02d}"

def search(n):
    for chapter in range(1,n):
        url = base_url.format(chapter=chapter)
        client = uReq(url)
        page_html = client.read()
        client.close()
        page_soup = soup(page_html, 'html.parser')

        # The next block of code sets up the code pieces to be retrieved from discogs, and how to get the youtube link.

        containers = page_soup.findAll('td', {'class': 'item_description'})
        release_container = page_soup.findAll('a', {'class': 'item_release_link hide_mobile'})

        for j in range(25):
            name = containers[j].strong.a.text
            link = [str('https://www.discogs.com' + release_container[k]['href']) for k in range(25)]

            song_url = [link[n] for n in range(25)]

            open = urllib.request.urlopen(song_url[j])
            page_soup2 = soup(open, 'html.parser')

            try:
                yt_container = page_soup2.find_all('div', {'id': 'youtube_player_wrapper'})

                video_urls = yt_container[0].div['data-video-ids']

                firstword = video_urls.split(',')
                yt_link = str('https://www.youtube.com/watch?v=' + firstword[0]) #+ '?start=60&end=70')

                with youtube_dl.YoutubeDL({'format': '140'}) as ydl:
                    ydl.download([yt_link])

            except:
                print('youtube:' + "No - ids")

search(3)




