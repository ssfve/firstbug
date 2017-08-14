# -*- coding:utf-8 -*-

import os
import io
import requests
import random
from faker import Factory
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

nameCN_dict = dict()

nameCN_dict[42] = u'两河流域'

nameCN_dict[521] = u'加拿大棋'
nameCN_dict[811] = u'拉密'
nameCN_dict[822] = u'卡卡颂'

nameCN_dict[1406] = u'大富翁'
nameCN_dict[2453] = u'角斗士'

nameCN_dict[8946] = u'达芬奇密码'
nameCN_dict[8098] = u'图腾快手'
nameCN_dict[9209] = u'车票之旅'


nameCN_dict[65244] = u'禁闭岛'

nameCN_dict[81453] = u'家族'
nameCN_dict[85256] = u'时间线'
nameCN_dict[98778] = u'花火'

nameCN_dict[103343] = u'权力的游戏(第二版)'

nameCN_dict[129622] = u'情书'

nameCN_dict[136063] = u'禁闭沙漠'

nameCN_dict[147949] = u'一夜终极狼人'
nameCN_dict[148228] = u'璀璨宝石'
nameCN_dict[148949] = u'伊斯坦布尔'

nameCN_dict[155821] = u'翠屿秘境'
nameCN_dict[163412] = u'拼布艺术'
nameCN_dict[167791] = u'火星开发计划'

nameCN_dict[209010] = u'约德尔战斗学院'
nameCN_dict[209685] = u'香料之路'


nameCN_dict[215312] = u'小偷别跑'





schema_name = 'boardgames'
table_name = 'bggdata'
table_name_cn = 'bggdatacn'

start_num = int(argv[1])
end_num = start_num + int(argv[2])

type_dict = {
    u'Abstract Strategy Games (like Chess or Go)':u'抽象',
    u'Customizable Games (CCGs, CMGs, LCGs, etc)':u'集换/自组',
    u'Thematic Games (emphasis on narrative)':u'美式剧情',
    u'family':u'家庭游戏',
    u'Children':u'儿童游戏',
    u'Party Games (few rules, lots of laughs)':u'聚会游戏',
    u'Strategy Games (more complex games)':u'德式策略',
    u'Wargames (conflict simulation, etc.)':u'战棋',
    u'None':u'无'
}

category_dict = dict()
category_dict['Abstract Strategy']='抽象'
category_dict['Action / Dexterity']='动作'
category_dict['Adventure']='冒险'
category_dict['Age of Reason']=''
category_dict['American Civil War']='美国内战'
category_dict['American Indian Wars']=''
category_dict['American Revolutionary War']=''
category_dict['American West']=''
category_dict['Ancient']='古代'
category_dict['Animals']='动物'
category_dict['Arabian']='阿拉伯'
category_dict['Aviation / Flight']=''
category_dict['Bluffing']='吹牛'
category_dict['Book']=''
category_dict['Card Game']='卡牌游戏'
category_dict['Children\'s Game']='儿童游戏'
category_dict['City Building']='城市建设'
category_dict['Civil War']='内战'
category_dict['Civilization']='文明'
category_dict['Collectible Components']='配件收藏'
category_dict['Comic Book / Strip']='美漫'
category_dict['Deduction']='推理'
category_dict['Dice']='骰子'
category_dict['Economic']='经济运营'
category_dict['Educational']='教育'
category_dict['Electronic']='电子'
category_dict['Environmental']='环保'
category_dict['Expansion for Base-game']='扩展'
category_dict['Exploration']='探索'
category_dict['Fan Expansion']='民间扩展'
category_dict['Fantasy']='奇幻'
category_dict['Farming']='农事'
category_dict['Fighting']='战斗/互车'
category_dict['Game System']=''
category_dict['Horror']='恐怖'
category_dict['Humor']='幽默'
category_dict['Industry / Manufacturing']='工业制造'
category_dict['Korean War']='朝鲜战争'
category_dict['Mafia']='黑帮'
category_dict['Math']='数学'
category_dict['Mature / Adult']='成人'
category_dict['Maze']='迷宫'
category_dict['Medical']=''
category_dict['Medieval']='中世纪'
category_dict['Memory']='记忆'
category_dict['Miniatures']='模型'
category_dict['Modern Warfare']=''
category_dict['Movies / TV / Radio theme']='影视改编'
category_dict['Murder/Mystery']='谜案'
category_dict['Music']='音乐'
category_dict['Mythology']='神话'
category_dict['Napoleonic']=''
category_dict['Nautical']='航海'
category_dict['Negotiation']='嘴炮谈判'
category_dict['Novel-based']='小说改编'
category_dict['Number']='数字'
category_dict['Party Game']='聚会游戏'
category_dict['Pike and Shot']=''
category_dict['Pirates']='海盗'
category_dict['Political']='政治'
category_dict['Post-Napoleonic']=''
category_dict['Prehistoric']='史前'
category_dict['Print & Play']='即印即玩'
category_dict['Puzzle']='拼解通关'
category_dict['Racing']='竞速'
category_dict['Real-time']='实时'
category_dict['Religious']='宗教信仰'
category_dict['Renaissance']='文艺复兴'
category_dict['Science Fiction']='科幻'
category_dict['Space Exploration']=''
category_dict['Spies/Secret Agents']='间谍卧底'
category_dict['Sports']='体育'
category_dict['Territory Building']='领土扩张'
category_dict['Trains']='火车'
category_dict['Transportation']='运输'
category_dict['Travel']='旅行'
category_dict['Trivia']='冷知识'
category_dict['Video Game Theme']='电游改编'
category_dict['Vietnam War']='越南战争'
category_dict['Wargame']='战棋'
category_dict['Word Game']=''
category_dict['World War I']='一战'
category_dict['World War II']='二战'
category_dict['Zombies']='僵尸'
category_dict['None']='无'

