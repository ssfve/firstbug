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

nameCN_dict[134352] = u'两室一弹'
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

#start_num = int(argv[1])
#end_num = start_num + int(argv[2])

type_dict = dict()
type_dict['Abstract Strategy Games (like Chess or Go)']='抽象'
type_dict['Customizable Games (CCGs CMGs LCGs etc)']='集换/自组'
type_dict['Thematic Games (emphasis on narrative)']='美式剧情'
type_dict['family']='家庭游戏'
type_dict['Children']='儿童游戏'
type_dict['Party Games (few rules lots of laughs)']='聚会游戏'
type_dict['Strategy Games (more complex games)']='德式策略'
type_dict['Wargames (conflict simulation etc.)']='战棋'
type_dict['None']='无'

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

mechanic_dict = dict()
mechanic_dict['Acting']='表演'
mechanic_dict['Action / Movement Programming']='行动编程'
mechanic_dict['Action Point Allowance System']='行动点分配'
mechanic_dict['Area Control / Area Influence']='区域控制'
mechanic_dict['Area Enclosure']='区域断围'
mechanic_dict['Area Movement']='区域移动'
mechanic_dict['Area-Impulse']='区域脉冲'
mechanic_dict['Auction/Bidding']='拍卖'
mechanic_dict['Betting/Wagering']='押注'
mechanic_dict['Campaign / Battle Card Driven']='卡驱'
mechanic_dict['Card Drafting']='卡牌轮选'
mechanic_dict['Chit-Pull System']='板块暗抽'
mechanic_dict['Co-operative Play']='合作'
mechanic_dict['Commodity Speculation']='货品估价'
mechanic_dict['Crayon Rail System']='画线连接'
mechanic_dict['Deck / Pool Building']='池库构筑(DBG)'
mechanic_dict['Dice Rolling']='掷骰'
mechanic_dict['Grid Movement']='区格移动'
mechanic_dict['Hand Management']='手牌管理'
mechanic_dict['Hex-and-Counter']='六边格+算子'
mechanic_dict['Line Drawing']='画线图'
mechanic_dict['Memory']='记忆'
mechanic_dict['Modular Board']='模组版图'
mechanic_dict['Paper-and-Pencil']='纸笔跑团'
mechanic_dict['Partnerships']='阵营组队'
mechanic_dict['Pattern Building']='创造图案'
mechanic_dict['Pattern Recognition']='图案识别'
mechanic_dict['Pick-up and Deliver']='取物递送'
mechanic_dict['Player Elimination']='玩家淘汰'
mechanic_dict['Point to Point Movement']='点对点移动'
mechanic_dict['Press Your Luck']='拼人品'
mechanic_dict['Rock-Paper-Scissors']='石头剪子布'
mechanic_dict['Role Playing']='角色扮演'
mechanic_dict['Roll / Spin and Move']='掷/转移动'
mechanic_dict['Route/Network Building']='路网建设'
mechanic_dict['Secret Unit Deployment']='秘密部署'
mechanic_dict['Set Collection']='收集成套'
mechanic_dict['Simulation']='模拟'
mechanic_dict['Simultaneous Action Selection']='同时选择行动'
mechanic_dict['Singing']='歌唱'
mechanic_dict['Stock Holding']='股票投资'
mechanic_dict['Storytelling']='编讲故事'
mechanic_dict['Take That']='接招'
mechanic_dict['Tile Placement']='板块拼置'
mechanic_dict['Time Track']='时间轴'
mechanic_dict['Trading']='交易'
mechanic_dict['Trick-taking']='吃墩'
mechanic_dict['Variable Phase Order']='可变流程'
mechanic_dict['Variable Player Powers']='多样玩家能力'
mechanic_dict['Voting']='投票'
mechanic_dict['Worker Placement']='工人放置'
mechanic_dict['None']='无'

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
    #con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
    con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')
    cur = con.cursor()

    for gameid in nameCN_dict.keys():
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