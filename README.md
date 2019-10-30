# selenium_tools
此工具参考了这篇文章提供的方法：https://www.cnblogs.com/jhao/p/8267929.html  
selenium_tools支持Python平台上的Selenium，用于辅助测试人员调试的一些工具  
  
selenium_tools包含两个工具：  
* [Debug](#debug)
* [WebDriverManager](#webdrivermanager) 

## Debug
---
 此工具用于打开一个调试窗口，此窗口连接到你的driver对象，可以在这个新命令行窗口内，对正在跑测试脚本的页面进行调试。(也可用于Appium,使用方法相同)  
### 使用场景：  
 有时候你脚本挂了，你不太清楚是哪里出了问题，只是想修改几个地方的代码进行调试，这时候你要面临着一个问题：我只是想看这几个改动的地方，却要从头开始跑测试内容（重新打开浏览器，登录...）！而如果你的问题出现在比较后面的地方，那就要花费较长的时间去验证，非常麻烦。此工具可以用在你的脚本挂掉或是正在测试的情况下，连接到那个还未关闭的测试页面，并开启一个命令行窗口以提供调试，你可以在此窗口下用dr(此窗口下的WebDriver对象)来控制你的测试页面！
### 使用方法：  

    # 将Debug.py、ReuseSelenium.py、ReuseAppium.py与你的脚本文件放在同一目录下，或者自己想办法导入Debug，别说这个也不会啊
    
    
    import Debug
    from selenium import webdriver
    dr = webdriver.Chrome()
    Debug.start(dr)  # 传入你的WebDriver,以获取session_id和command_executor._url值来重新连接到已打开的实例
    
### 注意:  
* selenium webdriver目前只支持firefox和chrome浏览器，其他浏览器我基本用不到所以不考虑，各位可以结合大佬们的文章自行研究  
* 建议你在创建了webdriver.Chrome()【或是webdriver.Firefox()、appium webdriver对象】后就使用此工具  
* 需要把 Debug.py 和 ReuseSelenium.py、ReuseAppium.py 三个文件放在同一目录下  
      
## WebDriverManager
---
　此工具相当于Debug工具的反向使用，在本地创建一个socket服务端用于管理webdriver，并提供sessionid，Connect.py用于与服务端通信，获取该测试实例的session信息。这样每次跑测试脚本时，就可以重复利用同一个浏览器，而不是重新打开新的浏览器。在编写测试脚本期间，需要大量重复性调试，使用此工具理论上来说应该会节省下很多时间，因为有的电脑打开浏览器真的很慢。
   
好吧，看起来好像并没什么卵用 (╯°Д°）╯  
### 使用方法:  

    # 将Connect.py、ReuseSelenium.py和WebDriverService.py与你的脚本文件放在同一目录下，或者自己想办法导入Connect，别说这个也不会啊
    
    
    import Connect
    webdriver = Connect.webdriver()        # 使用重写过的webdriver替换selenium的webdriver
    dr = webdriver.Chrome()
    dr.get("https://www.baidu.com")
    # 开启无图模式，加载网页时不加载图片，让测试脚本跑的更快! 当然你有需求要看图片就别开，默认关闭
    dr1 = webdriver.Chrome(no_img=True)

### 注意:
* 仅限脚本编写阶段，需要大量调试的时候使用！且只支持Chrome和Firefox ！
* ReuseSelenium.py 放在与Connect.py一目录下，否则需要按指定目录来import
* WebDriverService.py 放在与Connect.py同一目录下，否则需要传入指定的具体位置
* <font color=#F00>由于是服务端开启的WebDriver，而目前想不到办法在进程通讯间传递对象，所以一些骚操作(给webdriver传递一些个人配置)无法完成，只能用用普通的操作。也正如前面所说的，这并没有什么卵用，只能增加一些逼格。</font>

### 其他功能
#### 私有窗口:  
根据调用方的文件名(以下称为a.py)，在服务端创建一个新的浏览器窗口，之后只有a.py可以使用这个窗口。当然a.py还能使用原来的默认窗口，例如:  
a.py:

    dr1 = webdriver.Chrome()            # 使用default窗口
    dr2 = webdriver.PrivateChrome()     # 使用a.py窗口
    dr2.get("https://www.baidu.com")
    dr1.get("https://www.baidu.com")
    # 无图模式
    dr2 = webdriver.PrivateChrome(no_img=True)

b.py:

    dr = webdriver.Chrome()             # 使用default窗口
    dr1 = webdriver.PrivateChrome()     # 使用b.py窗口
    dr.get("https://www.baidu.com")
    dr1.get("https://www.baidu.com")
