## 获取用户profile名称
右键Edge快捷方式，选择属性  
![img_1.png](https://github.com/srsng/little-things/blob/main/AutoRewards/img_1.png)  
在"目标"中有--profile-directory=xxx
默认为Default，或Profile 1  
profile-dir可能的值在"C:\Users\USERNAME\AppData\Local\Microsoft\Edge\User Data"  
在该路径下可以找到Default以及零个或多个Profile #文件夹，
其中#为数字，如Profile 1、Profile 2等等。
## 安装
python 版本：3.6 及以上  
安装DrissionPage模块
```shell
pip install DrissionPage
```
DrissionPage初始化参考[DrissionPage文档](http://g1879.gitee.io/drissionpagedocs/get_start/before_start/#_3)
然后根据实际情况使用drissionpage_init.py
## 使用
在main.py中把Edge浏览器用户profile名称如下形式添加到user_list中，然后运行main.py即可。
```python
user_list = ['Profile 1', 'Default', 'Profile 2', 'Profile 3']
```
### 移动搜索自动
支持移动端自动搜索，但是必须把**headless**赋值为False，即必须前台。  
因为目前的打开开发者工具并启动设备仿真（ctrl+shift+M）只能通过pyautogui发送到焦点窗口。  
DrissionPage的方式不起作用，可能是我的用法有误。  
如果有更好的有效解决方式希望告知！  
**注意**，要先登录！

## 未来
目前本人还未了解DrissionPage模块的打包方法，
所以暂时只能在本地运行，
未来（有人催的话）会尝试打包成可执行文件。
