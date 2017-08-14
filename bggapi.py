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

schema_name = 'boardgames'
table_name = 'bggdata'

start_num = int(argv[1])
end_num = start_num + int(argv[2])

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


def bgg_xml_reader():
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    base_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{0}?stats=1'
    #con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
    cur = con.cursor()
    global column_str, value_str, var_dict
    for gameid in range(start_num,end_num):
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

        url = base_url.format(gameid)
        print url
        response = urllib2.urlopen(url)
        html = response.read()

        # from file
        #xml = tree.parse(html)
        xml = ET.fromstring(html)

        errors = xml.iter('error')
        for error in errors:
            error_flag = True
            print str(gameid) + pipeline + error.get('message')
        if error_flag == True:
            continue
        # elements is a generator
        elements = xml.iter('yearpublished')
        yearpublished = elements.next().text
        #print yearpublished
        elements = xml.iter('minplayers')
        minplayers = elements.next().text

        elements = xml.iter('maxplayers')
        maxplayers = elements.next().text

        elements = xml.iter('playingtime')
        playingtime = elements.next().text
        #print playingtime

        elements = xml.iter('minplaytime')
        minplaytime = elements.next().text
        #print minplaytime

        elements = xml.iter('maxplaytime')
        maxplaytime = elements.next().text
        #print maxplaytime

        elements = xml.iter('age')
        age = elements.next().text
        #print age

        items = xml.iter('name')
        for item in items:
            if item.get('primary') == 'true':
                name = item.text
        if name != None:
            name = name.replace('"','')
        #print name

        boardgamemechanics = xml.iter('boardgamemechanic')
        for mechanic in boardgamemechanics:
            mechanics += mechanic.text + pipeline
        #print boardgamemechanic

        boardgamefamilys = xml.iter('boardgamefamily')
        for family in boardgamefamilys:
            familys += family.text.replace('"','') + pipeline
        #print boardgamefamily

        boardgamecategorys = xml.iter('boardgamecategory')
        for category in boardgamecategorys:
            categorys += category.text + pipeline
        #print boardgamecategory

        boardgameartists = xml.iter('boardgameartist')
        for artist in boardgameartists:
            artists = artist.text.replace('"','') + pipeline
        #print boardgameartist.encode('GBK', 'ignore')

        boardgamepublishers = xml.iter('boardgamepublisher')
        for publisher in boardgamepublishers:
            #print publisher.text.encode('GBK', 'ignore')
            publishers += publisher.text.replace('"','') + pipeline
        #print boardgamepublisher.encode('GBK', 'ignore')

        boardgamedesigners = xml.iter('boardgamedesigner')
        for designer in boardgamedesigners:
            designers += designer.text.replace('"','') + pipeline
        #print boardgamedesigner.encode('GBK', 'ignore')

        boardgameexpansions = xml.iter('boardgameexpansion')
        for expansion in boardgameexpansions:
            expansions += expansion.text.replace('"','') + pipeline
        #print boardgameexpansion.encode('GBK', 'ignore')


        boardgamesubdomains = xml.iter('boardgamesubdomain')
        for subdomain in boardgamesubdomains:
            subdomains += subdomain.text + pipeline
        #print boardgamesubdomain

        polls = xml.iter('poll')
        for poll in polls:
            if poll.get('name') == 'suggested_numplayers':
                numvotes = 0
                for results_set in poll.iter('results'):
                    for result in results_set.iter('result'):
                        if result.get('value') == 'Best':
                            temp_votes = int(result.get('numvotes'))
                            if temp_votes > numvotes:
                                numvotes = temp_votes
                                suggested_numplayers = results_set.get('numplayers')
            if poll.get('name') == 'language_dependence':
                numvotes = 0
                for results_set in poll.iter('results'):
                    for result in results_set.iter('result'):
                        temp_votes = int(result.get('numvotes'))
                        if temp_votes > numvotes:
                            numvotes = temp_votes
                            language_dependence = result.get('level')
            if poll.get('name') == 'suggested_playerage':
                numvotes = 0
                for results_set in poll.iter('results'):
                    for result in results_set.iter('result'):
                        temp_votes = int(result.get('numvotes'))
                        if temp_votes > numvotes:
                            numvotes = temp_votes
                            suggested_playerage = result.get('value')
        #print suggested_numplayers
        #print language_dependence
        #print suggested_playerage

        statistics = xml.iter('statistics')
        for statistic in statistics:
            usersrated = statistic.find('ratings').find('usersrated').text
            average = statistic.find('ratings').find('average').text
            numweights = statistic.find('ratings').find('numweights').text
            averageweight = statistic.find('ratings').find('averageweight').text
            #bayesaverage_subtype = statistic.find('ratings').find('bayesaverage').text
            ranks = statistic.find('ratings').find('ranks')
            for rank in ranks:
                #print rank.get('type')
                #print rank.get('friednlyname')
                if rank.get('type') == "subtype":
                    bayesaverage_subtype = rank.get('bayesaverage')
                    rank_subtype = rank.get('value')
                if rank.get('type') != "subtype":
                    game_type = rank.get('type')
                    bayesaverage_type = rank.get('bayesaverage')
                    rank_type = rank.get('value')
        #print usersrated
        #print average
        #print bayesaverage_subtype
        #print rank_subtype
        #print bayesaverage_type
        #print rank_type
        #print numweights
        #print averageweight
        #print game_type
        var_dict['yearpublished']=yearpublished
        var_dict['age']=age
        var_dict['minplaytime']=minplaytime
        var_dict['maxplaytime']=maxplaytime
        var_dict['minplayers']=minplayers
        var_dict['maxplayers']=maxplayers
        var_dict['suggested_playerage']=suggested_playerage
        var_dict['average']=average
        var_dict['averageweight']=averageweight
        var_dict['numweights']=numweights
        var_dict['usersrated']=usersrated

        #print gameid
        column_str = left_par + 'gameid' + comma
        value_str = left_par + str(gameid) + comma

        #print column_str
        #print value_str
        #print name
        if name == '' or name =='None':
            column_str += ''
        else:
            column_str += 'name,'
            value_str += '"'+str(name)+'",'

        sql_gen('yearpublished')
        sql_gen('age')
        sql_gen('minplaytime')
        sql_gen('maxplaytime')
        sql_gen('minplayers')
        sql_gen('maxplayers')
        sql_gen('suggested_playerage')
        sql_gen('average')
        sql_gen('averageweight')
        sql_gen('numweights')
        sql_gen('usersrated')

        #print rank_subtype
        if rank_subtype == '' or rank_subtype =='NOT Ranked' or rank_subtype =='Not Ranked':
            #print 'hello'
            column_str += ''
        else:
            column_str += 'rank_subtype,'
            value_str += str(rank_subtype)+','

        #print rank_subtype
        if rank_type == '' or rank_type =="NOT Ranked"  or rank_type =='Not Ranked':
            column_str += ''
        else:
            column_str += 'rank_type,'
            value_str += str(rank_type)+','

        #print rank_subtype
        if bayesaverage_subtype == '' or bayesaverage_subtype=="NOT Ranked"  or bayesaverage_subtype=='Not Ranked':
            column_str += ''
        else:
            column_str += 'bayesaverage_subtype,'
            value_str += str(bayesaverage_subtype)+','

        #print rank_subtype
        if bayesaverage_type == '' or bayesaverage_type =="NOT Ranked"  or bayesaverage_type =='Not Ranked':
            column_str += ''
        else:
            column_str += 'bayesaverage_type,'
            value_str += str(bayesaverage_type)+','

        #print language_dependence
        if language_dependence == '' or language_dependence == 'None':
            column_str += ''
        else:
            column_str += 'language_dependence,'
            value_str += str(language_dependence)+','

        var_dict['suggested_numplayers']=suggested_numplayers
        var_dict['mechanics']=mechanics
        var_dict['designers']=designers
        var_dict['artists']=artists
        var_dict['categorys']=categorys
        var_dict['familys']=familys
        var_dict['publishers']=publishers
        var_dict['expansions']=expansions

        sql_gen_str('suggested_numplayers')
        sql_gen_str('mechanics')
        sql_gen_str('designers')
        sql_gen_str('artists')
        sql_gen_str('categorys')
        sql_gen_str('familys')
        sql_gen_str('publishers')
        sql_gen_str('expansions')

        #print rank_subtype
        if game_type == '':
            column_str += ''
        else:
            column_str += 'type,'
            value_str += '"'+str(game_type)+'",'

        if subdomains == '':
            column_str += ''
        else:
            column_str += 'subdomain,'
            value_str += '"'+str(subdomains)+'",'


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

        sql = 'REPLACE INTO '+schema_name+'.'+table_name+column_str+'values'+value_str
        #print sql

        try:
            cur.execute(sql)
            con.commit()
            print 'SQL EXECUTION SUCCESS!'
        except Exception,e:
            print 'error when executing sql'
            print sql
            #print boardgamepublisher.encode('GBK', 'ignore')
            print e

    cur.close()
    con.close()

if __name__ == '__main__':
    bgg_xml_reader()