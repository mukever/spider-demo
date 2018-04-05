# coding=utf-8
import os
import bs4
import requests
import re
import sys

class Problem():

    def __init__(self):
        self.title  = ''
        self.ansowers = ''
        self.explain = ''
        self.words = ''


def getHtmlUtf8(url):
    html = requests.get(url)
    content = html.content.decode('utf8')
    return content

def getlinks(content):
    links=[]
    html_bs4 = bs4.BeautifulSoup(content, "html.parser")
    href_attrs = html_bs4.find_all("div", class_="content pull-right")
    for j in range(href_attrs.__len__()):
        links.append(href_attrs[j].p.a['href'])
    return links


def firststep(url):
    return getlinks(getHtmlUtf8(url))

def getex(url):
    content = getHtmlUtf8(url)
    bs4_content = bs4.BeautifulSoup(content, "html.parser")
    # print(bs4_content.text)
    p = Problem()
    text = bs4_content.text
    sub1 = text.find('题目')
    sub2 =text.find('正确答案')
    sub3 =text.find('题目解析')
    sub4 =text.find('词汇含义')
    sub5 = text.find('如何使用好GRE填空500题')
    title = text[sub1+85:sub2]
    # print(text[sub2:sub3])
    answers = text[sub2:sub3]
    # print(text[sub3:sub4])
    expalain = text[sub3:sub4]
    # print(text[sub4:sub5])
    words = text[sub4:sub5]
    p.title = title
    p.ansowers = answers
    p.explain  =expalain
    p.words  =words
    if sub1 ==-1 or sub2 ==-1 or sub3 ==-1 or sub4 ==-1 or sub5 ==-1:
        return None
    return p

def getPs(links):
    ps = []
    for link in links:
        # print(link)
        ps.append(getex(link))
    return ps
def writetotxt(ps,file):
    for p in ps:
        if p is None:
            continue
        print('writing....')
        info = p.title+p.ansowers+p.explain+p.words
        # print(p.title)
        file.write(info.encode('utf-8'))

if __name__ == '__main__':
    file = open('f.txt', 'wb+')
    per_links_url = 'http://gre.zhan.com/tiankong/liebiao'
    end_links_url = '.html'
    # get links
    for i in range(12):
        links = firststep(per_links_url + str(i) + end_links_url)
        print(links)
        ps = getPs(links)
        print(ps)
        writetotxt(ps,file)

    file.close()


