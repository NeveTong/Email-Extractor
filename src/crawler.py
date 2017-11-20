###############################
# Download Google result page
###############################

import util
import myparser
import requests
import time
import constant
import json

class Proxy:
        
    ip_info = {}
    
    with open(constant.IP_INFO_PATH) as f:
        ip_info = json.load(f)   
    
    @classmethod
    def choose_proxy(cls):
        proxies_list = sorted(cls.ip_info.items(), key=lambda item:item[1][0])
        print(proxies_list)
        print(proxies_list[0][0])
        return proxies_list[0][0]
       
    @classmethod
    def modify_proxy_info(cls, proxy_ip, flag):
        if flag == -1:
            cls.ip_info.get(proxy_ip)[0] += 1
        else:
            cls.ip_info.get(proxy_ip)[0] += 1
            cls.ip_info.get(proxy_ip)[1] += 1
        print(cls.ip_info)
        with open(constant.IP_INFO_PATH, 'w') as wf:
            json.dump(cls.ip_info, wf, indent=4)
           


def download_page(url, useproxy=True, verbose=True, maxtry=999, timeout=5, checkpage=True):

    def retry():
        if verbose:
            print('[FAIL-{}] {} -> {}'.format(maxtry, proxy_ip, url))
        return download_page(url, useproxy, verbose, maxtry - 1, timeout, checkpage)

    if maxtry <= 0:
        return None
    try:
        proxy = None
        proxy_ip = 'localhost'
        if useproxy:
            proxy_ip = Proxy.choose_proxy()
            proxy = {
                'http': proxy_ip,
                'https': proxy_ip,
            }
        header = {
            'user-agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'
        }
        r = requests.get(url, proxies=proxy, headers=header)
#        time.sleep(10)
        content = r.text
        statuscode = r.status_code
        print('content:')
        print(content)
        if checkpage:
            try:
                snippets = myparser.parse(content)
                if not snippets and statuscode != 200:
                    print('1')
                    raise Exception
            except:
                print('2')
                raise Exception

        if verbose:
            print('[OK] {} -> {}'.format(proxy_ip, url))
            if useproxy:
                Proxy.modify_proxy_info(proxy_ip, 1)
            
        return content

    except Exception as e:
        print('Exception:')
        print(e)
        if useproxy:
            Proxy.modify_proxy_info(proxy_ip, -1)
        return retry()


@util.cache('text')
def search(query, useproxy=True, verbose=True, maxtry=99, timeout=5, checkpage=True):
    query = query.replace(' ', '+')
    print(query)
    url = 'https://www.google.com/search?hl=en&safe=off&q={}'.format(query)
    page = download_page(url, useproxy, verbose, maxtry, timeout, checkpage)
    return page


if __name__ == '__main__':
    names = [
        'jiawei han',
        'thorsten joachims'
    ]
    for name in names:
        with open('{}.html'.format(name), 'w', encoding='utf-8') as wf:
            page = search(name, usecache=True, cache='{}.html'.format(name.replace(' ', '')))
            wf.write(page)
