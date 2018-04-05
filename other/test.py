import requests

headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.baidu.com/'
           }


print(requests.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=你好'
                   '&oq=%25E7%2588%25AC%25E8%2599%25AB%25E8%25AF%25B7%25E6%25B1%2582%25E5%25A4%25B4&rsv_pq=a8df7e1a0002744d&rsv_t=98a2E5%2F135%2BvZJATB4w7rLq0d4n2%2F20G7xSMZILwDxhURpmSPXJVw2LGYG8&rqlang=cn&rsv_enter=1&rsv_sug3=2&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&inputT=214&rsv_sug4=782&rsv_sug=1&rsv_jmp=slow',headers).content.decode('utf8'))