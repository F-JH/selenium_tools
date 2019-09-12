import re
import os, sys
import threading
import socket
import time
from selenium import webdriver

DriverList = {'chrome':{}, 'firefox':{}}

def check_alive(browser):
    # 定期检查实例是否被不可抗力强行关闭
    while True:
        for i in DriverList[browser]:
            try:
                DriverList[browser][i].title
            except:
                DriverList[browser].pop(i)
        time.sleep(3)

def create_driver(browser, who):
    if browser == 'chrome':
        dr = webdriver.Chrome()
        DriverList['chrome'][who] = [dr, dr.service.process.pid]
    else:
        dr = webdriver.Firefox()
        DriverList['firefox'][who] = [dr, dr.service.process.pid]

def check_who(browser, who):
    return who in DriverList[browser]

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
                    browser = data.split('|')[1]
                    who = data.split('|')[2]
                    if check_who(browser, who):
                        msg = '["%s", "%s"]' %(DriverList[browser][who][0].session_id, DriverList[browser][who][0].command_executor._url)
                    else:
                        create_driver(browser, who)
                        msg = '["%s", "%s"]' %(DriverList[browser][who][0].session_id, DriverList[browser][who][0].command_executor._url)
                    i.send(msg.encode('utf-8'))
                    i.shutdown(2)
                    i.close()
                elif params[0] == 'quit':
                    browser = params[1]
                    who = params[2]
                    os.popen('taskkill -PID %d -F'%DriverList[browser][who][1])
                    DriverList[browser].pop(who)
                else:
                    i.send('0'.encode('utf-8'))
            sock_links.remove(i)
            print('---remove---')


if __name__ == '__main__':
    address = eval(sys.argv[2])

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