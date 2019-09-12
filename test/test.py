import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools import Connect
from tools import Debug
webdriver = Connect.webdriver()

if __name__ == '__main__':
    dr = webdriver.Chrome()
    # Debug.start(dr)
    dr.get("http://www.baidu.com")
    kw = dr.find_element_by_id("kw")
    su = dr.find_element_by_id("su")
    # kw.send_keys("Selenium学习")
    kw.send_keys("Selenium重新使用已打开的浏览器实例")
    su.click()
    # dr.quit()