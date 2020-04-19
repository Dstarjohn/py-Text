import urllib.request
import xlwt
from bs4 import BeautifulSoup
#获取HTML代码
def getHtml(url,headers={ }):
    req = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return  content
#解析HTMl数据
def get_filter_info(html):
    soup = BeautifulSoup(html,'lxml')    #lxml为解析器
    img_list = soup.select('ul#m-pl-container li div img')  #歌单封面地址链接
    title_list = soup.select('ul#m-pl-container li div a.msk')  #歌单（歌单名和歌单链接）
    pv_list = soup.select('div.bottom span.nb')          #歌单播放量
    user_list = soup.select('ul#m-pl-container li p a.nm.nm-icn.f-thide.s-fc3')  #歌单用户（名字和主页链接）
    file = xlwt.Workbook()
    table = file.add_sheet('wyy_music')
    table.write(0,0,u"歌单封面")
    table.write(0, 1, u"歌单名")
    table.write(0, 2, u"歌单链接")
    table.write(0, 3, u"播放量")
    table.write(0, 4, u"用户名")
    table.write(0, 5, u"用户主页链接")
    i = 0
    while i<len(img_list):
        table.write(i + 1, 0, img_list[i]["src"])
        table.write(i + 1, 1, title_list[i]["title"])
        table.write(i + 1, 2, title_list[i]["href"])
        table.write(i + 1, 3, pv_list[i].text)
        table.write(i + 1, 4, user_list[i]["title"])
        table.write(i + 1, 5, user_list[i]["href"])
        file.save("网易云_music.xls")
        i += 1
url = 'http://music.163.com/discover/playlist'   #playlist包含歌单文件，host：music.163.com就变成http://music.163.com/discover/playlist
html = getHtml(url,headers={
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)',    #通过设置 headers，一开始就设置一个UA
    'Host': 'music.163.com'   #有些网站会判断 host 是否是自己，所以有我们还需要加上host：music.163.com
})
get_filter_info(html)