# -*- coding:utf-8 -*- 

import os
import requests
import random
from faker import Factory
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

start_num = int(argv[1])
end_num = start_num + int(argv[2])
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
    base_url = 'https://www.boardgamegeek.com/boardgame/' 
    start_urls = [base_url+str(1)]

    cookies = {}

    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': True,  
        'handle_httpstatus_list': [301, 302, 404]  
    }
    gameid = ''
    gamename = ''
    gametype = ''

    def __init__(self):
        self.driver = webdriver.PhantomJS(executable_path='D:/Drivers/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        self.driver.set_page_load_timeout(15)
        #scrapy.Request(self.start_urls[0],callback=self.parse)
        #dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self,response):
        print "in parse"
        self.gamename = response.url.split('/')[-1]
        self.gameid = response.url.split('/')[-2]
        self.gametype = response.url.split('/')[-3]
        if self.gameid == 'boardgame':
            self.gameid = response.url.split('/')[-1]
            self.gamename = response.url.split('/')[-2]

        try:
            if self.gametype == 'rpgitem':
                pass
            else:
                print response.url
                self.driver.get(response.url)
                self.sub_parse(response)
        except Exception,e:
            print 'time out after 15 seconds when loading page still processing'
            #self.driver.execute_script('window.stop()')

        try:
            for self.gameid in range(start_num,end_num):
                self.start_urls[0] = self.base_url + str(self.gameid)
                #print self.start_urls[0]
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

        #year_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/div/div[2]/h1/span"
        year_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/div/div[2]/h1/span"
        try:
            year = self.driver.find_element_by_xpath(year_xpath).text
            year = year.strip('(').strip(')')
            if year.isdigit():
                year = year
            else:
                year = ''
        except Exception,e:
            year = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' year ' + 'NOT FOUND'
                f.write(error_msg)
        minAge_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]"
        #minAge_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[3]/div[1]/span"
        #minAge = self.driver.find_element_by_xpath(minAge_xpath).text
        try:
            minAge = self.driver.find_element_by_xpath(minAge_xpath).text
            minAge = minAge.strip('Age: ').strip('+')
            if minAge.isdigit():
                minAge = minAge
            else:
                minAge = ''
        except Exception,e:
            minAge = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' minAge ' + 'NOT FOUND'
                f.write(error_msg)
        #print minAge.text
        #print minAge.unicode
        #print '=' * 20
        #minage
        rateScore_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/div/div[1]/div/div/a/span[1]"
        try:
            rateScore = self.driver.find_element_by_xpath(rateScore_xpath).text
        except Exception,e:
            rateScore = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' rateScore ' + 'NOT FOUND'
                f.write(error_msg)
        #rateScore'
        rateNum_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/div/div[2]/ul/li/a[1]"
        try:
            rateNum = self.driver.find_element_by_xpath(rateNum_xpath).text
            rateNum = rateNum.strip('Ratings').strip(' ')
            if (rateNum[-1]=='k' or rateNum[-1]=='K'):
                rateNum = int(float(rateNum[:-1])*1000)
            print rateNum
        except Exception,e:
            rateNum = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' rateNum ' + 'NOT FOUND'
                f.write(error_msg)
        #rateNum
        #rank_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/flags-module/div/div[2]/div/ul[1]/li/span[2]/a"
        #rank_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/flags-module/div/div/div/ul[1]/li/span[2]/a"
        #rank_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[1]/flags-module/div/div[2]/div/ul[1]/li/span[2]/a"
        rank_xpath = "//span[@class=\"rank-number\"]/a"
        try:
            rank = self.driver.find_element_by_xpath(rank_xpath).text
            rank = rank.replace(',','')
            print rank
        except Exception,e:
            rank = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' rank ' + 'NOT FOUND'
                f.write(error_msg)

        weight_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[4]/div[1]/span[2]/span"
        try:
            weight = self.driver.find_element_by_xpath(weight_xpath).text
        except Exception,e:
            weight = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' weight ' + 'NOT FOUND'
                f.write(error_msg)
        #weight
        mintime_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[2]/div[1]/span/span/span"
        maxtime_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[2]/div[1]/span/span/span[2]"
        try:
            mintime = self.driver.find_element_by_xpath(mintime_xpath).text
        except Exception,e:
            mintime = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' mintime ' + 'NOT FOUND'
                f.write(error_msg)
        #mintime.text
        try:
            maxtime = self.driver.find_element_by_xpath(maxtime_xpath).text
            maxtime = maxtime.strip(u'\u2013').strip(' ')
        except Exception,e:
            maxtime = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' maxtime ' + 'NOT FOUND'
                f.write(error_msg)
        #mintime.text
        
        minplayer_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[1]"
        maxplayer_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[1]/span/span[2]"
        bestplayer_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[2]/gameplay-module/div/div/ul/li[1]/div[2]/span/button/span[3]"
        try:
            minplayer = self.driver.find_element_by_xpath(minplayer_xpath).text
        except Exception,e:
            minplayer = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' minplayer ' + 'NOT FOUND'
                f.write(error_msg)
        try:
            maxplayer = self.driver.find_element_by_xpath(maxplayer_xpath).text
            maxplayer = maxplayer.strip(u'\u2013').strip(' ')
        except Exception,e:
            maxplayer = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' maxplayer ' + 'NOT FOUND'
                f.write(error_msg)
        try:
            #bestplayer = self.driver.find_element_by_xpath(bestplayer_xpath).text.strip(u'\u2013').strip(u'\u2014').strip('Best: ')
            bestplayer = self.driver.find_element_by_xpath(bestplayer_xpath).text
            if bestplayer[-1].isdigit():
            	bestplayer = bestplayer[-1]
            else:
            	bestplayer = ''  
        except Exception,e:
            bestplayer = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' bestplayer ' + 'NOT FOUND'
                f.write(error_msg)
        #min-max players
        langDep_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div[1]/overview-module/description-module/div/div[2]/div/div[3]/div[2]/div[1]/div/ul/li/div[2]/span/span"
        try:
            #bestplayer = self.driver.find_element_by_xpath(bestplayer_xpath).text.strip(u'\u2013').strip(u'\u2014').strip('Best: ')
            langDep = self.driver.find_element_by_xpath(langDep_xpath).text
            print langDep
            if langDep_dict.has_key(langDep): 
                langDep = langDep_dict[langDep]
                print langDep
            else:
                langDep = ''  
        except Exception,e:
            langDep = ''
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' langDep ' + 'NOT FOUND'
                f.write(error_msg)
        #langDeplvl
        #designers_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/ng-include/div/div/div[2]/div[3]/div/ul/li[1]/popup-list//span/a"
        designers_xpath = "//popup-list[@items=\"geekitemctrl.geekitem.data.item.links.boardgamedesigner\"]//span/a"
        try:
            designers = self.driver.find_elements_by_xpath(designers_xpath)
        except Exception,e:
            designers = []
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' designers ' + 'NOT FOUND'
                f.write(error_msg)

        artists_xpath = "//popup-list[@items=\"geekitemctrl.geekitem.data.item.links.boardgameartist\"]//span/a"
        try:
            artists = self.driver.find_elements_by_xpath(artists_xpath)
        except Exception,e:
            artists = []
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' artists ' + 'NOT FOUND'
                f.write(error_msg)

        publishers_xpath = "//popup-list[@items=\"geekitemctrl.geekitem.data.item.links.boardgamepublisher\"]//span/a"
        try:
            publishers = self.driver.find_elements_by_xpath(publishers_xpath)
        except Exception,e:
            publishers = []
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' publishers ' + 'NOT FOUND'
                f.write(error_msg)

        categorys_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div[1]/overview-module/description-module/div/div[2]/div/div[1]/classifications-module/div/div[2]/ul/li[2]/div[2]/popup-list//span/a"
        try:
            categorys = self.driver.find_elements_by_xpath(categorys_xpath)
        except Exception,e:
            categorys = []
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' categorys ' + 'NOT FOUND'
                f.write(error_msg)

        mechanism_xpath = "//*[@id=\"mainbody\"]/div/div[1]/div[1]/div[2]/ng-include/div/div/ui-view/ui-view/div[1]/overview-module/description-module/div/div[2]/div/div[1]/classifications-module/div/div[2]/ul/li[3]/div[2]/popup-list//span/a"
        try:
            mechanisms = self.driver.find_elements_by_xpath(mechanism_xpath)
        except Exception,e:
            mechanisms = []
            with open('error.log','w+') as f:
                error_msg = str(self.gameid) + ' mechanisms ' + 'NOT FOUND'
                f.write(error_msg)
        
        

        column_str = '('
        value_str = '('

        column_str += 'gameid,'
        value_str += str(self.gameid)+','

        print self.gamename
        if self.gamename == '':
            column_str += ''
        else:
            column_str += 'nameEN,'
            value_str += '"'+str(self.gamename)+'",'
        
        print year
        if year == '':
            column_str += ''
        else:
            column_str += 'year,'
            value_str += str(year)+','

        print minAge
        if minAge == '':
            column_str += ''
        else:
            column_str += 'minAge,'
            value_str += str(minAge)+','

        print rateScore
        if rateScore == '':
            column_str += ''
        else:
            column_str += 'rateScore,'
            value_str += str(rateScore)+','

        print rateNum
        if rateNum == '':
            column_str += ''
        else:
            column_str += 'rateNum,'
            value_str += str(rateNum)+','

        print rank
        if rank == '':
            column_str += ''
        else:
            column_str += 'rank,'
            value_str += str(rank)+','

        print weight
        if weight == '':
            column_str += ''
        else:
            column_str += 'weight,'
            value_str += str(weight)+','

        print mintime
        if mintime == '':
            column_str += ''
        else:
            column_str += 'mintime,'
            value_str += str(mintime)+','
        print maxtime
        if maxtime == '':
            column_str += ''
        else:
            column_str += 'maxtime,'
            value_str += str(maxtime)+','

        print minplayer
        if minplayer == '':
            column_str += ''
        else:
            column_str += 'minplayer,'
            value_str += str(minplayer)+','

        print maxplayer
        if maxplayer == '':
            column_str += ''
        else:
            column_str += 'maxplayer,'
            value_str += str(maxplayer)+','

        print bestplayer
        if bestplayer == '':
            column_str += ''
        else:
            column_str += 'bestplayer,'
            value_str += str(bestplayer)+','

        print langDep
        if langDep == '':
            column_str += ''
        else:
            column_str += 'langDep,'
            value_str += str(langDep)+','
        
        mechanism_str = ''
        designer_str = ''
        artist_str = ''
        category_str = ''
        publisher_str = ''

        for mechanism in mechanisms:
            mechanism_str += mechanism.text+'|'
        for designer in designers:
            designer_str += designer.text.replace('"','')+'|'
        for artist in artists:
            artist_str += artist.text+'|'
        for category in categorys:
            category_str += category.text+'|'
        for publisher in publishers:
            publisher_str += publisher.text.encode("utf-8")+'|'

        if mechanism_str == '':
            column_str += ''
        else:
            column_str += 'mechanisms,'
            value_str += '"'+str(mechanism_str)+'",'

        if designer_str == '':
            column_str += ''
        else:
            column_str += 'designers,'
            value_str += '"'+str(designer_str)+'",'

        if artist_str == '':
            column_str += ''
        else:
            column_str += 'artists,'
            value_str += '"'+str(artist_str)+'",'

        if category_str == '':
            column_str += ''
        else:
            column_str += 'categorys,'
            value_str += '"'+str(category_str)+'",'

        if publisher_str == '':
            column_str += ''
        else:
            column_str += 'publishers,'
            value_str += '"'+str(publisher_str)+'",'


        if column_str[-1] == ',':
            column_str = column_str[:-1]+')'
        else:
            column_str += ')'

        if value_str[-1] == ',':
            value_str = value_str[:-1]+')'
        else:
            value_str += ')'

        con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')

        schema_name = 'boardgames'
        table_name = 'bggdata'
        #column_str = "(self.gameid,year,minAge,rateScore,rateNum,rank,weight,minplayer,time,designers,categorys,mechanisms,publishers,maxplayer,bestplayer,self.name)" 
        #value_str = str(self.gameid)+','+str(year)+','+str(minAge)+','+str(rateScore)+','+str(rateNum)+','+str(rank)+','+str(weight)+','+str(minplayer)+','+str(time)+','+  \
        #'"'+str(designer_str)+'","'+str(category_str)+'","'+str(mechanism_str)+'","'+str(publisher_str)+'",'+str(maxplayer)+','+str(bestplayer)+',"'+str(self.name)+'"'

        sql = 'REPLACE INTO '+schema_name+'.'+table_name+column_str+'values'+value_str
        print sql
        cur = con.cursor()
        try:
            cur.execute(sql)
            print 'SQL EXECUTION SUCCESS!'
        except Exception,e:
            print 'error when executing sql'
            print e
        cur.close()
        con.commit()
        con.close()
        #self.driver.quit()
        

        #self.driver.quit()
        #WebDriverWait(res,60).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@id='content']/table"))) 
        #text = res.find_elements_by_xpath("//div[@id='content']/table")
        #print text

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ProductSpider)
    process.start()