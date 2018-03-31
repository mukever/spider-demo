
import requests
import bs4


# need_detail = []
# for i in range(1,2):
#     return_content = requests.get('https://blog.csdn.net/quiet_girl/article/list/'+str(i)+'?viewmode=contents',"html.parser")
#
#     # print(return_content.content.decode('utf8'))
#     return_content_utf8 = return_content.content.decode('utf8')
#     # print(type(return_content_utf8))
#
#     bs4_html = bs4.BeautifulSoup(return_content_utf8)
#     # print(type(bs4_html))
#
#     urls = bs4_html.find_all('span',class_="link_title")
#     # print(urls[0])
#     print(urls.__len__())
#     for url in urls:
#
#         need_detail.append(url.a['href'])
# print(need_detail.__len__())
# # content_artical
# for detail in need_detail:
#     detail_response = requests.get(detail)
#     detail_content_utf8 = detail_response.content.decode('utf8')
#     # print(detail_content_utf8)
#     detail_bs4 = bs4.BeautifulSoup(detail_content_utf8)
#     title = detail_bs4.find('span',class_="link_title")
#     print(title.text)
