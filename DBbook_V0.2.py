
# coding: utf-8

# In[1]:

# Initiating crawler

import numpy as np
import pandas as pd
import requests
import bs4 as BeautifulSoup
import time
import csv
import sys
import random

filename = 'DoubanBook.csv'
proxy_file = 'proxy.txt'


# book_tag_list = {"小说": ['小说','外国','文学','随笔','中国文学','经典','日本文学','散文','村上春树','诗歌','童话','杂文','王小波','古典文学','儿童文学','名著','张爱玲','余华','当代文学','钱钟书','外国名著','鲁迅','诗词','茨威格','米兰·昆德拉','杜拉斯','港台'],
#                  "流行": ['漫画','绘本','推理','青春','言情','科幻','东野圭吾','悬疑','武侠','奇幻','韩寒','日本漫画','耽美','亦舒','三毛','推理小说','网络小说','安妮宝贝','郭敬明','穿越','金庸','轻小说','阿加莎·克里斯蒂','几米','魔幻','青春文学','科幻小说','张小娴','幾米','J.K.罗琳','高木直子','古龙','沧月','落落','张悦然','校园'],
#                  "文化": ['历史','心理学','哲学','传记','文化','社会学','艺术','设计','社会','政治','建筑','宗教','电影','数学','政治学','回忆录','中国','历史','思想','国学','音乐','人文','人物','传记','绘画','戏剧','艺术史','佛教','军事','西方','哲学','二战','近代史','考古','自由主义'],
#                  "生活": ['美术','爱情','旅行','生活','成长','励志','心理','摄影','女性','职场','美食','教育','游记','灵修','健康','情感','手工','两性','养生','人际关系','家居','自助游'],
#                  "经管": ['经济学','管理','经济','商业','金融','投资','营销','创业','理财','广告','股票','企业史','策划'],
#                  "科技": ['科普','互联网','编程','科学','交互设计','用户体验','算法','web','科技','UE','通信','交互','UCD','神经网络','程序']}



book_tag_list = {"小说": ['散文','村上春树','诗歌','童话','杂文','王小波','古典文学','儿童文学','名著','张爱玲','余华','当代文学','钱钟书','外国名著','鲁迅','诗词','茨威格','米兰·昆德拉','杜拉斯','港台'],
                 "流行": ['漫画','绘本','推理','青春','言情','科幻','东野圭吾','悬疑','武侠','奇幻','韩寒','日本漫画','耽美','亦舒','三毛','推理小说','网络小说','安妮宝贝','郭敬明','穿越','金庸','轻小说','阿加莎·克里斯蒂','几米','魔幻','青春文学','科幻小说','张小娴','幾米','J.K.罗琳','高木直子','古龙','沧月','落落','张悦然','校园'],
                 "文化": ['历史','心理学','哲学','传记','文化','社会学','艺术','设计','社会','政治','建筑','宗教','电影','数学','政治学','回忆录','中国','历史','思想','国学','音乐','人文','人物','传记','绘画','戏剧','艺术史','佛教','军事','西方','哲学','二战','近代史','考古','自由主义'],
                 "生活": ['美术','爱情','旅行','生活','成长','励志','心理','摄影','女性','职场','美食','教育','游记','灵修','健康','情感','手工','两性','养生','人际关系','家居','自助游'],
                 "经管": ['经济学','管理','经济','商业','金融','投资','营销','创业','理财','广告','股票','企业史','策划'],
                 "科技": ['科普','互联网','编程','科学','交互设计','用户体验','算法','web','科技','UE','通信','交互','UCD','神经网络','程序']}



# In[2]:

