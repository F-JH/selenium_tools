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
    # dr.implicitly_wait(3)
    Debug.start(dr)
    dr.get("http://192.168.34.104/index.html")
    go = dr.find_element_by_id('select2-chosen-2')
    # WebDriverWait(dr, 10).until(check)
    go.click()
    selector = dr.find_element_by_id('select2-drop')
    selector.find_element_by_xpath('.//div/input').send_keys('CAN')
    position = selector.find_element_by_xpath('.//ul/li/ul')
    position.click()

    daoda = dr.find_element_by_id('select2-drop')
    daoda.find_element_by_xpath('.//div/input').send_keys('HAK')
    daoda.find_element_by_xpath('.//ul/li/ul').click()
    notice = dr.find_element_by_id('notice')
    ActionChains(dr).move_to_element(notice).perform()
    # dr.quit()
