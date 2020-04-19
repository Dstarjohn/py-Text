import time   #导入需要的包
import requests  # 模拟http请求 和 解析内容 的包
from bs4 import BeautifulSoup
import numpy as np  # 数据展示的包
import pandas as pd
M = 0 # 设置点击量阈值
template_url = "https://tieba.baidu.com/f?kw=%E5%BF%83%E7%90%86%E5%AD%A6&ie=utf-8&pn={}" # get请求模版,{ }为占位符，方便发送不同页面（第n页）的请求。
def extra_from_one_page(page_lst):    #从第一页提取帖子
    tmp = []    # 临时列表保存字典数据，每一个帖子都是一个字典数据
    for i in page_lst:
        if int(i.find(class_='threadlist_rep_num').text) > M:  # 判断是否超过阈值
            dic = {}
            dic['num'] = int(i.find(class_='threadlist_rep_num').text)  # 点击量
            dic['name'] = i.find(class_='threadlist_title').text   # 帖子名称
            dic['address'] = 'https://tieba.baidu.com' + i.find(class_='threadlist_title').a['href']  # 帖子地址
            tmp.append(dic)    #将字典中对象添加进去
            sorted (dic.keys())
    return tmp
def search_n_pages(n): #爬取n页的数据
    target = []        #爬取n页的数据
    for i in range(n):  # 发起n次的get请求
        print('page:', i)  # 跟踪进度
        target_url = template_url.format(50*i) # 按照浏览贴吧的自然行为，每一页50条
        res = requests.get(target_url)
        soup = BeautifulSoup(res.text, 'html.parser')  # 转为 bs 对象
        page_lst = soup.find_all(class_='j_thread_list')  # 获取该页帖子列表
        target.extend(extra_from_one_page(page_lst))   # 该页信息保存到target
        time.sleep(0.2)   # 休息0.2秒再访问，友好型爬虫
    return target
d = search_n_pages(3)  # 爬取贴吧前200页数据
data = pd.DataFrame(d)  # 转化为pandas.DataFrame对象
data.to_excel('心理学-贴吧.xlsx') # 导出到excel表格