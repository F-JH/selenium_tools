# >>>说明<<<
# 此工具相当于Debug工具的反向使用，在本地创建一个socket服务端用于提供session，在服务端
# 打开webdriver，Connect.py用于与服务端通信，获取该测试实例的session信息这样每次跑测
# 试脚本时，就可以重复利用同一个浏览器，而不是重新打开新的浏览器，理论上来说应该会快多
# 了，因为有的电脑打开浏览器真的很慢。
#   经过精确测试，使用该工具重连到浏览器并加载到指定页面只需0.7799181938171387s，而正常
# 打开浏览器需要4.169507741928101s
# ( ͡° ͜ʖ ͡°)
# 好吧，看起来是个很鸡肋的东西 (╯°Д°）╯ 使用Debug工具应该就够了，要是觉得不够爽，那就用
# 一下这个工具，在某些方面也是可以省一点力气的
#
# 使用方法:
#       *注意：仅限脚本编写阶段，需要大量调试的时候使用！且只支持Chrome和Firefox ！
#
#       # from selenium import webdriver        //用此工具的webdriver替换selenium的webdriver
#
#       import connect
#       webdriver = connect.webdriver()
#       dr = webdriver.Chrome()
#       dr.get("https://www.baidu.com")
#       dr.find_element_by_id('kw').send_keys("selenium自动化测试")
#       dr.find_element_by_id('su').click()
#
#       这个工具只是在编写脚本期间，提供辅助性的调试功能，编写完后请用回selenium的webdriver
# 
# 依赖：
#       selenium
#       ReuseSelenium.py 放在同一目录下，否则需要按指定目录来import
#       WebDriverService.py 放在同一目录下，否则需要传入指定的具体位置



import re
import os, sys
import socket
import time
import traceback
import threading
sys.path.append(os.path.dirname(__file__))
import ReuseSelenium as reweb
try:
    import http.client as http_client
except ImportError:
    import httplib as http_client

from selenium.webdriver.remote.command import Command

# config
address = ('127.0.0.1', 9725)
server_file = os.path.join(os.path.dirname(__file__), 'WebDriverService.py')



class webdriver(object):
    # 如端口有改动，请传入address，默认为9725；
    # 请把WebDriverService.py文件放在同一目录下，否则需要传入指定的具体位置
    def __init__(self, addr=address, server=server_file):
        self.address = addr
        self.server_file = server
        self.who = traceback.extract_stack()[-2][0].split('/')[-1]

    def Chrome(self):
        return self.connect_chrome()

    def Firefox(self):
        return self.connect_firefox()

    def PrivateChrome(self):
        # 根据调用方文件名(上一层)，开启一个私有窗口
        return self.connect_chrome(self.who)

    def PrivateFirefox(self):
        return self.connect_firefox(self.who)

    # def search_port(self, mode):
    #     # 从默认端口 9725 逐渐+1搜索目标端口
    #     # mode: 参考 check_port()
    #     port = self.address[1]
    #     while True:
    #         if self.check_port(port) == mode:
    #             break
    #         port += 1
    #     return port


    def check_port(self, port):
        # 0 无应用占用
        # 1 webdriver service 占用
        # 2 其他应用占用
        check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check.settimeout(0.01)
        try:
            check.bind(('127.0.0.1', port))
            check.close()
            return 0
        except OSError:
            try:
                check.connect(('127.0.0.1', port))
                check.settimeout(3)
                check.send('close'.encode('utf-8'))
                eval(check.recv(512).decode('utf-8'))
                check.shutdown(2)
                return 1
            except:
                check.shutdown(2)
                return 2

    def connect_chrome(self, who=None):
        if who == None:
            who = 'default'
        check = self.check_port(self.address[1])

        if check == 0:
            os.system('start python -i "%s" Chrome "%s"' % (self.server_file, str(self.address)))
        elif check == 2:
            print('端口被其他应用占用!')
            exit(0)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        confirm = False
        for i in range(10):
            try:
                s.connect(self.address)
                confirm = True
                break
            except:
                time.sleep(1)
        if not confirm:
            print('连接超时，请检查WebDriverService与Connect的端口设置是否一致')
            print('如果检查没问题，在服务端那个黑窗口按几下回车试试，看有没有新的log打印出来，可能cmd窗口又卡了')
            exit(0)
        msg = 'getSession|chrome|%s'%who
        s.send(msg.encode('utf-8'))
        session = s.recv(512).decode('utf-8')
        session = eval(session)
        session_id = session[0]
        command_executor = session[1]
        options = (self.address, who)
        driver = reweb.Chrome_Remote(options=options, service_url=command_executor, session_id=session_id)
        return driver

    def connect_firefox(self, who=None):
        if who == None:
            who = 'default'
        check = self.check_port(self.address[1])

        if check == 0:
            os.system('start python -i "%s" Firefox "%s"' % (self.server_file, str(self.address)))
        elif check == 2:
            print('端口被其他应用占用!')
            exit(0)


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        confirm = False
        for i in range(10):
            try:
                s.connect(self.address)
                confirm = True
                break
            except:
                time.sleep(1)
        if not confirm:
            print('连接超时，请检查WebDriverService与Connect的端口设置是否一致')
            print('如果检查没问题，在服务端那个黑窗口按几下回车试试，看有没有新的log打印出来，可能cmd窗口又卡了')
            exit(0)
        msg = 'getSession|firefox|%s'%who
        s.send(msg.encode('utf-8'))
        session = s.recv(512).decode('utf-8')
        session = eval(session)
        session_id = session[0]
        command_executor = session[1]
        options = (self.address, who)
        driver = RemoteChrome(options=options, service_url=command_executor, session_id=session_id)
        return driver