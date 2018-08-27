import urllib.request as req
import bs4
import tools.proxyutils as pu
import os

RETRY = 3
retry_num = 1
print(os.getcwd())

testbaidu = 'https://www.cnblogs.com/cocoajin/p/3679821.html'
testdouban = 'https://book.douban.com/tag/?view=cloud'

proxy_fixed = 'https://124.89.2.250:63000'

proxies = pu.get_proxies_from_file('../tools/Proxy/Proxy 2018-06-05.txt')
proxy = pu.get_random_ip(proxies)
# print(proxy)
response = ''

# try:
#     handler = req.ProxyHandler({"https": proxy})
#     opener = req.build_opener(handler)
#     req.install_opener(opener)
#
#     response = req.urlopen("https://book.douban.com/tag/?view=cloud")
#
# except Exception as error:
#     print("Failed the first time.")
#     print(error)
#     while retry_num < RETRY:
#         try:
#             proxy = pu.get_random_ip(proxies)
#             handler = req.ProxyHandler({"http": proxy})
#             opener = req.build_opener(handler)
#             req.install_opener(opener)
#             print('retrying %s' % proxy)
#             response = req.urlopen("https://book.douban.com/tag/?view=cloud")
#         except Exception as error:
#             print("Retry %d time. with proxy %s" % (retry_num, proxy))
#             print(error)
#             retry_num += 1
#             continue


handler = req.ProxyHandler({"https": proxy_fixed})

opener = req.build_opener()  # req.build_opener(handler)
opener.addheaders = {('User-agent', 'Mozilla/5.0')}
req.install_opener(opener)
response = req.urlopen(testdouban)

soup = bs4.BeautifulSoup(response, 'html.parser')
print(soup)

print(proxies.__len__())
ip = pu.get_random_ip(proxies)
proxies.remove(ip)

print(proxies.__len__())