def list_fr_tag(book_tag):
#     outfile = open(filename, 'w', encoding='utf-8')
#     writer = csv.writer(outfile)
    proxies = [{"http": '58.59.155.200:8118',"https": '58.59.155.200:8118'},
               {"http": '61.191.173.31:808', "https": '61.191.173.31:808'},
               {"http": '221.216.94.77:808', "https": '221.216.94.77:808'},
               {"http": '115.202.174.88:808', "https": '115.202.174.88:808'},
               {"http": '119.5.1.4:808', "https": '119.5.1.4:808'},
               {"http": '115.220.6.196:808', "https": '115.220.6.196:808'},
               {"http": '122.241.195.124:808', "https": '122.241.195.124:808'},
               {"http": '183.32.88.152:808', "https": '183.32.88.152:808'},
               {"http": '220.174.43.103:8118', "https": '180.175.1.133:63000'},
               {"http": '119.5.0.46:808', "https": '119.5.0.46:808'},
               {"http": '60.214.118.170:63000', "https": '60.214.118.170:63000'},
               {"http": '175.155.25.19:808', "https": '175.155.25.19:808'},
               {"http": '115.202.184.73:808', "https": '115.202.184.73:808'}]
    page_num = 0
    try_times = 0
    book_list = []
    hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
         {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
         {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}] 
    while(1):
        url = 'https://www.douban.com/tag/' + book_tag + '/book?start=' + str(page_num*15)  #select one page to list
        proxy_no = np.random.randint(0,13)
        try: 
            # url = 'https://www.douban.com/tag/当代文学/book?start=0' [test url]
            r = requests.get(url, headers = hds[page_num%len(hds)]) # proxies = proxies[proxy_no]
            # print(r.content)
            time.sleep(np.random.rand()*20)
            soup = BeautifulSoup.BeautifulSoup(r.content, 'lxml')
            # print(soup)
        except(requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ConnectTimeout):
            print("Connection Error, Quit")

        g_data = soup.find_all("div", {"class": 'mod book-list'})
        h_data = g_data[0].find_all("dl")

        try_times += 1
        if not len(h_data) and try_times <5:  #To jump out of the loop when there's no book info.
            continue
        elif not len(h_data) and try_times >5:
            print('we jumped out!')
            break

        for book in h_data:  # Select each book item from single page [3rd degree loop]
            try:
                title = book.find_all("a", {"class": 'title'})[0].text
            except:
                title = 'N.A.'
            try:
                link = book.find_all("a", {"class": 'title'}, href = True)[0]['href']
            except:
                link = 'N.A.'
            try:
                desc = book.find_all("div", {"class": 'desc'})[0].text
            except:
                desc = 'N.A.'
            desc_clean = desc.strip()
            desc_list = desc_clean.split("/")
            try:
                rating_nums = book.find_all("span", {"class": 'rating_nums'})[0].text
            except:
                rating_nums = 'N.A.'
            try:
                author ="/".join(desc_list[0:-3])
            except:
                author = 'N.A.'
            try:
                publisher = desc_list[-3]
            except:
                publisher = 'N.A.'
            try:
                pub_year = desc_list[-2]
            except:
                pub_year = 'N.A.'
            try:
                price = desc_list[-1]
            except:
                price = 'N.A.'
            #book_list.append([title, author, publisher, pub_year, price, link])
            write_result(title, author, publisher, pub_year, price, link)
            try_times = 0
        print(book_tag + " page:" + str(page_num) + "is done.")
        page_num += 1
    return(book_list)


# In[ ]:

def write_result(title, author, publisher, pub_year, price, link):
    result = 'title' + title + 'author' + author + 'publisher' + publisher + 'pub_year' + pub_year + 'price' + price + 'link' + link
    item = [title, author, publisher, pub_year, price, link]
    csvfile = open(filename, 'a', encoding = 'utf-8')
    writer = csv.writer(csvfile, dialect = 'excel')
    writer.writerow(item)
    csvfile.close()
    #print('saved:' + result)


# In[ ]:




# In[ ]:

if __name__=='__main__':
    for item in book_tag_list:    #select one category from book_tag_list [1st degree loop]
        tag_list = book_tag_list[item]
        for book_tag in tag_list:        #select one book_tag from one category [2nd degree loop]
            list_fr_tag(book_tag)


# In[ ]:




# In[ ]:



