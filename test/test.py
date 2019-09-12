import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools import Connect
from tools import Debug
from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
webdriver = Connect.webdriver()

def check(driver):
    if os.system('tasklist | findstr chromedriver.exe'):
        return False
    return True


if __name__ == '__main__':
    dr = webdriver.Chrome()
    Debug.start(dr)
    dr.get("http://www.baidu.com")
    kw = dr.find_element_by_id("kw")
    su = dr.find_element_by_id("su")
    su.send_keys("Selenium学习")
    kw.click()
    # dr.quit()
