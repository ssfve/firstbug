# -*- coding:utf-8 -*- 

import os
import requests
import random
#from faker import Factory
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sys import argv

from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import scrapy
#from pydispatch import dispatcher

from selenium import webdriver
import mysql.connector
#from mysql.connector import connection

schema_name = 'boardgames'
#table_name = 'bggdata'
table_name = 'rank_list'

start_num = int(argv[1])
end_num = int(argv[2])
env_var = argv[3]

langDep_dict = {
    'No necessary in-game text':0,
    'Some necessary text - easily memorized or small crib sheet':1,
    'Moderate in-game text - needs crib sheet or paste ups':2,
    'Extensive use of text - massive conversion needed to be playable':3,
    'Unplayable in another language':4
}
class ProductSpider(Spider):
    name = 'boardgameinfo'
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    #base_url = 'https://www.boardgamegeek.com/boardgame/'
    base_url = 'https://www.boardgamegeek.com/browse/boardgame/page/'
    start_urls = [base_url+'1']
    rankid = 1
    # above are class variables
    #enter_var = 0
    
    cookies = {}

    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': False,  
        'handle_httpstatus_list': [301, 302, 404]  
    }
    gameid = ''
    nameEN = ''
    gametype = ''

    def __init__(self):
        if env_var == 'windows':
            print "using windows client"
            self.driver = webdriver.PhantomJS(executable_path='D:/Drivers/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        else:
            print "using linux client"
            self.driver = webdriver.PhantomJS(executable_path='/home/test/spiderbug/getrank/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
            
        self.driver.set_page_load_timeout(25)
        #scrapy.Request(self.start_urls[0],callback=self.parse)
        #dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self,response):
        print "in parse"

        try:
            print response
            print response.url
            self.driver.get(response.url)
            self.sub_parse(response)
        except Exception,e:
            print e
            print 'time out after 25 seconds when loading page still processing'
            #self.driver.execute_script('window.stop()')
            
        try:
            #self.enter_var = 1
            for self.pageid in range(start_num,end_num):
                self.start_urls[0] = self.base_url + str(self.pageid)
                print self.start_urls[0]
                yield scrapy.Request(self.start_urls[0],callback=self.parse)
        except Exception,e:
            print e
            with open('error.log','w+') as f:
                f.write('error')
                #f.write(url)
            self.driver.save_screenshot('D:\screenshot.png')

    def sub_parse(self,response):
        print "in sub_parse"
        print response.url
        #print get_base_url(response)
        #res = self.driver.get(response.url)
        
        #con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
        #con = mysql.connector.connect(host='180.76.244.130',port=3306,user='root',password='b0@rdg@merule5')
        con = mysql.connector.connect(host='180.76.244.130',port=3306,user='mysql',password='MyNewPass4!')
        cur = con.cursor()
        rank_xpath = "//*[@id=\"row_\"]/td[1]"
        rank_element = self.driver.find_elements_by_xpath(rank_xpath)
        print len(rank_element)
        #//*[@id="row_43330232"]
        #//*[@id="row_43330232"]/td[1]
        
        #for i,index in enumerate(range(1,200,2)):
        for i,index in enumerate(range(1,101)):
            object_xpath = "//*[@id=\"results_objectname"+str(index)+"\"]/a"
            print object_xpath
            
            try:
                game_element = self.driver.find_elements_by_xpath(object_xpath)
                content = game_element[0].get_attribute("href").split("/")
                print content
                
                #print rank_element
                self.rankid = rank_element[i].text
                self.gameid = content[4]
                self.nameEN = content[5]
                
                #print self.gameid
                #print self.nameEN
                #print self.rankid
                
            except Exception,e:
                print e
                    
            column_str = 'gameid,nameEN,rankid'
            value_str = str(self.gameid)+',\''+str(self.nameEN)+'\','+str(self.rankid)
                
                
            sql = 'REPLACE INTO '+schema_name+'.'+table_name+'('+column_str+')values('+value_str+')'
            print sql
            
            try:
                cur.execute(sql)
                #print 'SQL EXECUTION SUCCESS!'
            except Exception,e:
                print 'error when executing sql'
                print e
            con.commit()
            
        cur.close()
        con.close()

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ProductSpider)
    process.start()