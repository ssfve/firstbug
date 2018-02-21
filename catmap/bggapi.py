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
#from categorylist import *


name_dict = create_gamelist()

schema_name = 'boardgames'
table_name = 'bggdata'

"""
try:
    environment = argv[1]
Exception:
    print 'usage: python bggapi.py local|remote'
"""
try:
    gameid = argv[1]
    if gameid[0:2] != '99':
        print 'gameid should start with 99, example 991234'
        sys.exit(0)
except:
    print 'usage: python bggapi.py gameid'
    sys.exit(0)
#end_num = start_num + int(argv[2])

pipeline = '|'
comma = ','
left_par = '('
right_par = ')'
quote = '"'
none_str = 'None'
null_str = ''
var_dict = dict()

game_list = list()
game_list.append(gameid)

def sql_gen(string):
    #print yearpublished
    global column_str, value_str, var_dict
    #print var_dict[string]
    if var_dict[string] in (null_str, none_str, None):
        column_str += null_str
    else:
        #print 'in'
        column_str += string + comma
        value_str += str(var_dict[string]) + comma

def sql_gen_str(string):
    #print yearpublished
    global column_str, value_str, var_dict
    #print var_dict[string]
    if var_dict[string] in (null_str, none_str, None):
        column_str += null_str
    else:
        #print 'in'
        column_str += string + comma
        value_str += quote + str(var_dict[string]) + quote + comma


