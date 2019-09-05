# selenium_tools
    此工具参考了这篇文章提供的方法：https://www.cnblogs.com/jhao/p/8267929.html

selenium_tools包含升两个工具：
  *Debug
  *Connect  （暂时没想好取什么名）

### Debug
  此工具用于打开一个调试窗口，此窗口连接到你的driver对象，可以在这个新命令行窗口内，对正在跑测试脚本的页面进行调试。  
使用场景：  
  有时候你脚本挂了，你不太了解是哪里出了问题，想对几个关键的地方进行调试，但重新编辑脚本再跑的话，你需要从头开始跑测试内容（重新打开浏览器，登录...），如果你的问题出现在比较后面的地方，那得需要花费较长的时间去验证，非常麻烦。  
  此工具可以在你的脚本挂掉或是正在测试的情况下，接管那个还未关闭的测试页面，并提供名为 "dr" 的WebDriver对象给你调试。  

使用方法：  
import Debug  
        Debug.start(driver)  //传入你的WebDriver对象,此工具需要获取session_id和command_executor._url值来创建连接  
注意：  
selenium webdriver目前只支持firefox和chrome浏览器，其他浏览器我基本没用过所以不考虑  
建议你在创建了webdriver.Chrome()【或是webdriver.Firefox()、appium webdriver对象】后就使用此工具  
需要把 Debug.py 和 ReuseSelenium.py、ReuseAppium.py 三个文件放在同一目录下  
      
### Connect
  此工具相当于Debug工具的反向使用，在本地创建一个socket服务端用于提供session，在服务端打开webdriver，Connect.py用于与服务端通信，获取该测试实例的session信息这样每次跑测试脚本时，就可以重复利用同一个浏览器，而不是重新打开新的浏览器。在编写测试脚本期间，需要大量重复性调试，使用此工具理论上来说应该会节省下很多时间，因为有的电脑打开浏览器真的很慢。经过精确测试，使用该工具重连到浏览器并加载到指定页面只需0.7799181938171387s，而正常打开浏览器需要4.169507741928101s;好吧，看起来是个很鸡肋的东西 (╯°Д°）╯   
使用方法:
    import connect
    webdriver = connect.webdriver()        //用此工具的webdriver替换selenium的webdriver
    dr = webdriver.Chrome()
    dr.get("https://www.baidu.com")
    dr.find_element_by_id('kw').send_keys("selenium自动化测试")  
    
#### 文本摘自《深入理解计算机系统》P27
　令人吃惊的是，在哪种字节顺序是合适的这个问题上，人们表现得非常情绪化。实际上术语“little endian”（小端）和“big endian”（大端）出自Jonathan Swift的《格利佛游记》一书，其中交战的两个派别无法就应该从哪一端打开一个半熟的鸡蛋达成一致。因此，争论沦为关于社会政治的争论。只要选择了一种规则并且始终如一的坚持，其实对于哪种字节排序的选择都是任意的。
