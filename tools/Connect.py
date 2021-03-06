#coding=utf-8
import re
import ast
eval = ast.literal_eval
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
isMac = False
from selenium.webdriver.remote.command import Command
import platform
if "Windows" not in platform.system():
    import appscript
    isMac = True

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

    def Chrome(self, options=None, no_img=False):
        return self.connect_chrome(options=options, no_img=no_img)

    def Firefox(self, options=None, no_img=False):
        return self.connect_firefox(options=options, no_img=no_img)

    def PrivateChrome(self, options=None, no_img=False):
        # 根据调用方文件名(上一层)，开启一个私有窗口
        return self.connect_chrome(self.who, options=options, no_img=no_img)

    def PrivateFirefox(self, options=None, no_img=False):
        return self.connect_firefox(self.who, options=options, no_img=no_img)

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

    def connect_chrome(self, who=None, options=None, no_img=False):
        if who == None:
            who = 'default'
        check = self.check_port(self.address[1])

        if check == 0:
            cmd = 'start python -i "%s" "%s"' % (self.server_file, str(self.address))
            if isMac:
                appscript.app("Terminal").do_script(cmd)
            else:
                os.system(cmd)
        elif check == 2:
            print('服务端出现错误，或是端口被其他应用占用!')
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
            print('连接超时...')
            print('检查一下服务端窗口是不是卡住了，按几下回车...')
            exit(0)
        msg = 'getSession|chrome|%s|%s|%s'%(who, str(options), str(no_img))
        s.send(msg.encode('utf-8'))
        session = s.recv(512).decode('utf-8')
        session = eval(session)
        session_id = session[0]
        command_executor = session[1]
        options = (self.address, who)
        driver = reweb.Chrome_Remote(options=options, service_url=command_executor, session_id=session_id)
        return driver

    def connect_firefox(self, who=None, options=None, no_img=False):
        if who == None:
            who = 'default'
        check = self.check_port(self.address[1])

        if check == 0:
            cmd = 'python -i "%s" "%s"' % (self.server_file, str(self.address))
            if isMac:
                appscript.app("Terminal").do_script(cmd)
            else:
                os.system("start "+cmd)
        elif check == 2:
            print('服务端出现错误，或是端口被其他应用占用!')
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
            print('如果检查没问题，可能是cmd窗口又卡了，按一下回车')
            exit(0)
        msg = 'getSession|firefox|%s|%s|%s'%(who, str(options), str(no_img))
        s.send(msg.encode('utf-8'))
        session = s.recv(512).decode('utf-8')
        session = eval(session)
        session_id = session[0]
        command_executor = session[1]
        options = (self.address, who)
        driver = reweb.Firefox_Remote(options=options, service_url=command_executor, session_id=session_id)
        return driver