import re
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import Debug

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '6.0.1'
    desired_caps['deviceName'] = '127.0.0.1:7555'
    desired_caps['appPackage'] = 'com.null00.warframe'         # 包名
    desired_caps['appActivity'] = '.activity.SplashActivity'    # 启动Activity
    desired_caps['newCommandTimeout'] = '6000'                   # 设置session_id过期时间

    dr = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    Debug.start(dr)


    WebDriverWait(dr, 6).until(lambda dr:dr.find_element_by_id("com.null00.warframe:id/comm_title"))
    dr.find_element_by_id("com.null00.warframe:id/comm_back").click()
    WebDriverWait(dr, 1).until(lambda dr:dr.find_element_by_id("com.null00.warframe:id/track_list_recycler"))
    frame = dr.find_element_by_id("com.null00.warframe:id/track_list_recycler")
    frame.get_attribute()
    l = 'childSelector(className("android.widget.LinearLayout"))'
    Linears = frame.find_elements_by_android_uiautomator(l)
for i in Linears:
    print('-'*75)
    TextView = i.find_elements_by_xpath(".//android.widget.TextView")
    for j in TextView:
        print(j.text)
    xpath = ".//android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.TextView[1]"
    minute = i.find_element_by_xpath(xpath)
    print(minute.text)
input(">>>")