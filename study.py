import urllib.request
data = urllib.request.urlopen("http://tieba.baidu.com/p/2460150866").read()
data = data.decode('UTF-8')
print(data)