
# coding: utf-8

# In[1]:

import requests
import bs4 as BeautifulSoup
import xlwings as xw
import lxml
import time
import math


# In[9]:

page = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225]

wb = xw.Book(r'C:\users\duro\Douban_250.xlsx')
sht = wb.sheets['Top250']
sht.range("A1").value = "Movie title"
sht.range("B1").value = "Other title"
sht.range("C1").value = "Description"
sht.range("D1").value = "Ranking"
sht.range("E1").value = "Quote"

step = 25
for item in page:
    url = "https://movie.douban.com/top250?start=" + str(item) + "&filter="
    r = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(r.content, "lxml")
    g_data = soup.find_all("div", {"class":"hd"})
    h_data = soup.find_all("p", {"class": ""})
    i_data = soup.find_all("span", {"class": "rating_num"})
    j_data = soup.find_all("span", {"class": "inq"})
    
    # this is write movie title into excel
    a = item + 2
    it_no = 0 
    for item_0 in g_data:
        sht.range("A" + str(a)).value = g_data[it_no].find_all("span", {"class": "title"})[0].text
        it_no += 1
        a = a + 1
        print(item_0.text)
    
    # this is to write movie description into excel
    b = item + 2
    for item_1 in h_data:
        sht.range("C" + str(b)).value = item_1.text
        b = b + 1
        print(item_1.text)
    
    # this is to write movie ranking into excel
    c = item + 2
    for item_2 in i_data:
        sht.range("D" + str(c)).value = item_2.text
        c = c + 1
        print(item_2.text)
    
    # this is to write movie quote into excel
    d =item + 2
    for item_3 in j_data:
        sht.range("E" + str(d)).value = item_3.text
        d = d + 1
        print(item_3.text)
    
    wb.save()
    time.sleep(10)

wb.close()


# In[ ]:




# In[ ]:



