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
from palette import create_colorlist
#from categorylist import *

nameCN_dict = create_gamelist()
color_dict = create_colorlist()

schema_name = 'boardgames'
table_name = 'style_table'

"""
try:
    gameid = int(argv[1])
    color = argv[2]
    environment = argv[3]
except:
    print 'usage: python one_bgg_api.py gameid color local/remote/linux\n'
    print 'choose between local remote and linux\n'
    print 'color could be '
    print color_dict.keys()
    sys.exit(0)
#end_num = start_num + int(argv[2])
"""


default_color = '#999999';
bg_color = '#F4F4F4';


pipeline = '|'
comma = ','
left_par = '('
right_par = ')'
quote = '"'
none_str = 'None'
null_str = ''
var_dict = dict()

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


def bgg_xml_styler(games_dict):
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    base_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{0}?stats=1'
    #con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    #con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
    global column_str, value_str, var_dict
    #game_list = list()
    con = mysql.connector.connect(host='180.76.244.130',port=3306,user='mysql',password='MyNewPass4!')
    cur = con.cursor()

    for gameid in games_dict:
        color = games_dict[gameid][1]
        theme_color = color_dict[color][0]
        content_color = color_dict[color][1]
        #column_str = "(self.gameid,year,minAge,rateScore,rateNum,rank,weight,minplayer,time,designers,categorys,mechanisms,publishers,maxplayer,bestplayer,self.name)"
        #value_str = str(self.gameid)+','+str(year)+','+str(minAge)+','+str(rateScore)+','+str(rateNum)+','+str(rank)+','+str(weight)+','+str(minplayer)+','+str(time)+','+  \
        #'"'+str(designer_str)+'","'+str(category_str)+'","'+str(mechanism_str)+'","'+str(publisher_str)+'",'+str(maxplayer)+','+str(bestplayer)+',"'+str(self.name)+'"'
        column_str = '(gameid,theme_color,content_color,default_color,bg_color)'
        value_str = str((gameid,theme_color,content_color,default_color,bg_color))
        sql = 'REPLACE INTO '+schema_name+'.'+table_name+column_str+'values'+value_str
        print sql

        """
        con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
        cur = con.cursor()
        try:
            cur.execute(sql)
            con.commit()
            print('WINDOWS SQL EXECUTION SUCCESS!')
        except Exception,e:
            print('error when executing sql')
            print(sql)
            #print boardgamepublisher.encode('GBK', 'ignore')
            print(e)

        cur.close()
        con.close()
        """

        try:
            cur.execute(sql)
            con.commit()
            print('LINUX SQL EXECUTION SUCCESS!')
        except Exception,e:
            print('error when executing sql')
            print(sql)
            #print boardgamepublisher.encode('GBK', 'ignore')
            print(e)

    cur.close()
    con.close()

"""
if __name__ == '__main__':
    bgg_xml_styler(games_dict)
"""