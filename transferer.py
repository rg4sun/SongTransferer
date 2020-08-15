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

def elementExist_id(ele_id):
    '''
    用于判断页面上某个id的元素是否存在/出现
    '''
    try:
        browser.find_element_by_id(ele_id)
        return True
    except:
        return False

def transferer():
    song_list_url = input('Paste the url of your song list: ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    song_list = getSongList(getSongListHtml(song_list_url, headers))