
import requests
import bs4
import json

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'Cookie':'thw=cn; t=c612c1477cd13b0fee2ec59c3bbe95bb; cna=bMNEE5PPSH0CAXkEX53yRFSX; ali_ab=121.4.95.157.1522502514639.9; _cc_=W5iHLLyFfA%3D%3D; tg=0; mt=ci=0_0; uc3=nk2=&id2=&lg2=; tracknick=; l=ArOzZKl/1fZhR5xLfx4lvVQkw7zd7Ueq; _m_h5_tk=d79f2e2511e2128714ca047d3d763c1d_1522514284415; _m_h5_tk_enc=788b00d762b149de5ddcd6d1f3e4fcf7; hng=CN%7Czh-CN%7CCNY%7C156; enc=hh8hDw13RB1t0LnV2%2BKD9YtDps%2BlPJ%2Fh8rGz7lL491eAQsZMUydyJ%2BvNZd23GxZJwKkRXjZYgvqlILzZVTj9Xw%3D%3D; cookie2=38217aeaa4e7baf4659afc56002718fc; v=0; _tb_token_=f577eee303513; isg=BCYmj6jnQHDDLBSq7ZMBiVS3d5por2taW460uxDPE8kkk8ateJe60QzC748fO2LZ'
} #替换成自己的cookie

len = 50
url = 'https://ju.taobao.com/json/tg/ajaxGetItemsV2.json?stype=samount&reverse=down&salesSite=2&type=0&psize='+str(len)+'&jview=all&actSignIds=31591065&includeForecast=true&page=1&_ksTS=1522642919752_66'
html = requests.get(url)
html_utf8  = html.content.decode('utf8')


json_str = json.loads(html_utf8)
for i in range(len):
 print('Title:'+json_str['itemList'][i]['name']['title']+
       '   Price:'+json_str['itemList'][i]['price']['actPrice']  +
       '   origPrice:'+json_str['itemList'][i]['price']['origPrice'])