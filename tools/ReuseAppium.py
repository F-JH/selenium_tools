import sys
import ast
from appium import webdriver
from appium.webdriver.webdriver import WebDriver as Remote
from selenium.webdriver.remote.command import Command as RemoteCommand


class wd(Remote):
    def __init__(self, command_executor, session_id, desired_caps, capabilities):
        self.r_capabilities = capabilities
        super(wd, self).__init__(command_executor, desired_caps)
        self.session_id = session_id
        self.w3c = True
        
    def start_session(self, capabilities, browser_profile=None):
        """Creates a new session with the desired capabilities.

        Override for Appium

        Args:
            automation_name: The name of automation engine to use.
            platform_name: The name of target platform.
            platform_version: The kind of mobile device or emulator to use
            app: The absolute local path or remote http URL to an .ipa or .apk file, or a .zip containing one of these.

        Read https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/caps.md for more details.
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException('Capabilities must be a dictionary')
        if browser_profile:
            if 'moz:firefoxOptions' in capabilities:
                capabilities['moz:firefoxOptions']['profile'] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        # parameters = self._merge_capabilities(capabilities)
        #
        # response = self.execute(RemoteCommand.NEW_SESSION, parameters)
        # if 'sessionId' not in response:
        #     response = response['value']
        # self.capabilities = response.get('value')
        #
        # # if capabilities is none we are probably speaking to
        # # a W3C endpoint
        # if self.capabilities is None:
        #     self.capabilities = response.get('capabilities')

        self.capabilities = self.r_capabilities # 不再创建新窗口
        
        
if __name__=="__main__":
    try:
        session_id = sys.argv[1]
        command_executor = sys.argv[2]
        desired_capabilities = ast.literal_eval(sys.argv[3])
        
        desired_caps = {}
        desired_caps['platformName'] = desired_capabilities['platformName']
        desired_caps['platformVersion'] = desired_capabilities['platformVersion']
        desired_caps['deviceName'] = desired_capabilities['deviceName']
        desired_caps['appPackage'] = desired_capabilities['appPackage']
        desired_caps['appActivity'] = desired_capabilities['appActivity']
        dr = wd(command_executor, session_id, desired_caps, desired_capabilities)
        usage = \
        '''
                        |--------------------------------------------------------------------|
                        |           >>>此窗口下可使用 dr 对象进行调试<<<                     |
                        |   如:  dr.find_element_by_id("xxx").send_keys("xxx")               |
                        |        dr.get("http://www.baidu.com")                              |
                        |--------------------------------------------------------------------|
        '''
        print(usage)
    except Exception as err:
        print(type(err), err)
        print("出现错误，dr已不可用")
