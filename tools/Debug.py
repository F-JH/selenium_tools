import os
import platform
import traceback
isMac = False
if "Darwin" in platform.platform():
    import appscript
    isMac = True

# ReuseSelenium.py、ReuseAppium.py 路径
selenium_funciton = os.path.join(os.path.dirname(__file__), "ReuseSelenium.py")
appium_function = os.path.join(os.path.dirname(__file__), "ReuseAppium.py")



def selenium_webdriver(dr):
    try:
        session_id = dr.session_id
        command_executor = dr.command_executor._url
        browser = dr.capabilities['browserName']
    except Exception as err:
        traceback.print_exc()
        return err
    try:
        options = '\"((\'127.0.0.1\', %d), \'%s\')\"'%(dr.address[1], dr.who)
        options = str(options)
    except:
        options = None
        
    if browser not in ['firefox', 'chrome']:
        print("目前只支持firefox和chrome浏览器，其他浏览器有待研究")
        return
    else:
        cmd = 'start python -i "%s" %s %s %s %s'%(selenium_funciton, session_id, command_executor, browser, options)
        if isMac:
            appscript.app("Terminal").do_script(cmd)
        os.system(cmd)
    return 1
        
def appium_webdriver(dr):
    try:
        session_id = dr.session_id
        command_executor = dr.command_executor._url
        desired_capabilities = str(dr.desired_capabilities)
        
        cmd = 'start python -i "%s" %s %s "%s"'%(appium_function, session_id, command_executor, desired_capabilities)
        os.system(cmd)
        return 1
    except Exception as err:
        traceback.print_exc()
        return err
    
    
    
 
def start(dr):
    # 目前按'deviceName' 来区分selenium 和 appium，如遇到问题再观察
    try:
        if "deviceName" in dr.desired_capabilities:
            return appium_webdriver(dr)
        else:
            return selenium_webdriver(dr)
    except Exception as err:
        traceback.print_exc()
        print("请传入有效的WebDriver对象！")
        return err