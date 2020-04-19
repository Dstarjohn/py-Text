import re
import requests
from bs4 import BeautifulSoup
def book(target_url):
    books = []
    book = requests.get(target_url) #使用requests返回网页的整体结构
    soup = BeautifulSoup(book.text, 'lxml') # 使用lxml作为解析器，返回一个Beautifulsoup对象
    table = soup.findAll('table', {"width": "100%"}) #找到其中所有width=100%的table标签），即找到所有的书
    for item in table: #遍历table，一个item代表一本书
        name = item.div.a.text.strip() #找到书名
        r_name = name.replace('\n', '').replace(' ', '') #通过看网页的HTML结构，可以发现书名后是有换行以及空格的，将这些全部通过replace替换去除
        tmp2 = item.div.span  #判断是否存在别名
        if tmp2:
            name2 = tmp2.text.strip().replace(':', '') #因为是通过div.span判断别名 有些书的别名前面有个冒号，比如《三体系列》
        else:
            name2 = r_name #无别名就使用原始的名称
        url = item.div.a['href'] #获取书的链接
        info = item.find('p', {"class": "pl"}).text #获取书的信息
        score = item.find('span', {"class": "rating_nums"}).text.strip() #获取分数
        nums = item.find('span', {"class": "pl"}).text.strip() # 获取评价人数
        num = re.findall('(\d+)人评价', nums)[0]  # 通过正则取具体的数字
        if item.find('span', {"class": "inq"}): # 判断是否存在描述
            desc = item.find('span', {"class": "inq"}).text.strip()
        else:
            desc = 'no description'
        books.append((r_name, name2, url, info, score, num, desc)) #以元组存入列表
    return books #返回一页的书籍
for n in range(10):
    url1 = 'https://book.douban.com/top250?start=' + str(n*25) #top250的网页，每页25本书，共10页，“start=”后面从0开始，以25递增
    tmp = book(url1)
    with open('booktop250.xls', 'a', encoding='utf-8') as d: #新建一个文件存放数据，模式取'a'，表示在后面追加；编码一定要写上，因为win下新建文件，默认是gbk编码，但是前面返回的结构是unicode的，会报编码错误
        for i in tmp:
            print(i[0]+"\t"+i[1]+"\t"+i[2]+"\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\t"+i[6], file=d)