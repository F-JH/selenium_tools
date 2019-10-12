# selenium_tools
此工具参考了这篇文章提供的方法：https://www.cnblogs.com/jhao/p/8267929.html  
selenium_tools是基于Python的Selenium辅助测试人员调试的工具  
  
selenium_tools包含两个工具：  
* [Debug](#debug)
* [Connect](#connect) （暂时没想好取什么名）

## Debug
---
 此工具用于打开一个调试窗口，此窗口连接到你的driver对象，可以在这个新命令行窗口内，对正在跑测试脚本的页面进行调试。(也可用于Appium,使用方法相同)  
### 使用场景：  
 有时候你脚本挂了，你不太清楚是哪里出了问题，只是想修改几个地方的代码进行调试，这时候你要面临着一个问题：我只是想看这几个改动的地方，却要从头开始跑测试内容（重新打开浏览器，登录...）！而如果你的问题出现在比较后面的地方，那就要花费较长的时间去验证，非常麻烦。此工具可以在你的脚本挂掉或是正在测试的情况下，接管那个还未关闭的测试页面，并提供名为 "dr" 的WebDriver对象给你调试。  
### 使用方法：  

    import Debug
    from selenium import webdriver
    dr = webdriver.Chrome()
    Debug.start(dr)  //传入你的WebDriver,以获取session_id和command_executor._url值来重新连接到已打开的实例
    
### 注意:  
* selenium webdriver目前只支持firefox和chrome浏览器，其他浏览器我基本没用过所以不考虑  
* 建议你在创建了webdriver.Chrome()【或是webdriver.Firefox()、appium webdriver对象】后就使用此工具  
* 需要把 Debug.py 和 ReuseSelenium.py、ReuseAppium.py 三个文件放在同一目录下  
      
## Connect
---
　此工具相当于Debug工具的反向使用，在本地创建一个socket服务端用于提供session，在服务端打开webdriver，Connect.py用于与服务端通信，获取该测试实例的session信息。这样每次跑测试脚本时，就可以重复利用同一个浏览器，而不是重新打开新的浏览器。在编写测试脚本期间，需要大量重复性调试，使用此工具理论上来说应该会节省下很多时间，因为有的电脑打开浏览器真的很慢。
   
好吧，看起来是个很鸡肋的东西 (╯°Д°）╯  
### 使用方法:  

    import Connect
    webdriver = Connect.webdriver()        //使用重写过的webdriver替换selenium的webdriver
    dr = webdriver.Chrome()
    dr.get("https://www.baidu.com")

### 注意:
* 仅限脚本编写阶段，需要大量调试的时候使用！且只支持Chrome和Firefox ！
* ReuseSelenium.py 放在同一目录下，否则需要按指定目录来import
* WebDriverService.py 放在同一目录下，否则需要传入指定的具体位置

### 其他功能
#### 私有窗口:  
根据调用方的文件名(以下称为a.py)，在服务端创建一个新的浏览器窗口，之后只有a.py可以使用这个窗口。当然a.py还能使用原来的默认窗口，例如:  
a.py:

    dr1 = webdriver.Chrome()            # 使用default窗口
    dr2 = webdriver.PrivateChrome()     # 使用a.py窗口
    dr2.get("https://www.baidu.com")
    dr1.get("https://www.baidu.com")

b.py:

    dr = webdriver.Chrome()             # 使用default窗口
    dr1 = webdriver.PrivateChrome()     # 使用b.py窗口
    dr.get("https://www.baidu.com")
    dr1.get("https://www.baidu.com")
