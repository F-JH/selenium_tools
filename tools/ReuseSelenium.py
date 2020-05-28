import sys
import os, re
import socket
import traceback
import ast
try:
    import http.client as http_client
except ImportError:
    import httplib as http_client
import socket
from selenium import webdriver as Remote
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.errorhandler import ErrorHandler
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.remote.mobile import Mobile
from selenium.webdriver.remote.file_detector import FileDetector, LocalFileDetector
from selenium.webdriver.remote.command import Command

from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection

from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.firefox.remote_connection import FirefoxRemoteConnection




class Firefox_Remote(Firefox):
    def __init__(self, options=None, capabilities=None, service_url=None, session_id=None):
        if options == None:
            self.service = False
        else:
            self.service = True
            self.address = options[0]
            self.who = options[1]
        # super(Firefox_Remote, self).__init__()
        if service_url is None and session_id is None:
            raise NameError('Can not connect to "None" browser')
        
        if capabilities is None:
            capabilities = DesiredCapabilities.FIREFOX.copy()
        
        self.capabilities = dict(capabilities)
        
        self.w3c = True

        executor = FirefoxRemoteConnection(remote_server_addr=service_url)
        self.session_id=session_id
        self.command_executor = executor
        self.command_executor.w3c = self.w3c
        if type(self.command_executor) is bytes or isinstance(self.command_executor, str):
            self.command_executor = RemoteConnection(self.command_executor, keep_alive=True)
        self._is_remote = True
        self.error_handler = ErrorHandler()
        self._switch_to = SwitchTo(self)
        self._mobile = Mobile(self)
        self.file_detector = LocalFileDetector()
    def quit(self):
        """Quits the driver and close every associated window."""
        try:
            if self.service:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(self.address)
                msg = 'quit|firefox|%s' % self.who
                s.send(msg.encode('utf-8'))
                s.shutdown(2)
                s.close()
            else:
                self.execute(Command.QUIT)
        except (http_client.BadStatusLine, socket.error):
            pass
        except Exception:
            # 在此前浏览器挂掉或是原driver执行了quit()
            exit(0)
            
    def start_session(self, capabilities, browser_profile=None):
        # 重写start_session方法，不再创建新窗口
        Options = Remote.FirefoxOptions
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = Options().to_capabilities()
        


class Chrome_Remote(Chrome):
    def __init__(self, options=None, capabilities=None, service_url=None, session_id=None):
        if options == None:
            self.service = False
        else:
            self.service = True
            self.address = options[0]
            self.who = options[1]
        # super(Chrome_Remote, self).__init__(port=port)
        if service_url is None and session_id is None:
            raise NameError
        
        if capabilities is None:
            capabilities = DesiredCapabilities.CHROME.copy()
        
        self.capabilities = dict(capabilities)

        self.w3c = True

        executor = ChromeRemoteConnection(remote_server_addr=service_url)
        self.session_id=session_id
        self.command_executor = executor
        self.command_executor.w3c = self.w3c
        if type(self.command_executor) is bytes or isinstance(self.command_executor, str):
            self.command_executor = RemoteConnection(self.command_executor, keep_alive=True)
        self._is_remote = True
        self.error_handler = ErrorHandler()
        self._switch_to = SwitchTo(self)
        self._mobile = Mobile(self)
        self.file_detector = LocalFileDetector()
    def quit(self):
        """Quits the driver and close every associated window."""
        try:
            if self.service:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(self.address)
                msg = 'quit|chrome|%s' % self.who
                s.send(msg.encode('utf-8'))
                s.shutdown(2)
                s.close()
            else:
                self.execute(Command.QUIT)
        except (http_client.BadStatusLine, socket.error):
            pass
        except Exception:
            # 在此前浏览器挂掉或是原driver执行了quit()
            exit(0)
            
    def start_session(self, capabilities, browser_profile=None):
        # 重写start_session方法，不再创建新窗口
        Options = Remote.ChromeOptions
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = Options().to_capabilities()


if __name__ == '__main__':
    # 连接测试页面
    print(sys.argv[4])
    session_id = sys.argv[1]
    command_executor = sys.argv[2]
    browser = sys.argv[3]
    options = ast.literal_eval(sys.argv[4])
    if browser == 'firefox':
        dr = Firefox_Remote(options=options, service_url=command_executor, session_id=session_id)
    elif browser == 'chrome':
        dr = Chrome_Remote(options=options, service_url=command_executor, session_id=session_id)

    
    usage = \
    '''
                            |--------------------------------------------------------------------|
                            |           >>>此窗口下存在一个默认对象<dr>,可用于控制浏览器<<<          |
                            |   如:  dr.find_element_by_id("xxx").send_keys("xxx")               |
                            |        dr.get("http://www.baidu.com")                              |
                            |--------------------------------------------------------------------|
    '''
    print(usage)
