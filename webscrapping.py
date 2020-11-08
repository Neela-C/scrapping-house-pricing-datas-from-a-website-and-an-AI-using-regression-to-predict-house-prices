from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
import time


yourMYSQLpassword='iop' ### change here

def sqlstuff(idee, metraj,mantaghe,salesakht,price):
    DB = mysql.connector.connect(host = 'localhost', user = 'root', password = yourMYSQLpassword)
    cursor = DB.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS housesdatabase;')
    cursor.execute('USE housesdatabase;')
    cursor.execute('CREATE TABLE IF NOT EXISTS houses (idee INT, metraj INT, mantaghe INT, salesakht INT, priceInMillion INT);')
    cursor.execute("SELECT * FROM houses WHERE idee = {}".format(idee))
    results = cursor.fetchall()

    if not results:
        cursor.execute('INSERT INTO houses VALUES ({}, {}, {}, {},{});'.format(idee, metraj,mantaghe,salesakht,price))

        DB.commit()

    cursor.close()
    DB.close()


def webstuff():

    datalist =[[]]
    i = 1
    count = 0
    while i<300 :
        j = str(i)
        r = requests.get('https://dodota.com/realestate/search/?deal_type=1&v1=1&citycode=1&region_code=thr&page_num={}'.format(j))
        soup = BeautifulSoup(r.text, 'html.parser')
        # f = open('site.html', 'w')
        # f.write(r.text)
        # print(r.text)
        boxes = soup.find_all('div',attrs = {'class':"main-l panel panel-info"})

        for box in boxes:
            # print(count, len(datalist))
            ideebox = box.find('span',attrs = {'class':"hidden-xs hidden-sm"})
            ideetext = ideebox.text
            if ideetext == "":
                pass
            else:
                regex = r'ملک (\d+)'
                idee = int(re.search(regex,ideetext).group(1))
                datalist[count].append(idee)

                metrajbox = box.find('span',attrs = {'class':"rd"})
                metrajtext = metrajbox.text
                regex = r'(\d+) متر مربع'
                try:
                    metraj = int(re.search(regex,metrajtext).group(1))
                except AttributeError:
                    datalist.pop(count)
                    datalist.append([])
                    continue
                datalist[count].append(metraj)

                mantaghebox = box.find('div', attrs={'class':'panel-heading'}).div
                mantaghetext = mantaghebox.text
                regex = r'منطقه (\d+)'
                try:
                    mantaghe = int(re.search(regex, mantaghetext).group(1))
                except AttributeError:
                    datalist.pop(count)
                    datalist.append([])
                    continue
                datalist[count].append(mantaghe)
            
                salesakhtbox = box.find('div',attrs = {'class':"col-sm-12 col-md-6"})
                salesakhttext = salesakhtbox.text
                regex = r'سال ساخت: (\d+)'
                try:
                    salesakht = int(re.search(regex,salesakhttext).group(1))
                except AttributeError:
                    datalist.pop(count)
                    datalist.append([])
                    continue
                datalist[count].append(salesakht)

                pricebox = box.find('div',attrs = {'class':"itm-desc itm-price"})
                pricetext =pricebox.text
                regex1 = r' (\d+)\/(\d+)  میلیارد تومان'
                regex2 = r' (\d+)\/(\d+)  میلیون تومان'
                regex3 = r' (\d+)  میلیارد تومان'
                regex4 = r' (\d+)  میلیون تومان'
                if re.match(regex1, pricetext):
                    price = float(re.search(regex1,pricetext).group(1)+'.'+re.search(regex1,pricetext).group(2))*1000
                if re.match(regex2,pricetext):
                    price = float(re.search(regex2,pricetext).group(1)+'.'+re.search(regex2,pricetext).group(2))
                if re.match(regex3,pricetext):
                    price = float(re.search(regex3,pricetext).group(1))*1000
                if re.match(regex4,pricetext):
                    price = float(re.search(regex4,pricetext).group(1))
                datalist[count].append(price)

                datalist.append([])
                count+=1
        i+=1
        time.sleep(0.25)
    for data in datalist:
        if len(data)==0:
            datalist.remove(data)
    for data in datalist:
        sqlstuff(data[0],data[1],data[2],data[3],data[4])
        
        
    
webstuff()
