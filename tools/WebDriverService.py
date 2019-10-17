import re
import ast
import traceback
import os, sys
import threading
import socket
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxProfile

DriverList = {'chrome':{}, 'firefox':{}}

class Task(threading.Thread):
    def __init__(self, dr, browser, who):
        super(Task, self).__init__()
        self.dr = dr
        self.browser = browser
        self.who = who
        self.result = None
    def run(self):
        try:
            title = self.dr.title
            self.result = True
        except:
            try:
                self.dr.quit()
                print('PID:%d' % DriverList[self.browser][self.who][1] + ',' + self.who + '>' + self.browser + ',实例已被强制关闭...')
                self.result = False
            except:
                pass
    def getResult(self):
        return self.result

def check_alive(browser):
    # 定期检查实例是否被不可抗力强行关闭
    while True:
        try:
            threads = []
            for i in DriverList[browser]:
                t = Task(DriverList[browser][i][0], browser, i)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
            for thread in threads:
                if thread.getResult():
                    continue
                DriverList[browser].pop(thread.who)
            if browser == 'firefox':    # Firefox响应比较快，Chrome慢...
                time.sleep(3)
        except RuntimeError:    # 检查期间可能出现DriverList内容的变动
            time.sleep(0.1)
            continue
        except KeyError:
            time.sleep(0.1)
            continue

def create_driver(browser, who, options=None, no_img=False):
    print('creat new webdriver...')
    if browser == 'chrome':
        # 无图模式配置
        if no_img:
            chop = ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images': 2}
            chop.add_experimental_option('prefs', prefs)
        else:
            chop = None
        dr = webdriver.Chrome(options=options, chrome_options=chop)
        DriverList['chrome'][who] = [dr, dr.service.process.pid, no_img]
    else:
        # 无图模式配置
        if no_img:
            ffile = FirefoxProfile()
            ffile.set_preference('browser.migration.version', 9001)
            ffile.set_preference('permissions.default.image', 2)
        else:
            ffile = None
        dr = webdriver.Firefox(firefox_profile=ffile, options=options)
        DriverList['firefox'][who] = [dr, dr.service.process.pid, no_img]

def check_who(browser, who, no_img):
    if who in DriverList[browser]:
        if DriverList[browser][who][2] == no_img:
            return True
    return False

def quit_webdriver(browser, who):
    try:
        DriverList[browser][who][0].quit()
        DriverList[browser].pop(who)
    except KeyError:
        pass

def handle(sock_links):
    while True:
        for i in sock_links:
            try:
                data = i.recv(512)
            except:
                continue
            if not data:
                sock_links.remove(i)
                continue
            else:
                data = data.decode('utf-8')
                params = data.split('|')
                if data == "close":
                    i.send('True'.encode('utf-8'))
                    i.shutdown(2)
                    i.close()
                elif params[0] == "getSession":
                    browser = params[1]
                    who = params[2]
                    # 接收用户定制的options
                    options = ast.literal_eval(params[3])
                    #  是否以无图模式打开
                    no_img = ast.literal_eval(params[4])
                    if check_who(browser, who, no_img):
                        msg = '["%s", "%s"]' %(DriverList[browser][who][0].session_id, DriverList[browser][who][0].command_executor._url)
                    else:
                        print('以无图模式开启...' if no_img else '以有图模式开启...')
                        quit_webdriver(browser, who)
                        create_driver(browser, who, options, no_img)
                        msg = '["%s", "%s"]' %(DriverList[browser][who][0].session_id, DriverList[browser][who][0].command_executor._url)
                    i.send(msg.encode('utf-8'))
                    i.shutdown(2)
                    i.close()
                elif params[0] == 'quit':
                    browser = params[1]
                    who = params[2]
                    quit_webdriver(browser, who)
                else:
                    i.send('0'.encode('utf-8'))
            sock_links.remove(i)
            # print('---remove---')


if __name__ == '__main__':
    address = ast.literal_eval(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(address)
    except OSError:
        print("端口已被占用!")
    s.listen(1)
    sock_links = []
    
    #清理可能残留的driver进程
    os.popen('taskkill /F /IM chromedriver.exe')
    os.popen('taskkill /F /IM geckodriver.exe')

    attention = \
    '''
                ============================================================
                                    没事不要关闭这个窗口
                            如遇服务端无反应，则在此窗口下按下回车
                            键。根据经验，建议将此窗口最小化。
                ============================================================
    '''
    print(attention)





    t = threading.Thread(target=handle, args=[sock_links])
    t.start()
    
    check_chrome = threading.Thread(target=check_alive, args=["chrome"])
    check_firefox = threading.Thread(target=check_alive, args=["firefox"])
    check_chrome.start()
    check_firefox.start()

    print('Service start at port %d'%address[1])
    while True:
        ss, addr = s.accept()
        print('connect from:', addr)
        ss.setblocking(0)   # 设置recv()为非阻塞，此时如果某个连接超时得不到信息则会抛出异常
        sock_links.append(ss)