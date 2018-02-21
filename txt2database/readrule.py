# -*- coding:utf-8 -*-

import os
import locale
import io
import requests
import random
#from faker import Factory
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sys import argv
import re
import io
import codecs

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import urllib2
import mysql.connector
#from mysql.connector import connection

from gamelist import create_gamelist
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
table_name_src = 'bggdata'
table_name_dst = 'raw_text_table'

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

def guess_notepad_encoding(filepath, default_ansi_encoding=None):
    with open(filepath, 'rb') as f:
        data = f.read(3)
    if data[:2] in ('\xff\xfe', '\xfe\xff'):
        return 'utf-16'
    if data == u''.encode('utf-8-sig'):
        return 'utf-8-sig'
    # presumably "ANSI"
    return default_ansi_encoding or locale.getpreferredencoding()
    
def txt_reader(games_dict):
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
            sql = 'SELECT * FROM '+schema_name+'.'+table_name_src+' where gameid = '+str(gameid)
            print sql
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



        files = os.listdir(str(gameid))
        for file in files:
            print file
            if re.match('.*txt$',file):
                filename = file
                
        enc = guess_notepad_encoding(str(gameid)+"/"+filename)
        with codecs.open(str(gameid)+"/"+filename,'r',enc) as fp:
            line = fp.readline()
            count = 1
            while line:
                column_str = '('
                value_str = '('
                column_str += 'gameid,'
                value_str += str(gameid)+','
                column_str += 'lineNum,'
                value_str += str(count)+','
                column_str += 'text_content,'
                value_str += '"'+str(line)+'",'
                column_str += 'textID,'
                value_str += '"'+str(gameid)+"-"+str(count)+'",'
                if column_str[-1] == ',':
                    column_str = column_str[:-1]+')'
                else:
                    column_str += ')'

                if value_str[-1] == ',':
                    value_str = value_str[:-1]+')'
                else:
                    value_str += ')'
                sql = 'REPLACE INTO '+schema_name+'.'+table_name_dst+column_str+'values'+value_str
                #print sql
                """
                try:
                    cur.execute(sql)
                    con.commit()
                    print('WINDOWS SQL EXECUTION SUCCESS!')
                except Exception,e:
                    print 'error when executing sql 2'
                    print sql
                    #print boardgamepublisher.encode('GBK', 'ignore')
                    print e

                cur.close()
                con.close()
                """
                con = mysql.connector.connect(host='180.76.244.130',port=3306,user='mysql',password='MyNewPass4!')
                cur = con.cursor()
                try:
                    cur.execute(sql)
                    con.commit()
                    print('LINUX SQL EXECUTION SUCCESS!')
                except Exception,e:
                    print 'error when executing sql 2'
                    print sql
                    #print boardgamepublisher.encode('GBK', 'ignore')
                    print e
                cur.close()
                con.close()
                line = fp.readline()
                count += 1
"""
if __name__ == '__main__':
    bgg_xml_translater()
"""