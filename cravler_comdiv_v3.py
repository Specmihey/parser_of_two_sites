# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:09:06 2018

@author: @specmihey
"""

import os
import math
import openpyxl
from openpyxl import Workbook
import requests     
import numpy as np   
import pandas as pd  
import time
import re
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from fake_useragent import UserAgent
UserAgent().chrome
#your directory for files
os.chdir('C:\\Users\\user\\Documents\\Курсы Мэриленда\\Data Science Specialization\\Python_for_Beginners\\seo_Beautiful')
base_url = "http://rvi-cctv.ru"

#--------- For urls http://rvi-cctv.ru/catalog/ip_kamery_videonablyudeniya_1/
linck = "http://rvi-cctv.ru/catalog/ip_kamery_videonablyudeniya_1/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url + item)
    print (items)
#--- Объявление функций

    
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
            data = requests.get(page)
            soup = BeautifulSoup(data.text, 'html.parser')
            #soup.prettify()
            #--- получение IDs
            s = str(soup.find('ul', attrs={'class':'download-list'}))
            id_ = int(re.search('(?<=PRODUCT=)\d+',s)[0])
            
            # --- Наименование товара
            name = soup.html.head.title.text
            #soup.get_text()
            # --- Вторая цена товара
            price = soup.find_all('span', {"class":"ci-price"})
            if not price:
                price = "N/A"
            if price is "N/A":
                price_v3 = "По договоренности"
            else:
                price_v2 = str(price[1])
                numPattern = re.sub("\D", "", price_v2)
                price_v3 = int(numPattern)

            # --- получение Изображений товара
            image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
            images = image[:3]
            images = [image.attrs['href'] for image in images]
            images_base = []
            for itemImg in images:
                images_base.append(base_url+itemImg)
            images_base = images_base[0:3]
            images_base = '|'.join(images_base)
            #---требуеся цикл for
            #projects.extend(parse(get_html(base_url + "page=%d" % images)))   
            # --- Описание товара
            #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
            text_ = soup.find('div', attrs={'class':'osobennost'})
            text_body = text_.text[4:]

            #--- Таблица с характеристиками
            #soup.select('div .charact') #список объектов супа
            tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
            number_of_signs = len(soup.text) #расчет объема текста
            # save the data in tuple
            data_out.append((id_,name,price_v3,text_body,images_base,tds)) #no tuple
            # open a csv file with append, so old data will not be erased

import csv 
import codecs  
with codecs.open('index_v3.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out)  



































