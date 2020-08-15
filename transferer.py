# one for all
# combine the functions of getSongList.py and songs2appleMusic.py

import requests
from bs4 import BeautifulSoup 
import os,re,time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains # 模拟鼠标行为用的，不过这里没用到
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def getSongListHtml(list_url,headers):
    response = requests.get(list_url, headers=headers)
    return response.text

def getSongList(html_txt, joint='&'):
    # 歌手A & 歌手B 的格式【看了看apple music多歌手格式，是用 & 连接的】
    soup = BeautifulSoup(html_txt, 'html.parser')
    # 获取歌曲名字
    song_name_list = [
        song.string for song in soup.find_all('span', class_='songlist__songname_txt')
    ]
    # 获取歌手
    singer_list = [
        ' {} '.format(joint).join(re.findall('>(.*?)</a>', str(singerTag)) ) 
        for singerTag in soup.find_all('div', class_='songlist__artist')
    ]
    # 合并
    song_list = [
        ' - '.join([song, artist]) for song, artist in zip(song_name_list, singer_list)
    ]
    return song_list

