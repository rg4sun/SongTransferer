from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains # 模拟鼠标行为用的，不过这里没用到
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os,re,time

def elementExist_id(ele_id):
    '''
    用于判断页面上某个id的元素是否存在/出现
    '''
    try:
        browser.find_element_by_id(ele_id)
        return True
    except:
        return False

with open('./mySongList.txt', 'r') as f:
    song_list  = f.read()
song_list

# macOS chrome selenium python 全屏
# https://blog.csdn.net/u010953692/article/details/83822818
# options = webdriver.ChromeOptions()
# options.add_argument('--kiosk')

tool_url = 'https://www.tunemymusic.com/zh-cn/'
# browser = webdriver.Chrome(chrome_options=options) 
browser = webdriver.Chrome() # 设置浏览器驱动为chrome
browser.get(tool_url) # 模拟打开网页
browser.maximize_window()

browser.find_element_by_id('startButton').click() # 找到并点击开始按钮
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[2]/div[3]/div[17]').click() # 选择文本输入歌曲列表
time.sleep(1)
browser.find_element_by_id('songText').send_keys(song_list) # 模拟输入 歌曲 
time.sleep(3)
browser.find_element_by_id('FreeTextConfirmInput').click() # 点击 转换歌曲列表
time.sleep(1)
browser.find_element_by_id('Step2Next').click() # 点击 下一步
time.sleep(3)
browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[4]/div[3]/div[2]').click() # 找到 apple music并点击，点击后会弹出新窗口
time.sleep(1)
browser.switch_to_window(browser.window_handles[1]) # 将窗口指向 新窗口句柄
browser.find_element_by_id('LoginBtn').click() # 点击登陆 apple id
# ===============================================================================
# 这里需要登陆 apple id，建议手动输入（自动化也可以，但是id 和 密码 得内置在这个脚本里，不安全）
# 因此此处需要手动登陆 apple id
# ===============================================================================
browser.switch_to_window(browser.window_handles[0]) # 将窗口指回原本的窗口
#等待登陆完后 页面出现 ‘开始移动我的音乐’按钮 其元素可见
ele_id = "Step4Next"
param = (By.ID,ele_id)
WebDriverWait(browser,300).until(EC.visibility_of_element_located(param)) # 等待该元素出现, 默认等 300s
browser.find_element_by_id(ele_id).click() # 出现后点击
#等待转换完后 页面出现 ‘再次转换’按钮 其元素可见
ele_id = "ConvertAgain"
param = (By.ID,ele_id)
WebDriverWait(browser,600).until(EC.visibility_of_element_located(param)) # 等待该元素出现,等600s
print("当前歌单已经转换完成")
# 如果有丢失歌曲，就勾选丢失列表复选框
ele_id = 'MissingCheckBox'
if elementExist_id(ele_id):
    browser.find_element_by_id(ele_id).click()
    page_html = browser.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    soup.find_all('div', class_='PlaylistItem InnerItem Fail')
    missing_songs = [
        ''.join(re.findall('PlaylistName">(.*?)</div>', str(songTag)))
        for songTag in soup.find_all('div', class_='PlaylistItem InnerItem Fail')
    ]
    # 发现最后一首丢失歌曲的 class和之前的不一样，单独处理后添加至丢失表中
    missing_songs.append(
        ''.join(re.findall(
        'PlaylistName">(.*?)</div>',
        str(soup.find_all('div', class_='PlaylistItem InnerItem LastTrackOfPlaylist Fail'))
    ))
    )
    if missing_songs[-1] == '':
        missing_songs = missing_songs[:-1]
    # 输出转换结果信息
    bar = '-'*25
    print('成功转换{}首歌曲，丢失如下{}首:\n{}\n{}'.format( # song_list.split('\n')把字符串转换成list才可以统计歌曲数量
        len(song_list.split('\n')) - len(missing_songs), len(missing_songs),bar,
        '\n'.join(missing_songs)
    ))
else:
    print('成功转换{}首歌曲，没有丢失歌曲'.format(len(song_list.split('\n'))))
