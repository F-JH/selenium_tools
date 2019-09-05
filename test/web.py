from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

class reRemoteConnection(RemoteConnection):
    def __init__(self, *args, **kwargs):
        super(reRemoteConnection, self).__init__(*args, **kwargs)

    def execute(self, command, params):
        """
        Send a command to the remote server.

        Any path subtitutions required for the URL mapped to the command should be
        included in the command parameters.

        :Args:
         - command - A string specifying the command to execute.
         - params - A dictionary of named parameters to send with the command as
           its JSON payload.
        """
        print(params)
        command_info = self._commands[command]
        assert command_info is not None, 'Unrecognised command %s' % command
        path = string.Template(command_info[1]).substitute(params)
        if hasattr(self, 'w3c') and self.w3c and isinstance(params, dict) and 'sessionId' in params:
            del params['sessionId']
        data = utils.dump_json(params)
        url = '%s%s' % (self._url, path)
        return self._request(command_info[0], url, body=data)

class webdriver(WebDriver):
    def __init__(self, *args, **kwargs):
        super(webdriver, self).__init__(*args, **kwargs)
        self.command_executor = command_executor
        if type(self.command_executor) is bytes or isinstance(self.command_executor, str):
            self.command_executor = reRemoteConnection(command_executor, keep_alive=keep_alive)


if __name__ == '__main__':
    dr = webdriver(executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True)
    dr.get('https://www.baidu.com')
    a = dr.find_element_by_id('kw')

    dr.implicitly_wait()