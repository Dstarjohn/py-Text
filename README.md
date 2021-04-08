# py-Text
>>入门使用的python爬虫小程序
# 目的
>>&nbsp;&nbsp;&nbsp;&nbsp;掌握使用IDLE开发环境进行Python语言编程、调试、运行等各个环节的基本操作，培养学生的分析问题和解决问题的实际能力。了解基于Python的数据挖掘与相关分析的技术，掌握核心数据的抓取、数据的下载，了解在数据在并发下载模式下的可视化爬虫的相关实现。同时，体验企业工作环境和工作方式，加强团队意识、交流和表达能力。
# 设计环境和所需开发工具
IDE：JetBrains PyCharm <br>
Python版本：Python3.7
   # 背景描述
>>&nbsp;&nbsp;&nbsp;&nbsp;IDLE环境，用Pycharm工具对慕课网（https://www.imooc.com/course/list?page={}）
进行课程信息的抓取，主要抓取里面的核心数据，然后进行下载，最后保存下来你需要的核心数据。随着网络的发展，万维网成为大量信息的载体，如何有效的提取你想要下载的核心数据，不同的搜索引擎是辅助人们检索信息的工具。但是万维网的数据形式丰富，图片，数据库，音频，视频多媒体数据的大量出现，通用引擎往往对这些信息含量密集且具有一定结构的数据无能为力，不能很好的发现和获取。所以就有了网络蜘蛛，也叫网络爬虫，是一种自动化浏览网络的程序，通过获取各类网站信息，访问它们的页面内容，然后进行进一步的分析下载处理，从而使我们更快的检索到我们想要的核心数据信息。这里我设计了一个爬虫程序用来抓取慕课网的所有课程的信息，并且将其下载导出excel表。
## 总体设计需要的库
>>这里用到了time，requests，BeautifulSoup主要功能是爬取网页中我么需要的核心数据，BeautifulSoup将html解析为对象进行处理，全部页面转变为字典或者数组。然后requests是发送请求和传递参数的作用，requests是python实现的简单易用的HTTP库，使用起来比urllib简洁很多，是第三方库，所以我们需要导入requests.get()用于请求目标网站，类型是一个HTTPresponse类型，pandas 是基于 Numpy 构建的含有更高级数据结构和工具的数据分析包类似于 Numpy 的核心是 ndarray，pandas 也是围绕着 Series 和 DataFrame 两个核心数据结构展开的。还有一个time，在爬取数据，防止爬取太快或次数较多，可以用来休眠时间设置，通常为友好型爬虫，numpy提供了python对多维数组对象的支持：ndarray，具有矢量运算能力，快速、节省空间。numpy支持高级大量的维度数组与矩阵运算，此外也针对数组运算提供大量的数学函数库。而在python中，通过内嵌集成re模块，可以直接调用来实现正则匹配。以下为需要导入的库：
```
import time   #导入需要的库
import requests  # 模拟http请求 和 解析内容 的包
from bs4 import BeautifulSoup
import numpy as np  # 数据展示的包
import pandas as pd
import re
```
## 项目会用到的基本函数
这里我们通过def开始函数定义紧接着就是函数名，括号里面为函数的参数，我们通过定义extra_from_one_page(page_lst)函数从慕课网第一页提取其中的内容，然后用一个tmp[]临时列表来保存字典数据，每一个课程就是一个字典数据。
```
def extra_from_one_page(page_lst): 
tmp = [] 
```
这里定义了一个search_n_pages(n)函数，n为里面的参数，将爬取n页的数据。然后用一个target = []保存n页的数据。
```
def search_n_pages(n): 
target = []
```
## 设计的基本语句
我们在定义了函数之后，用一个for循环语句来实现核心数据的抓取，这里我们在慕课网上抓取了课程的链接地址，课程的名字，课程下载人数，课程简介，课程类型，课程难度的数据信息。
```
 for i in page_lst:
    dic = {}
    itag = i.find(class_='course-card')
    dic['img'] =  'https://www.imooc.com' + itag['href']   #课程的地址
    dic['name'] = i.find(class_='course-card-name').text   # 课程名字
```
   在我们逐页抓取课程数据的课程类型信息时候，发现抓取的数据有报错，然后通过print语句输出，定位到了是24页出错，然后我们查看原网页代码，审查元素找到了其中一个课程的类型未定义，所以这里有用到了一个if语句进行判断
```
if i.find(class_='course-label'): #24页有一个课程暂未设置类型，所以进行if判断
    dic['类型'] = i.find(class_='course-label').label.text     #课程类型
else:
    dic['类型'] = '暂无类型'
```
   然后我们在抓取课程难度这个数据的时候发现课程难度和课程人数在同一个div标签下面的sapn，而且处于同级，所以我们在抓取的时候会把两个同时抓取出来，然后我们得把他们拆分开来，分别显示出来，主要是将后面一个span取出来并且导出，我们这里又使用一个for循环语句抓取课程难度和课程下载人数两个span，然后将其类型转换成str，后面利用正则表达式读取第二个课程人数span的数字，根据正则表达式包含的字符串创建模式对象，找到所有显示人数的字符串，然后用if语句对tag类型的长度判断，最后从第0位开始读取，将list类型转换成字符串类型，然后将人数这一数据抓取出来。
```
for j in i.find_all('span'):      #for循环找到所有span
    j = str(j)                    #将其类型强制转换Str
    res = r'\b\d+\b'              #利用正则读取第二个span的数字
    regs = re.compile(res)         #根据包含正则表达式的字符串创建模式对象
    tag = regs.findall(j)          #找到所有的字符串
    if len(tag)>0:                #对tag类型的长度进行判断
        tag = int(tag[0])         #在列表中从第0位开始读取，然后将list类型转换成str
    dic['人数'] = tag
```
在第二个函数名里面又用了一个for循环来发起n次请求来顺序抓取不同页数的数据信息最后将信息保存到target中，返回target。
```
for i in range(1,n):  # 发起n次的get请求，从page=1开始，0和1同一个页面
    print('page:', i)  # 跟踪进度
    target_url = template_url.format(i)
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, 'html.parser')  # 转为 bs 对象
    page_lst = soup.find_all(class_='course-card-container')  # 获取该页课程列表 #course-card-container
    target.extend(extra_from_one_page(page_lst))
```
### 设计目标
从慕课网爬取核心数据课程的信息，爬取课程链接地址，课程名字，课程人数，课程类型，课程简介，课程难度
1. 初始URL：（https://www.imooc.com/course/list?page={}）
2. 数据格式：
             课程地址-- itag['href'] <br>
             课程名字-- class_='course-card-name'<br>
             课程人数—(class_='course-card-info').span <br>
             课程类型-- (class_='course-card-info').span <br>
             课程简介—class_='course-card-desc' <br>
             课程难度-- class_='course-card-info'<br>
3. 页面编码：utf-8
