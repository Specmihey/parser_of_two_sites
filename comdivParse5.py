# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:06:07 2018

@author: @specmihey
"""
import logging
import os
import math
import openpyxl
from openpyxl import Workbook
import requests     
import numpy as np   
import pandas as pd
import re
from bs4 import BeautifulSoup
import urllib.request
import csv 
import codecs
import datetime
from fake_useragent import UserAgent
UserAgent().chrome
os.listdir('.')
base_url_rvi_cctv = "https://rvi-cctv.ru"
cataloge_v1 = "N/A"
#========================================================= IP-видеонаблюдение
linck = "https://rvi-cctv.ru/catalog/ip_videonablyudenie/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_rvi_cctv + item)  
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
        data = requests.get(page)
        soup = BeautifulSoup(data.text, 'html.parser')
        # --- Вторая цена товара
        price_ci = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['ci-price'])
        if not price_ci:
            price_ci = "N/A"
        if price_ci is "N/A":
            continue
        else:
            price_v2 = []
            for i in price_ci:
                price_v1 = re.sub("\D", "", str(i))
                price_v2.append((int(price_v1)))
                price = min(price_v2)        
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = str(soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['crumbs']))
        subdirectory_li = re.findall(r'title="\w+',subdirectory)
        subdirectory_li_text = []
        for o in subdirectory_li:
            subdirectory_li_text.append(re.sub(r'title="',"",o))
        cataloge_v2 = subdirectory_li_text[0]
        cataloge_v3 = subdirectory_li_text[1]
        cataloge_v4 = subdirectory_li_text[2]
        # --- Наименование товара
        name = soup.html.head.title.text
        #soup.get_text()

        # --- получение Изображений товара
        image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
        images = image[:3]
        images = [image.attrs['href'] for image in images]
        images_base = []
        for itemImg in images:
            images_base.append(base_url_rvi_cctv+itemImg)
        images_base = images_base[0:3]
        images_base = '|'.join(images_base)

        # --- Описание товара
        #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
        text_ = soup.find('div', attrs={'class':'osobennost'})
        text_body = text_.text[4:]

        #--- Таблица с характеристиками
        #soup.select('div .charact') #список объектов супа
        tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
        number_of_signs = len(soup.text) #расчет объема текста
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
datetime.datetime.now() 
now = datetime.datetime.now() 
folder_v1 = now.strftime('%Y%m%d-%H-%M-%S')
path = folder_v1
os.makedirs(path)
os.chdir(path) #смена текущей директории.        
with codecs.open('rvi-cctv-1.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out) 
#=========================================================== HD-аналоговое видеонаблюдение
linck = "https://rvi-cctv.ru/catalog/hd_analogovoe_videonablyudenie/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_rvi_cctv + item)  
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
        data = requests.get(page)
        soup = BeautifulSoup(data.text, 'html.parser')
        # --- Вторая цена товара
        price_ci = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['ci-price'])
        if not price_ci:
            price_ci = "N/A"
        if price_ci is "N/A":
            continue
        else:
            price_v2 = []
            for i in price_ci:
                price_v1 = re.sub("\D", "", str(i))
                price_v2.append((int(price_v1)))
                price = min(price_v2)        
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = str(soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['crumbs']))
        subdirectory_li = re.findall(r'title="\w+',subdirectory)
        subdirectory_li_text = []
        for o in subdirectory_li:
            subdirectory_li_text.append(re.sub(r'title="',"",o))
        cataloge_v1 = subdirectory_li_text[0]
        cataloge_v2 = subdirectory_li_text[1]
        cataloge_v3 = subdirectory_li_text[2]
        # --- Наименование товара
        name = soup.html.head.title.text
        #soup.get_text()

        # --- получение Изображений товара
        image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
        images = image[:3]
        images = [image.attrs['href'] for image in images]
        images_base = []
        for itemImg in images:
            images_base.append(base_url_rvi_cctv+itemImg)
        images_base = images_base[0:3]
        images_base = '|'.join(images_base)

        # --- Описание товара
        #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
        text_ = soup.find('div', attrs={'class':'osobennost'})
        text_body = text_.text[4:]

        #--- Таблица с характеристиками
        #soup.select('div .charact') #список объектов супа
        tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
        number_of_signs = len(soup.text) #расчет объема текста
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('rvi-cctv-1.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out)
#============================================================ Сетевое оборудование
linck = "https://rvi-cctv.ru/catalog/setevoe_oborudovanie/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_rvi_cctv + item)  
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
        data = requests.get(page)
        soup = BeautifulSoup(data.text, 'html.parser')
        # --- Вторая цена товара
        price_ci = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['ci-price'])
        if not price_ci:
            price_ci = "N/A"
        if price_ci is "N/A":
            continue
        else:
            price_v2 = []
            for i in price_ci:
                price_v1 = re.sub("\D", "", str(i))
                price_v2.append((int(price_v1)))
                price = min(price_v2)        
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = str(soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['crumbs']))
        subdirectory_li = re.findall(r'title="\w+',subdirectory)
        subdirectory_li_text = []
        for o in subdirectory_li:
            subdirectory_li_text.append(re.sub(r'title="',"",o))
        cataloge_v1 = subdirectory_li_text[0]
        cataloge_v2 = subdirectory_li_text[1]
        cataloge_v3 = subdirectory_li_text[2]
        # --- Наименование товара
        name = soup.html.head.title.text
        #soup.get_text()

        # --- получение Изображений товара
        image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
        images = image[:3]
        images = [image.attrs['href'] for image in images]
        images_base = []
        for itemImg in images:
            images_base.append(base_url_rvi_cctv+itemImg)
        images_base = images_base[0:3]
        images_base = '|'.join(images_base)

        # --- Описание товара
        #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
        text_ = soup.find('div', attrs={'class':'osobennost'})
        text_body = text_.text[4:]

        #--- Таблица с характеристиками
        #soup.select('div .charact') #список объектов супа
        tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
        number_of_signs = len(soup.text) #расчет объема текста
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('rvi-cctv-1.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out)
#================================================== Дополнительное оборудование и аксессуары 
linck = "https://rvi-cctv.ru/catalog/dopolnitelnoe_oborudovanie_i_aksessuary/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_rvi_cctv + item)  
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
        data = requests.get(page)
        soup = BeautifulSoup(data.text, 'html.parser')
        # --- Вторая цена товара
        price_ci = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['ci-price'])
        if not price_ci:
            price_ci = "N/A"
        if price_ci is "N/A":
            continue
        else:
            price_v2 = []
            for i in price_ci:
                price_v1 = re.sub("\D", "", str(i))
                price_v2.append((int(price_v1)))
                price = min(price_v2)        
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = str(soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['crumbs']))
        subdirectory_li = re.findall(r'title="\w+',subdirectory)
        subdirectory_li_text = []
        for o in subdirectory_li:
            subdirectory_li_text.append(re.sub(r'title="',"",o))
        cataloge_v1 = subdirectory_li_text[0]
        cataloge_v2 = subdirectory_li_text[1]
        cataloge_v3 = subdirectory_li_text[2]
        # --- Наименование товара
        name = soup.html.head.title.text
        #soup.get_text()

        # --- получение Изображений товара
        image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
        images = image[:3]
        images = [image.attrs['href'] for image in images]
        images_base = []
        for itemImg in images:
            images_base.append(base_url_rvi_cctv+itemImg)
        images_base = images_base[0:3]
        images_base = '|'.join(images_base)

        # --- Описание товара
        #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
        text_ = soup.find('div', attrs={'class':'osobennost'})
        text_body = text_.text[4:]

        #--- Таблица с характеристиками
        #soup.select('div .charact') #список объектов супа
        tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
        number_of_signs = len(soup.text) #расчет объема текста
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('rvi-cctv-1.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out)
#==================================================================== Домофонные системы
linck = "https://rvi-cctv.ru/catalog/domofonnye_sistemy_1/"
data = requests.get(linck, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(data.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['cb-name'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_rvi_cctv + item)  
#--- получили все url всех карточек товара в листе items    
data_out = []  
for page in items:
        data = requests.get(page)
        soup = BeautifulSoup(data.text, 'html.parser')
        # --- Вторая цена товара
        price_ci = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['ci-price'])
        if not price_ci:
            price_ci = "N/A"
        if price_ci is "N/A":
            continue
        else:
            price_v2 = []
            for i in price_ci:
                price_v1 = re.sub("\D", "", str(i))
                price_v2.append((int(price_v1)))
                price = min(price_v2)        
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = str(soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['crumbs']))
        subdirectory_li = re.findall(r'title="\w+',subdirectory)
        subdirectory_li_text = []
        for o in subdirectory_li:
            subdirectory_li_text.append(re.sub(r'title="',"",o))
        cataloge_v1 = subdirectory_li_text[0]
        cataloge_v2 = subdirectory_li_text[1]
        cataloge_v3 = subdirectory_li_text[2]
        # --- Наименование товара
        name = soup.html.head.title.text
        #soup.get_text()

        # --- получение Изображений товара
        image = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['fancybox'])
        images = image[:3]
        images = [image.attrs['href'] for image in images]
        images_base = []
        for itemImg in images:
            images_base.append(base_url_rvi_cctv+itemImg)
        images_base = images_base[0:3]
        images_base = '|'.join(images_base)

        # --- Описание товара
        #text_ = str(soup.find_all('font', {"face":"Raleway"})[0:10])
        text_ = soup.find('div', attrs={'class':'osobennost'})
        text_body = text_.text[4:]

        #--- Таблица с характеристиками
        #soup.select('div .charact') #список объектов супа
        tds = str(soup.find('table',attrs={'class':'table-char my_class'}))
        number_of_signs = len(soup.text) #расчет объема текста
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('comdiv.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out)


#==================================  www.dssl.ru
base_url_dssl = "https://www.dssl.ru"
#---- Аналоговые камеры AHD, TVI в стандартном корпусе
url_cat = "https://www.dssl.ru/products/analogovye-v-standartnom-korpuse/"
dataRequest = requests.get(url_cat, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(dataRequest.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['thumb'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_dssl + item)
#---получили ссылки подкаталога - каждой карточки товара   

#========================================== Карточка товара
data_out = []  
for page in items:
    data = requests.get(page)
    soup = BeautifulSoup(data.text, 'html.parser')
    # --- Условие если цена есть? Вторая цена товара
    price_div = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['price'])
    price_span = price_div.text
    price_span_n = re.sub("\D", "", str(price_span))
    if not price_span_n:
        price = "N/A"
    if price is "N/A":
        continue
    else:
        price = price_span_n   
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = soup.find_all('span',attrs={'itemprop':'name'})
        cataloge_v1 = subdirectory[0].text
        cataloge_v2 = subdirectory[1].text
        cataloge_v3 = subdirectory[2].text
        cataloge_v4 = subdirectory[3].text

        # --- Наименование товара
        name = soup.h1.text
        #soup.get_text()

        # --- получение Изображений товара
        images_r = soup.find_all('a',attrs={'class':'popup_link fancy'})
        images = images_r[:3]
        images = [images_r.attrs['href'] for images_r in images]
        images_base = []
        for i in images:
            images_base.append(base_url_dssl+i)
        images_base = '|'.join(images_base)

        # --- Описание товара
        text_ = soup.find('div', attrs={'class':'detail_text'})
        text_body = str(text_)
        #--- Таблица характеристик
        tds = str(soup.find('table',attrs={'id':'tech'}))
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('comdiv.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out) 

#---- Аналоговые купольные камеры AHD, HD-TVI, HD-CVI
url_cat = "https://www.dssl.ru/products/analogovye-kupolnyie/"
dataRequest = requests.get(url_cat, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(dataRequest.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['thumb'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_dssl + item)
#---получили ссылки подкаталога - каждой карточки товара   

#========================================== Карточка товара
data_out = []  
for page in items:
    data = requests.get(page)
    soup = BeautifulSoup(data.text, 'html.parser')
    # --- Условие если цена есть? Вторая цена товара
    price_div = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['price'])
    price_span = price_div.text
    price_span_n = re.sub("\D", "", str(price_span))
    if not price_span_n:
        price = "N/A"
    if price is "N/A":
        continue
    else:
        price = price_span_n   
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = soup.find_all('span',attrs={'itemprop':'name'})
        cataloge_v1 = subdirectory[0].text
        cataloge_v2 = subdirectory[1].text
        cataloge_v3 = subdirectory[2].text
        cataloge_v4 = subdirectory[3].text

        # --- Наименование товара
        name = soup.h1.text
        #soup.get_text()

        # --- получение Изображений товара
        images_r = soup.find_all('a',attrs={'class':'popup_link fancy'})
        images = images_r[:3]
        images = [images_r.attrs['href'] for images_r in images]
        images_base = []
        for i in images:
            images_base.append(base_url_dssl+i)
        images_base = '|'.join(images_base)

        # --- Описание товара
        text_ = soup.find('div', attrs={'class':'detail_text'})
        text_body = str(text_)
        #--- Таблица характеристик
        tds = str(soup.find('table',attrs={'id':'tech'}))
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('comdiv.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out) 
#---- Мини-камеры
url_cat = "https://www.dssl.ru/products/mini-kamery-ahd-tvi-analogovye/"
dataRequest = requests.get(url_cat, headers={'User-Agent': UserAgent().chrome})
soup = BeautifulSoup(dataRequest.text, 'html.parser')
link = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['thumb'])
links = link[:100]
links = [link.attrs['href'] for link in links]
items = []
for item in links:
    items.append(base_url_dssl + item)
#---получили ссылки подкаталога - каждой карточки товара   

#========================================== Карточка товара
data_out = []  
for page in items:
    data = requests.get(page)
    soup = BeautifulSoup(data.text, 'html.parser')
    # --- Условие если цена есть? Вторая цена товара
    price_div = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['price'])
    price_span = price_div.text
    price_span_n = re.sub("\D", "", str(price_span))
    if not price_span_n:
        price = "N/A"
    if price is "N/A":
        continue
    else:
        price = price_span_n   
        #--- получение IDs
        try:
            prodIds = str(soup.find(string=re.compile("productId")))
            prodIds = prodIds.split(';')
            prodId = int(re.sub("\D", "", prodIds[8]))
        except:
            prodId = "N/A"
        #--- getting the name of a subdirectory
        subdirectory = soup.find_all('span',attrs={'itemprop':'name'})
        cataloge_v1 = subdirectory[0].text
        cataloge_v2 = subdirectory[1].text
        cataloge_v3 = subdirectory[2].text
        cataloge_v4 = subdirectory[3].text

        # --- Наименование товара
        name = soup.h1.text
        #soup.get_text()

        # --- получение Изображений товара
        images_r = soup.find_all('a',attrs={'class':'popup_link fancy'})
        images = images_r[:3]
        images = [images_r.attrs['href'] for images_r in images]
        images_base = []
        for i in images:
            images_base.append(base_url_dssl+i)
        images_base = '|'.join(images_base)

        # --- Описание товара
        text_ = soup.find('div', attrs={'class':'detail_text'})
        text_body = str(text_)
        #--- Таблица характеристик
        tds = str(soup.find('table',attrs={'id':'tech'}))
        # save the data in tuple
        data_out.append((prodId,name,cataloge_v1,cataloge_v2,cataloge_v3,cataloge_v4,price,text_body,images_base,tds)) #no tuple
        # open a csv file with append, so old data will not be erased
with codecs.open('comdiv.csv', 'a', 'utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(data_out) 



























































    