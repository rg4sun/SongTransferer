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