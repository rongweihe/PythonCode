
# encoding=utf8 
'''
解决中文乱码 模拟登录微博
'''
import sys  
import requests
from selenium import webdriver
chromePath = r'B:\Download\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath) #构建浏览器
loginUrl = 'http://www.weibo.com/login.php' 
wd.get(loginUrl) #进入登陆界面
wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('18800119432') #输入用户名
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('weibo.com') #输入密码
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click() #点击登陆
req = requests.Session() #构建Session
cookies = wd.get_cookies() #导出cookie
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value']) #转换cookies
print(cookies) #打印cookies


# encoding=utf8 
'''
解决中文乱码 第一个 python 爬虫
'''
import sys  
import requests
from selenium import webdriver
chromePath = r'B:\Download\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath) #构建浏览器
loginUrl = 'http://bestcoder.hdu.edu.cn/login.php' 
wd.get(loginUrl) #进入登陆界面
wd.find_element_by_xpath('//*[@id="username"]').send_keys('username') #输入用户名
wd.find_element_by_xpath('//*[@id="password"]').send_keys('passwd') #输入密码
wd.find_element_by_xpath('//*[@id="login-form"]/form/fieldset/div[2]/button').click() #点击登陆
req = requests.Session() #构建Session
cookies = wd.get_cookies() #导出cookie
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value']) #转换cookies
print(cookies) #打印cookies
