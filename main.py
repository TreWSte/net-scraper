#!/usr/bin/python
import os
import urllib
import requests
import boto3
from bs4 import BeautifulSoup
import pandas as p
from datetime import datetime

TIME_FORMAT = "%Y%m%d%H%M%S"

def getData(url):
    r = requests.get(url)
    pageSoup = BeautifulSoup(r.content, "html.parser")
    table = pageSoup.find('table')
    table_rows = table.find_all('tr')
    dataColumns = []
    data = {}
    dataCols = table_rows[0].find_all('th')
    for col in dataCols:
        columnName = col.get_text()
        dataColumns.append(columnName)
        data[columnName] = []
    for i, row in enumerate(table_rows):
        if i != 0:
            dataPoints = row.find_all('td')
            for j, d in enumerate(dataPoints):
                data[dataColumns[j]].append(d.get_text())
    df = p.DataFrame(data=data)
    #print(datetime.now().strftime(TIME_FORMAT))
    #df.to_csv(datetime.now().strftime(TIME_FORMAT) + ".csv")
    # print(data)
    return df
    data = {}
    dataColumns = []
    print(table_rows)
    for i, row in enumerate(table_rows):
        cols = row.find_all('th')
        for j, c in enumerate(cols):
            if i == 0:
                dataColumns.append(c)
                data[dataColumns[j]] = []
            else:
                print(c)
                # data[dataColumns[j]].append(c)
    print(data)
    return

def nameOfDocument(url):
    r = requests.get(url)
    pageSoup = BeautifulSoup(r.content, "html.parser")
    r = requests.get(url)
    pageSoup = BeautifulSoup(r.content, "html.parser")
    figure = pageSoup.find_all('figure')[1]
    return figure.get_text().strip() + " - " + datetime.now().strftime(TIME_FORMAT)
    #rankings-last-updated

def savePage(df, name):
    s3 = boto3.resource('s3')
    object = s3.Object('my_bucket_name', 'pages' + name + '.csv')
    object.put(Body=df.to_csv(datetime.now().strftime(TIME_FORMAT) + ".csv"))

def run():
    print("Hello")
    url = "https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings"

    r = requests.get(url)
    with open("net.html",'wb') as f: 
        f.write(r.content)
    with open("net.txt",'wb') as f: 
        f.write(r.content)

    df = getData(url)
    name = nameOfDocument(url)
    savePage(df, name)
    print("DONE")
    
#page = urllib.request.urlopen(url)
#page = open(url)
#soup = BeautifulSoup(page)
#print(soup)

if __name__ == "__main__":
    run()