def bgg_xml_reader():
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    base_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{0}?stats=1'
    """
    if environment == 'local':
        con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    else if environment == 'remote':
        con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
    cur = con.cursor()
    """
    global column_str, value_str, var_dict

    #for gameid in range(start_num,end_num):
    for gameid in game_list:
        mechanics = ''
        categorys = ''
        publishers = ''
        designers = ''
        familys = ''
        expansions = ''
        subdomains = ''
        artists = ''
        suggested_numplayers = ''
        suggested_playerage = ''
        language_dependence = ''
        game_type = ''
        error_flag = False

        bayesaverage_subtype = ''
        rank_subtype = ''
        bayesaverage_type = ''
        rank_type = ''

        #for gameid in game_list:
        column_str = '('
        value_str = '('

        #print gameid
        column_str += 'gameid,'

        print 'please input each column press enter is no value at that column'
        #gameid = input("game id = ")
        print ('gameid = ' + gameid)
        value_str += str(gameid)+','

        #print name
        name = raw_input("name = ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        if name == '' or name == 'None':
            column_str += ''
        else:
            column_str += 'name,'
            value_str += '"'+str(name)+'",'

        #print yearpublished
        yearpublished = input("yearpublished = ")
        if yearpublished == '' or yearpublished == 'None':
            column_str += ''
        else:
            column_str += 'yearpublished,'
            value_str += str(yearpublished)+','
        #print column_str
        age = input("age = ")
        if age == '' or age == 'None':
            column_str += ''
        else:
            column_str += 'age,'
            value_str += str(age)+','

        minplaytime = input("minplaytime = ")
        if minplaytime == '' or minplaytime == 'None':
            column_str += ''
        else:
            column_str += 'minplaytime,'
            value_str += str(minplaytime)+','

        maxplaytime = input("maxplaytime = ")
        if maxplaytime == '' or maxplaytime == 'None':
            column_str += ''
        else:
            column_str += 'maxplaytime,'
            value_str += str(maxplaytime)+','

        minplayers = input("minplayers = ")
        if minplayers == '' or minplayers == 'None':
            column_str += ''
        else:
            column_str += 'minplayers,'
            value_str += str(minplayers)+','

        maxplayers = input("maxplayers = ")
        if maxplayers == '' or maxplayers == 'None':
            column_str += ''
        else:
            column_str += 'maxplayers,'
            value_str += str(maxplayers)+','

        suggested_playerage = input("suggested_playerage = ")
        if suggested_playerage == '' or suggested_playerage == 'None':
            column_str += ''
        else:
            column_str += 'suggested_playerage,'
            value_str += str(suggested_playerage)+','

        average = input("average = ")
        if average == '' or average =='None' or average == None:
            column_str += ''
        else:
            column_str += 'average,'
            value_str += str(average)+','

        averageweight = input("averageweight = ")
        if averageweight == '' or averageweight =='None' or averageweight == None:
            column_str += ''
        else:
            column_str += 'averageweight,'
            value_str += str(averageweight)+','

        numweights = input("numweights = ")
        if numweights == '' or numweights =='None'  or numweights == None:
            column_str += ''
        else:
            column_str += 'numweights,'
            value_str += str(numweights)+','

        usersrated = input("usersrated = ")
        if usersrated == '' or usersrated =='None'  or usersrated == None:
            column_str += ''
        else:
            column_str += 'usersrated,'
            value_str += str(usersrated)+','

        rank_subtype = input("rank_subtype = ")
        if rank_subtype == '' or rank_subtype == 'None' or rank_subtype == None:
            #print 'hello'
            column_str += ''
        else:
            column_str += 'rank_subtype,'
            value_str += str(rank_subtype)+','

        rank_type = input("rank_type = ")
        if rank_type == '' or rank_type == 'None' or rank_type == None:
            column_str += ''
        else:
            column_str += 'rank_type,'
            value_str += str(rank_type)+','

        bayesaverage_subtype = input("bayesaverage_subtype = ")
        if bayesaverage_subtype == '' or bayesaverage_subtype == 'None'  or bayesaverage_subtype == None:
            column_str += ''
        else:
            column_str += 'bayesaverage_subtype,'
            value_str += str(bayesaverage_subtype)+','

        #print bayesaverage_type
        bayesaverage_type = input("bayesaverage_type = ")
        if bayesaverage_type == '' or bayesaverage_type == None or bayesaverage_type == 'None':
            column_str += ''
        else:
            column_str += 'bayesaverage_type,'
            value_str += str(bayesaverage_type)+','

        #print language_dependence
        language_dependence = input("language_dependence = ")
        if language_dependence == '' or language_dependence == None or language_dependence == 'None':
            column_str += ''
        else:
            column_str += 'language_dependence,'
            value_str += str(language_dependence)+','

        suggested_numplayers = input("suggested_numplayers = ")
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

        """
        mechanics = mechanics.rstrip('|').split('|')
        categorys = categorys.rstrip('|').split(pipeline)
        #print mechanics
        #print mechanic_dict['Area Control / Area Influence']
        type_str += type_dict[type] + pipeline
        for mechanic in mechanics:
            mechanism_str += mechanic_dict[mechanic] + pipeline
        for category in categorys:
            #print category
            category_str += category_dict[category] + pipeline
        """
        """
        for designer in designers:
            designer_str += designer.text.replace('"','')+'|'
        for artist in artists:
            artist_str += artist.text+'|'
        for publisher in publishers:
            publisher_str += publisher.text.encode("utf-8")+'|'
        """
        print 'mechanisms should be separate with | and end with |'
        mechanism_str = raw_input("mechanism_str = ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        if mechanism_str == '':
            column_str += ''
        else:
            column_str += 'mechanics,'
            value_str += '"'+str(mechanism_str)+'",'

        type_str = input("type_str = ")
        if type_str == '':
            column_str += ''
        else:
            column_str += 'type,'
            value_str += '"'+str(type_str)+'",'


        designers = raw_input("designers = ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        if designers == '' or designers == 'None':
            column_str += ''
        else:
            column_str += 'designers,'
            value_str += '"'+str(designers)+'",'

        artists = input("artists = ")
        if artists == '' or artists == 'None':
            column_str += ''
        else:
            column_str += 'artists,'
            value_str += '"'+str(artists)+'",'

        print 'categorys should be separate with | and end with |'
        category_str = raw_input("category_str = ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        if category_str == '':
            column_str += ''
        else:
            column_str += 'categorys,'
            value_str += '"'+str(category_str)+'",'

        familys = input("familys = ")
        if familys == '':
            column_str += ''
        else:
            column_str += 'familys,'
            value_str += '"'+str(familys)+'",'

        publishers = raw_input("publishers = ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
        if publishers == '':
            column_str += ''
        else:
            column_str += 'publishers,'
            value_str += '"'+str(publishers)+'",'

        expansions = input("expansions = ")
        if expansions == '':
            column_str += ''
        else:
            column_str += 'expansions,'
            value_str += '"'+str(expansions)+'",'

        subdomain = input("subdomain = ")
        if subdomain == '':
            column_str += ''
        else:
            column_str += 'subdomain,'
            value_str += '"'+str(subdomain)+'",'

        #subdomain = input("subdomain = ")
        if column_str[-1] == ',':
            column_str = column_str[:-1]+')'
        else:
            column_str += ')'

        if value_str[-1] == ',':
            value_str = value_str[:-1]+')'
        else:
            value_str += ')'


    #con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    #con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
        con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
        cur = con.cursor()

        #column_str = "(self.gameid,year,minAge,rateScore,rateNum,rank,weight,minplayer,time,designers,categorys,mechanisms,publishers,maxplayer,bestplayer,self.name)"
        #value_str = str(self.gameid)+','+str(year)+','+str(minAge)+','+str(rateScore)+','+str(rateNum)+','+str(rank)+','+str(weight)+','+str(minplayer)+','+str(time)+','+  \
        #'"'+str(designer_str)+'","'+str(category_str)+'","'+str(mechanism_str)+'","'+str(publisher_str)+'",'+str(maxplayer)+','+str(bestplayer)+',"'+str(self.name)+'"'

        sql = 'REPLACE INTO '+schema_name+'.'+table_name+column_str+'values'+value_str
        #print sql

        try:
            cur.execute(sql)
            con.commit()
            print 'SQL EXECUTION SUCCESS!'
        except Exception,e:
            print 'error when executing sql 2'
            print sql
            #print boardgamepublisher.encode('GBK', 'ignore')
            print e

        cur.close()
        con.close()

        con = mysql.connector.connect(host='180.76.244.130',port=3306,user='mysql',password='MyNewPass4!')
        cur = con.cursor()

        try:
            cur.execute(sql)
            con.commit()
            print 'SQL EXECUTION SUCCESS!'
        except Exception,e:
            print 'error when executing sql 2'
            print sql
            #print boardgamepublisher.encode('GBK', 'ignore')
            print e

        cur.close()
        con.close()

if __name__ == '__main__':
    bgg_xml_reader()