import time   #导入需要的包
import requests  # 模拟http请求 和 解析内容 的包
from bs4 import BeautifulSoup
import numpy as np  # 数据展示的包
import pandas as pd
import re
M = 0 # 设置点击量阈值
template_url = "https://www.imooc.com/course/list?page={}" # get请求模版,{ }为占位符，方便发送不同页面（第n页）的请求。
def extra_from_one_page(page_lst):    #从第一页提取课程
    tmp = []    # 临时列表保存字典数据，每一个课程都是一个字典数
    for i in page_lst:
        dic = {}
        itag = i.find(class_='course-card')
        dic['img'] =  'https://www.imooc.com' + itag['href']   #课程的地址
        dic['name'] = i.find(class_='course-card-name').text   # 课程名字
        dic['简介'] = i.find(class_='course-card-desc').text    #课程简介
        if i.find(class_='course-label'):                  #24页有一个课程暂未设置类型，所以进行if判断
            dic['类型'] = i.find(class_='course-label').label.text     #课程类型
        else:
            dic['类型'] = '暂无类型'
        dic['难度'] = i.find(class_='course-card-info').span.text  #课程等级
        for j in i.find_all('span'):      #for循环找到所有span
            j = str(j)                    #将其类型强制转换Str
            res = r'\b\d+\b'              #利用正则读取第二个span的数字
            regs = re.compile(res)         #根据包含正则表达式的字符串创建模式对象
            tag = regs.findall(j)          #找到所有的字符串
            if len(tag)>0:                #对tag类型的长度进行判断
                tag = int(tag[0])         #在列表中从第0位开始读取，然后将list类型转换成str
            dic['人数'] = tag
        tmp.append(dic)    #将字典中对象添加进去
        sorted (dic.keys())
    return tmp
def search_n_pages(n): #爬取n页的数据
    target = []        #爬取n页的数据
    for i in range(1,n):  # 发起n次的get请求，从page=1开始，0和1同一个页面
        print('page:', i)  # 跟踪进度
        target_url = template_url.format(i)
        res = requests.get(target_url)
        soup = BeautifulSoup(res.text, 'html.parser')  # 转为 bs 对象
        page_lst = soup.find_all(class_='course-card-container')  # 获取该页课程列表 #course-card-container
        target.extend(extra_from_one_page(page_lst))   # 该页信息保存到target
        time.sleep(0.2)   # 休息0.2秒再访问，友好型爬虫
    return target
d = search_n_pages(33)  # 爬取慕课网前2页数据
data = pd.DataFrame(d)  # 转化为pandas.DataFrame对象
data.to_excel('慕课.xlsx') # 导出到excel表格