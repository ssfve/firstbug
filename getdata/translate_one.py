# -*- coding:utf-8 -*-

import os
import io
import requests
import random
#from faker import Factory
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sys import argv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import urllib2
import mysql.connector
#from mysql.connector import connection

from gamelist import create_gamelist
import platform
from api_one import writedb
from categorylist import *


nameCN_dict = create_gamelist()

designer_dict = dict()
designer_dict['Reiner Knizia'] = u'倪睿南'
designer_dict['Chu-Lan Kao'] = u'高竹岚'
designer_dict['Uwe Rosenberg'] = u'乌老师'
designer_dict['Liu Xiao'] = u'刘啸'

type_dict = create_typelist()
category_dict = create_categorylist()
mechanic_dict = create_mechaniclist()

#print nameCN_dict
schema_name = 'boardgames'
table_name = 'bggdata'
table_name_cn = 'bggdatacn'

#start_num = int(argv[1])
#end_num = start_num + int(argv[2])
"""
try:
    gameid = int(argv[1])
    environment = argv[2]
except:
    print 'usage: python translate_db_one.py gameid local/remote/linux'
    sys.exit(0)
#type_dict = dict()
"""
#mechanic_dict = dict()
import categorylist

pipeline = '|'

def bgg_xml_translater(games_dict):
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    #base_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{0}?stats=1'

    boardgamemechanic = ''
    boardgamecategory = ''
    boardgamepublisher = ''
    boardgamedesigner = ''
    boardgamefamily = ''
    boardgameexpansion = ''
    boardgamesubdomain = ''
    boardgameartist = ''
    suggested_numplayers = ''
    suggested_playerage = ''
    language_dependence = ''
    #game_type = ''
    #error_flag = False

    bayesaverage_subtype = ''
    rank_subtype = ''
    bayesaverage_type = ''
    rank_type = ''
    yearpublished = ''
    age = ''
    minplaytime = ''

    #global gameid

    #game_list = list()
    #game_list.append(gameid)

    for gameid in games_dict:
        try:
            sql = 'SELECT * FROM '+schema_name+'.'+table_name+' where gameid = '+str(gameid)
            print sql
	    userPlatform=platform.system()
	    if(userPlatform=='Linux'):
		print('System is Linux')
		con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
                cur = con.cursor()
            elif(userPlatform=='Windows'):
	    	print('System is Windows')
		con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
            	cur = con.cursor()
            cur.execute(sql)
            records = cur.fetchall()
            data = list(records[0])
            #print data
            yearpublished = str(data[1])
            age = str(data[2])
            suggested_playerage = str(data[3])
            usersrated = str(data[4])
            rank_subtype = str(data[5])
            rank_type = str(data[6])
            numweights = str(data[7])
            minplayers = str(data[8])
            maxplayers = str(data[9])
            minplaytime = str(data[10])
            maxplaytime = str(data[11])
            language_dependence = str(data[12])

            average = data[13]
            bayesaverage_subtype = data[14]
            bayesaverage_type = data[15]
            averageweight = data[16]

            suggested_numplayers = str(data[17])
            #nameCN = str(data[18])
            if games_dict.has_key(gameid):
                nameCN = str(games_dict[gameid][0])
                #print nameCN
            else:
                nameCN = str(data[18])
            expansionsCN = str(data[19])
            typeCN = str(data[20])
            categorysCN = str(data[21])
            mechanicsCN = str(data[22])
            familysCN = str(data[23])
            subdomainCN = str(data[24])
            designersCN = str(data[25])
            artistsCN = str(data[26])
            publishersCN = str(data[27])

        except Exception,e:
            print 'error while executing sql 1'
            print sql
            print e
            continue

        column_str = '('
        value_str = '('

        #print gameid
        column_str += 'gameid,'
        value_str += str(gameid)+','

        #print nameCN
        if nameCN == '' or nameCN == 'None':
            column_str += ''
        else:
            column_str += 'nameCN,'
            value_str += '"'+str(nameCN)+'",'

        #print yearpublished
        if yearpublished == '' or yearpublished == 'None':
            column_str += ''
        else:
            column_str += 'yearpublished,'
            value_str += str(yearpublished)+','
        #print column_str
        #print age
        if age == '' or age == 'None':
            column_str += ''
        else:
            column_str += 'age,'
            value_str += str(age)+','

        #print minplaytime
        if minplaytime == '' or minplaytime == 'None':
            column_str += ''
        else:
            column_str += 'minplaytime,'
            value_str += str(minplaytime)+','

        #print maxplaytime
        if maxplaytime == '' or maxplaytime == 'None':
            column_str += ''
        else:
            column_str += 'maxplaytime,'
            value_str += str(maxplaytime)+','

        #print minplayers
        if minplayers == '' or minplayers == 'None':
            column_str += ''
        else:
            column_str += 'minplayers,'
            value_str += str(minplayers)+','

        #print maxplayers
        if maxplayers == '' or maxplayers == 'None':
            column_str += ''
        else:
            column_str += 'maxplayers,'
            value_str += str(maxplayers)+','

        if suggested_playerage == '' or suggested_playerage == 'None':
            column_str += ''
        else:
            column_str += 'suggested_playerage,'
            value_str += str(suggested_playerage)+','

        #print averageweight
        if average == '' or average =='None' or average == None:
            column_str += ''
        else:
            column_str += 'average,'
            value_str += str(average)+','

        #print averageweight
        if averageweight == '' or averageweight =='None' or averageweight == None:
            column_str += ''
        else:
            column_str += 'averageweight,'
            value_str += str(averageweight)+','

        #print averageweight
        if numweights == '' or numweights =='None'  or numweights == None:
            column_str += ''
        else:
            column_str += 'numweights,'
            value_str += str(numweights)+','

        #print usersrated
        if usersrated == '' or usersrated =='None'  or usersrated == None:
            column_str += ''
        else:
            column_str += 'usersrated,'
            value_str += str(usersrated)+','

        #print rank_subtype
        if rank_subtype == '' or rank_subtype == 'None' or rank_subtype == None:
            #print 'hello'
            column_str += ''
        else:
            column_str += 'rank_subtype,'
            value_str += str(rank_subtype)+','

        #print rank_subtype
        if rank_type == '' or rank_type == 'None' or rank_type == None:
            column_str += ''
        else:
            column_str += 'rank_type,'
            value_str += str(rank_type)+','

        #print rank_subtype
        if bayesaverage_subtype == '' or bayesaverage_subtype == 'None'  or bayesaverage_subtype == None:
            column_str += ''
        else:
            column_str += 'bayesaverage_subtype,'
            value_str += str(bayesaverage_subtype)+','

        #print bayesaverage_type
        #print type(bayesaverage_type)
        if bayesaverage_type == '' or bayesaverage_type == None or bayesaverage_type == 'None':
            column_str += ''
        else:
            column_str += 'bayesaverage_type,'
            value_str += str(bayesaverage_type)+','

        #print language_dependence
        #print type(language_dependence)
        if language_dependence == '' or language_dependence == None or language_dependence == 'None':
            column_str += ''
        else:
            column_str += 'language_dependence,'
            value_str += str(language_dependence)+','

        #print suggested_numplayers
        if suggested_numplayers == '':
            column_str += ''
        else:
            column_str += 'suggested_numplayers,'
            value_str += '"'+str(suggested_numplayers)+'",'


        mechanism_str = ''
        designer_str = ''
        artist_str = ''
        category_str = ''
        publisher_str = ''
        type_str = ''

        mechanics = mechanicsCN.rstrip('|').split('|')
        designers = designersCN.rstrip('|').split('|')
        categorys = categorysCN.rstrip('|').split(pipeline)
        #print mechanics
        #print mechanic_dict['Area Control / Area Influence']
        type_str += type_dict[typeCN] + pipeline
        for mechanic in mechanics:
            mechanism_str += mechanic_dict[mechanic] + pipeline
        for designer in designers:
            try:
                designer_str += designer_dict[designer] + pipeline
            except:
                designer_str += designer + pipeline
        for category in categorys:
            category = category.replace(' ','')
            #print "1"+category+"1"
            #print category_dict[category]
            category_str += category_dict[category] + pipeline
        """
        for designer in designers:
            designer_str += designer.text.replace('"','')+'|'
        for artist in artists:
            artist_str += artist.text+'|'
        for publisher in publishers:
            publisher_str += publisher.text.encode("utf-8")+'|'
        """
        if mechanism_str == '':
            column_str += ''
        else:
            column_str += 'mechanicsCN,'
            value_str += '"'+str(mechanism_str)+'",'

        if type_str == '':
            column_str += ''
        else:
            column_str += 'typeCN,'
            value_str += '"'+str(type_str)+'",'

        if designersCN == '':
            column_str += ''
        else:
            column_str += 'designersCN,'
            value_str += '"'+str(designer_str)+'",'

        if artistsCN == '':
            column_str += ''
        else:
            column_str += 'artistsCN,'
            value_str += '"'+str(artistsCN)+'",'

        if category_str == '':
            column_str += ''
        else:
            column_str += 'categorysCN,'
            value_str += '"'+str(category_str)+'",'

        if familysCN == '':
            column_str += ''
        else:
            column_str += 'familysCN,'
            value_str += '"'+str(familysCN)+'",'

        if publishersCN == '':
            column_str += ''
        else:
            column_str += 'publishersCN,'
            value_str += '"'+str(publishersCN)+'",'

        if expansionsCN == '':
            column_str += ''
        else:
            column_str += 'expansionsCN,'
            value_str += '"'+str(expansionsCN)+'",'

        if subdomainCN == '':
            column_str += ''
        else:
            column_str += 'subdomainCN,'
            value_str += '"'+str(subdomainCN)+'",'


        if column_str[-1] == ',':
            column_str = column_str[:-1]+')'
        else:
            column_str += ')'

        if value_str[-1] == ',':
            value_str = value_str[:-1]+')'
        else:
            value_str += ')'




        #column_str = "(self.gameid,year,minAge,rateScore,rateNum,rank,weight,minplayer,time,designers,categorys,mechanisms,publishers,maxplayer,bestplayer,self.name)"
        #value_str = str(self.gameid)+','+str(year)+','+str(minAge)+','+str(rateScore)+','+str(rateNum)+','+str(rank)+','+str(weight)+','+str(minplayer)+','+str(time)+','+  \
        #'"'+str(designer_str)+'","'+str(category_str)+'","'+str(mechanism_str)+'","'+str(publisher_str)+'",'+str(maxplayer)+','+str(bestplayer)+',"'+str(self.name)+'"'

        sql = 'REPLACE INTO '+schema_name+'.'+table_name_cn+column_str+'values'+value_str
        #print sql

        
"""
if __name__ == '__main__':
    bgg_xml_translater()
"""
