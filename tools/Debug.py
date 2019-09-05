# >>>说明<<<
# 此工具用于打开一个调试窗口，此窗口连接到你的driver对象，
# 可以在这个新命令行窗口内，对正在跑测试脚本的页面进行调试。
# 使用场景：
#       有时候你脚本挂了，你不太了解是哪里出了问题，想对几个
# 关键的地方进行调试，但重新编辑脚本再跑的话，你需要从头开始
# 跑测试内容（重新打开浏览器，登录...），如果你的问题出现在
# 比较后面的地方，那得需要花费较长的时间去验证，非常麻烦。
#       此工具可以在你的脚本挂掉或是正在测试的情况下，接管那
# 个还未关闭的测试页面/App，并提供名为 "dr" 的WebDriver对象
# 给你调试。
# 
# 使用方法：
# import Debug
# Debug.start(driver)       //传入你的WebDriver对象,此工具需要获取session_id和command_executor._url值来创建连接
#
# 注意：
#       *selenium webdriver目前只支持firefox和chrome浏览器，其他浏览器看情况再说吧
#       *建议你在创建了webdriver.Chrome()【或是webdriver.Firefox()、appium webdriver对象】后就使用此工具
#       *需要把 Debug.py 和 ReuseSelenium.py、ReuseAppium.py 三个文件放在同一目录下

import os
import traceback

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
        cmd = "start python -i %s %s %s %s %s"%(selenium_funciton, session_id, command_executor, browser, options)
        os.system(cmd)
    return 1
        
def appium_webdriver(dr):
    try:
        session_id = dr.session_id
        command_executor = dr.command_executor._url
        desired_capabilities = str(dr.desired_capabilities)
        
        cmd = 'start python -i %s %s %s "%s"'%(appium_function, session_id, command_executor, desired_capabilities)
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