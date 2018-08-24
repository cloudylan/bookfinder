import urllib.request
import bs4
import io
import datetime
import random

proxy_url = 'http://www.xicidaili.com/wn'


class Proxy:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://%s:%s' % (self.host, self.port)


def get_random_ip(proxies):
    index = random.randint(0, proxies.__len__() - 1)
    return proxies[index]


def get_proxies_from_online(target_url):
    proxies = []
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(target_url)
    ip_list = bs4.BeautifulSoup(response, 'html.parser').find('table').find_all('tr')

    for ip in ip_list:
        detail = ip.find_all('td')
        if detail.__len__() == 0:
            continue
        proxy = Proxy(detail[1].text, detail[2].text)
        proxies.append(proxy.url + '\n')
        # proxies.append(proxy)

    # Write proxies to file.

    filename = 'Proxy/Proxy %s.txt' % str(datetime.datetime.now())[:10]

    file = io.open(filename, 'w')
    file.writelines(proxies)
    file.close()
    return filename


def get_proxies_from_file(file_path):
    file = io.open(file_path, 'r')
    proxies = file.read().split('\n')
    print('Get %d proxies from the file.' % proxies.__len__())
    file.close()
    return proxies


# get_proxies_from_file('Proxy/Proxy.txt')
# get_proxies_from_online(proxy_url)
