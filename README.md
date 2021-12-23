#### 学习Python时候写的一个小程序，小白一个，不足之处还请大佬们多多指教；

## 关于程序的使用说明
#### 两个.bat文件都是windows的批处理文件，可以写入windows的计划任务中
#### 其中auto_daka.py 与 benke_daka.py 分别为研究生打卡程序和本科生打卡程序，里面需要填写你的邮箱账号以及密码，如果不需要给你发消息，可以注释掉发送邮件那部分。
#### 两个.exe文件为selenium驱动程序文件，建议使用phantomjs驱动（隐式浏览器），如果使用chromedrive.exe需要注意自己电脑谷歌浏览器版本，在百度找到适合自己谷歌版本的驱动，网址（https://npm.taobao.org/mirrors/chromedriver）。

#### 如果想让程序每天到点自动运行，可以放在自己的电脑上，写在计划任务里面，也可以放在服务器上，这里推荐阿里云服务器，学生可以免费领取两个月哈哈哈



#### 白嫖的服务器到期了，移植到了另外一个服务器上，出现问题：

```shell
Python: 'module' object has no attribute 'PhantomJS'
```

但是在之前那个服务器上可以运行；

发现是版本的问题：

```shell
#新的服务器的selenium的版本是最新版，我将该版本卸载重新安装之前的版本就行了。
# 方法
pip uninstall selenium
pip install selenium==3.41.0
# ok 结束，可以正常运行
pip freeze #查看每个安装包的版本
```

