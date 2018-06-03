# -*- coding:utf-8 -*-

import platform
import datetime
from datetime import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from urllib.request import urlopen
import mysql.connector
from gamelist import create_game_list

nameCN_dict = create_game_list()
schema_name = 'boardgames'
table_name = 'bggdata'

"""
try:
    gameid = int(argv[1])
    environment = argv[2]
except:
    print 'usage: python one_bgg_api.py gameid local/remote/linux'
    sys.exit(0)
#end_num = start_num + int(argv[2])
"""

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


def bgg_xml_reader(games_dict):
    #start_urls = 'https://www.boardgamegeek.com/boardgame/3076'
    base_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{0}?stats=1'

    global column_str, value_str, var_dict

    #game_list = list()
    #game_list.append(gameid)
    #for gameid in range(start_num,end_num):
    for gameid in games_dict:
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
        name= ''
        error_flag = False
        BGG_flag = True
        
        bayesaverage_subtype = ''
        rank_subtype = ''
        bayesaverage_type = ''
        rank_type = ''
        url = base_url.format(gameid)
        print(url)
        response = urlopen(url)
        html = response.read()

        # from file
        #xml = tree.parse(html)
        xml = ET.fromstring(html)

        errors = xml.iter('error')
        for error in errors:
            error_flag = True
            print(str(gameid) + pipeline + error.get('message'))
        if error_flag == True:
            default_enabled = input("Is this a game not in BGG?(y/n): ")
            if(default_enabled == 'y'):
                BGG_flag = False
            else:
                BGG_flag = True
                print("skipping this game")
                continue
        # elements is a generator
        if(BGG_flag):
            elements = xml.iter('yearpublished')
            yearpublished = next(elements).text
            elements = xml.iter('minplayers')
            minplayers = next(elements).text
            elements = xml.iter('maxplayers')
            maxplayers = next(elements).text
            elements = xml.iter('playingtime')
            playingtime = next(elements).text
            elements = xml.iter('minplaytime')
            minplaytime = next(elements).text
            elements = xml.iter('maxplaytime')
            maxplaytime = next(elements).text
            elements = xml.iter('age')
            age = next(elements).text
            items = xml.iter('name')
            for item in items:
                if item.get('primary') == 'true':
                    name = item.text
            if name != None:
                name = name.replace('"', '')
            boardgamemechanics = xml.iter('boardgamemechanic')
            for mechanic in boardgamemechanics:
                mechanics += mechanic.text + pipeline
            # print boardgamemechanic

            boardgamefamilys = xml.iter('boardgamefamily')
            for family in boardgamefamilys:
                familys += family.text.replace('"', '') + pipeline
            # print boardgamefamily

            boardgamecategorys = xml.iter('boardgamecategory')
            for category in boardgamecategorys:
                categorys += category.text + pipeline
            # print boardgamecategory

            boardgameartists = xml.iter('boardgameartist')
            for artist in boardgameartists:
                artists = artist.text.replace('"', '') + pipeline
            # print boardgameartist.encode('GBK', 'ignore')

            boardgamepublishers = xml.iter('boardgamepublisher')
            for publisher in boardgamepublishers:
                # print publisher.text.encode('GBK', 'ignore')
                publishers += publisher.text.replace('"', '') + pipeline
            # print boardgamepublisher.encode('GBK', 'ignore')

            boardgamedesigners = xml.iter('boardgamedesigner')
            for designer in boardgamedesigners:
                designers += designer.text.replace('"', '') + pipeline
            # print boardgamedesigner.encode('GBK', 'ignore')

            boardgameexpansions = xml.iter('boardgameexpansion')
            for expansion in boardgameexpansions:
                expansions += expansion.text.replace('"', '') + pipeline
            # print boardgameexpansion.encode('GBK', 'ignore')

            boardgamesubdomains = xml.iter('boardgamesubdomain')
            for subdomain in boardgamesubdomains:
                subdomains += subdomain.text + pipeline
            # print boardgamesubdomain
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
            # print suggested_numplayers
            # print language_dependence
            # print suggested_playerage

            statistics = xml.iter('statistics')
            for statistic in statistics:
                usersrated = statistic.find('ratings').find('usersrated').text
                average = statistic.find('ratings').find('average').text
                numweights = statistic.find('ratings').find('numweights').text
                averageweight = statistic.find('ratings').find('averageweight').text
                # bayesaverage_subtype = statistic.find('ratings').find('bayesaverage').text
                ranks = statistic.find('ratings').find('ranks')
                for rank in ranks:
                    # print rank.get('type')
                    # print rank.get('friednlyname')
                    if rank.get('type') == "subtype":
                        bayesaverage_subtype = rank.get('bayesaverage')
                        rank_subtype = rank.get('value')
                    if rank.get('type') != "subtype":
                        game_type = rank.get('type')
                        bayesaverage_type = rank.get('bayesaverage')
                        rank_type = rank.get('value')
            # print usersrated
            # print average
            # print bayesaverage_subtype
            # print rank_subtype
            # print bayesaverage_type
            # print rank_type
            # print numweights
            # print averageweight
            # print game_type
        else:
            currentYear = datetime.now().year
            yearpublished = input("Please input yearpublished (default:{}):".format(currentYear))
            while((len(yearpublished)!=4) or (not(yearpublished.isdigit()))):
                if (yearpublished == ""):
                    yearpublished = currentYear
                    break
                else:
                    print("year format error")
                    yearpublished = input("Please input yearpublished (default:{}):".format(currentYear))
            print(yearpublished)

            default_minplayers = 1
            minplayers = input("Please input minplayers (default:{}):".format(default_minplayers))
            while ((not (minplayers.isdigit()))):
                if (minplayers == ""):
                    minplayers = default_minplayers
                    break
                else:
                    print("minplayers format error")
                    minplayers = input("Please input minplayers (default:{}):".format(default_minplayers))
            print(minplayers)

            default_maxplayers = 4
            maxplayers = input("Please input maxplayers (default:{}):".format(default_maxplayers))
            while ((not (maxplayers.isdigit()))):
                if (maxplayers == ""):
                    maxplayers = default_maxplayers
                    break
                else:
                    print("maxplayers format error")
                    maxplayers = input("Please input maxplayers (default:{}):".format(default_maxplayers))
            print(maxplayers)

            default_playingtime = 30
            playingtime = input("Please input playingtime (default:{}):".format(default_playingtime))
            while ((not (playingtime.isdigit()))):
                if (playingtime == ""):
                    playingtime = default_playingtime
                    break
                else:
                    print("playingtime format error")
                    playingtime = input("Please input playingtime (default:{}):".format(default_playingtime))
            print(playingtime)

            default_minplaytime = 10
            minplaytime = input("Please input minplaytime (default:{}):".format(default_minplaytime))
            while ((not (minplaytime.isdigit()))):
                if (minplaytime == ""):
                    minplaytime = default_minplaytime
                    break
                else:
                    print("minplaytime format error")
                    minplaytime = input("Please input minplaytime (default:{}):".format(default_minplaytime))
            print(minplaytime)

            default_maxplaytime = 60
            maxplaytime = input("Please input maxplaytime (default:{}):".format(default_maxplaytime))
            while ((not (maxplaytime.isdigit()))):
                if (maxplaytime == ""):
                    maxplaytime = default_maxplaytime
                    break
                else:
                    print("maxplaytime format error")
                    maxplaytime = input("Please input maxplaytime (default:{}):".format(default_maxplaytime))
            print(maxplaytime)

            default_age= 8
            age = input("Please input age (default:{}):".format(default_age))
            while ((not (age.isdigit()))):
                if (age == ""):
                    age = default_age
                    break
                else:
                    print("age format error")
                    age = input("Please input age (default:{}):".format(default_age))
            print(age)

            default_suggested_playerage = 8
            suggested_playerage = input("Please input suggested_playerage (default:{}):".format(default_suggested_playerage))
            while ((not (suggested_playerage.isdigit()))):
                if (suggested_playerage == ""):
                    suggested_playerage = default_suggested_playerage
                    break
                else:
                    print("suggested_playerage format error")
                    suggested_playerage = input("Please input suggested_playerage (default:{}):".format(default_suggested_playerage))
            print(suggested_playerage)

            default_suggested_numplayers = 4
            suggested_numplayers = input("Please input suggested_numplayers (default:{}):".format(default_suggested_numplayers))
            while ((not (suggested_numplayers.isdigit()))):
                if (suggested_numplayers == ""):
                    suggested_numplayers = default_suggested_numplayers
                    break
                else:
                    print("suggested_numplayers format error")
                    suggested_numplayers = input(
                        "Please input suggested_numplayers (default:{}):".format(default_suggested_numplayers))
            print(suggested_numplayers)

            default_language_dependence = 3
            language_dependence = input(
                "Please input language_dependence (default:{}):".format(default_language_dependence))
            while ((not (language_dependence.isdigit()))):
                if (language_dependence == ""):
                    language_dependence = default_language_dependence
                    break
                else:
                    print("language_dependence format error")
                    language_dependence = input(
                        "Please input language_dependence (default:{}):".format(default_language_dependence))
            print(language_dependence)

            confirm_flag = "n"
            while(confirm_flag == "n"):
                name = input("Please input English name:")
                print("English name is {}".format(name))
                confirm_flag = input("Please confirm(y/n):")
            print(name)

            confirm_flag = "n"
            while (confirm_flag == "n"):
                designers = input("Please input designers(separated by comma):")
                print("designers is {}".format(designers))
                confirm_flag = input("Please confirm(y/n):")
            print(designers)

            confirm_flag = "n"
            while (confirm_flag == "n"):
                artists = input("Please input artists(separated by comma):")
                print("artists is {}".format(artists))
                confirm_flag = input("Please confirm(y/n):")
            print(artists)

            average=0
            averageweight=0
            numweights=0
            usersrated=0

            mechanics=""
            categorys=""
            familys=""
            publishers=""
            expansions=""



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
        #print(sql)
        
        userPlatform=platform.system()
        if(userPlatform=='Linux'):
            con = getdb('Linux_local')
            writedb(con,sql)
            print(userPlatform+' SQL EXECUTION SUCCESS!')
        elif(userPlatform=='Windows'):
            con = getdb('Windows_local')
            writedb(con,sql)
            print(userPlatform+' SQL EXECUTION SUCCESS!')
            con = getdb('Linux_remote')
            writedb(con,sql)
            print('Linux_remote SQL EXECUTION SUCCESS!')
            

def getdb(userPlatform):
    passwd_dict=dict()
    passwd_dict['Windows_local']=('localhost',3306,'root','b0@rdg@merule5')
    passwd_dict['Linux_remote']=('180.76.244.130',3306,'mysql','MyNewPass4!')
    passwd_dict['Linux_local']=('localhost',3306,'mysql','MyNewPass4!')
    
    pst = passwd_dict[userPlatform]
    #print(pst[0])
    con = mysql.connector.connect(host=pst[0],port=pst[1],user=pst[2],password=pst[3])
    return con
    
def writedb(con,sql):
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except Exception as e:
        print(sql)
        print(e)
    cur.close()
    con.close()
"""
if __name__ == '__main__':
    bgg_xml_reader()
"""
