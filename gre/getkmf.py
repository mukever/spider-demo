# coding=utf-8
import os
import bs4
import requests
import re
import sys
import json
class Problem():

    def __init__(self):
        self.title  = ''
        self.ansowers = ''
        self.explain = ''
        self.words = ''
        self.comments = ''


def getHtmlUtf8(url):
    html = requests.get(url)
    content = html.content.decode('utf8')
    return content

def getlinks(content):
    links=[]
    html_bs4 = bs4.BeautifulSoup(content, "html.parser")
    href_attrs = html_bs4.find_all('td')
    for j in range(href_attrs.__len__()):
        # print(href_attrs[j].a['href'])
        links.append(href_attrs[j].a['href'])
    return links


def firststep(url):
    return getlinks(getHtmlUtf8(url))

def getex(url):
    content = getHtmlUtf8(url)
    bs4_content = bs4.BeautifulSoup(content, "html.parser")
    # print(bs4_content.text)
    p = Problem()
    title = bs4_content.find_all('div',class_='sub-text')
    # print(title[0].text)
    p.title = title[0].text
    answers = bs4_content.find_all('div', class_= 'sub-cont')
    p.ansowers = str(answers[0].text).replace('显示答案','')
    id = bs4_content.find_all('a',class_='js-open-error')
    qid = id[0]['data-qid']
    discuss = requests.get('http://ugcv2.kmf.com/api/gre/explain/'+qid+'/current')
    json_dis = json.loads(discuss.content.decode('utf8'))
    try:
        # print(bs4.BeautifulSoup(json_dis['result']['explain']['content']).text)
        p.explain = bs4.BeautifulSoup(json_dis['result']['explain']['content'],'html.parser').text
    except:
        pass
    # print('http://ugcv2.kmf.com/api/gre/comment/'+qid+'/list?psize=100&page=1&orderType=1&uid=0')
    try:
        comments_json = json.loads(requests.get('http://ugcv2.kmf.com/api/gre/comment/'+qid+'/list?psize=100&page=1&orderType=1&uid=0').content.decode('utf8'))
        total = comments_json['result']['pages']['total']
        for i in range(int(total)):
            # print(bs4.BeautifulSoup(comments_json['result']['item'][i]['content']).text)
            p.comments = p.comments+bs4.BeautifulSoup(comments_json['result']['item'][i]['content'],'html.parser').text+'\n'
    except json.decoder.JSONDecodeError as e:
        pass
    return p

def getPs(links):
    ps = []
    # for i in range(1):
    for i in range(links.__len__()):
        print('处理第'+str(i)+'题')
        ps.append(getex(links[i]))
    return ps
def writetotxt(ps,file,record,start):
    print('输出到文件')
    for p in ps:
        if p is None:
            continue
        info = p.title+p.ansowers+p.explain+p.comments
        print('.',end='.')
        file.write(info.encode('utf-8'))
        record.write(str(start))

if __name__ == '__main__':
    file = open('kmf.txt', 'wb+')

    record = open('record.txt','r')
    start = record.readline()
    record.close()

    record = open('record.txt', 'w')
    per_links_url = 'http://gre.kmf.com/question/tc/0?keyword=&page='
    end_links_url = ''
    # get links

    print(start)

    for i in range(int(start),293):
        print("\n*******************第 "+str(i) +"页************")
        links = firststep(per_links_url + end_links_url +str(i) )
        ps = getPs(links)
        writetotxt(ps,file,record,i+1)

    record.close()
    file.close()