mechanic_dict = {
    u'Acting':u'表演',
    u'Action / Movement Programming':u'行动编程',
    u'Action Point Allowance System':u'行动点分配',
    u'Area Control / Area Influence':u'区域控制',
    u'Area Enclosure':u'区域断围',
    u'Area Movement':u'区域移动',
    u'Area-Impulse':u'区域脉冲',
    u'Auction/Bidding':u'拍卖',
    u'Betting/Wagering':u'押注',
    u'Campaign / Battle Card Driven':u'卡驱',
    u'Card Drafting':u'卡牌轮选',
    u'Chit-Pull System':u'板块暗抽',
    u'Co-operative Play':u'合作',
    u'Commodity Speculation':u'货品估价',
    u'Crayon Rail System':u'画线连接',
    u'Deck / Pool Building':u'池库构筑(DBG)',
    u'Dice Rolling':u'掷骰',
    u'Grid Movement':u'区格移动',
    u'Hand Management':u'手牌管理',
    u'Hex-and-Counter':u'六边格+算子',
    u'Line Drawing':u'画线图',
    u'Memory':u'记忆',
    u'Modular Board':u'模组版图',
    u'Paper-and-Pencil':u'纸笔跑团',
    u'Partnerships':u'阵营组队',
    u'Pattern Building':u'创造图案',
    u'Pattern Recognition':u'图案识别',
    u'Pick-up and Deliver':u'取物递送',
    u'Player Elimination':u'玩家淘汰',
    u'Point to Point Movement':u'点对点移动',
    u'Press Your Luck':u'拼人品',
    u'Rock-Paper-Scissors':u'石头剪子布',
    u'Role Playing':u'角色扮演',
    u'Roll / Spin and Move':u'掷/转移动',
    u'Route/Network Building':u'路网建设',
    u'Secret Unit Deployment':u'秘密部署',
    u'Set Collection':u'收集成套',
    u'Simulation':u'模拟',
    u'Simultaneous Action Selection':u'同时选择行动',
    u'Singing':u'歌唱',
    u'Stock Holding':u'股票投资',
    u'Storytelling':u'编讲故事',
    u'Take That':u'接招',
    u'Tile Placement':u'板块拼置',
    u'Time Track':u'时间轴',
    u'Trading':u'交易',
    u'Trick-taking':u'吃墩',
    u'Variable Phase Order':u'可变流程',
    u'Variable Player Powers':u'多样玩家能力',
    u'Voting':u'投票',
    u'Worker Placement':u'工人放置',
    u'None':u'无'
}



pipeline = '|'

def bgg_xml_reader():
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
    con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    cur = con.cursor()

    for gameid in range(start_num,end_num):
        try:
            sql = 'SELECT * FROM '+schema_name+'.'+table_name+' where gameid = '+str(gameid)
            print sql
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
            if nameCN_dict.has_key(gameid):
                nameCN = str(nameCN_dict[gameid])
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
        categorys = categorysCN.rstrip('|').split(pipeline)
        #print mechanics
        #print mechanic_dict['Area Control / Area Influence']
        type_str += type_dict[typeCN] + pipeline
        for mechanic in mechanics:
            mechanism_str += mechanic_dict[mechanic] + pipeline
        for category in categorys:
            #print category
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
            value_str += '"'+str(designersCN)+'",'

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