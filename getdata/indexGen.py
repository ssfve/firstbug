# -*- coding:utf-8 -*-

import os
import codecs
from api_one import *

schema_name = 'boardgames'
table_name_en = 'bggdata'
table_name_cn = 'bggdatacn'
# img_home = os.getenv('IMG_HOME')

#boardgame_home = os.getenv('BG_HOME')
boardgame_home = "D:/Github/boardgamerules"
pageGenerator_home = os.getenv('PG_HOME')
img_home = os.getenv('IMG_HOME')
# print boardgame_home

slash = '/'
image = 'img'
jsFolder = 'js'
indexFolder = 'index'
pageFolder = 'page'
variablesFolder = 'variables'
index_variables_filename = 'index.variables.js'

# js_page_folder = boardgame_home + slash + jsFolder + slash + pageFolder + slash
js_page_folder = boardgame_home + slash + indexFolder + slash + variablesFolder + slash
# /opt/mount/apache-tomcat-9.0.0.M21/webapps/boardgamerules/index/variables
js_index_path = js_page_folder + index_variables_filename

index_dict = dict()
index_dict['000000'] = ['#']
index_dict['9ZZZZZ'] = ['A']
index_dict['AZZZZZ'] = ['B']
index_dict['BZZZZZ'] = ['C']
index_dict['CZZZZZ'] = ['D']
index_dict['DZZZZZ'] = ['E']
index_dict['EZZZZZ'] = ['F']
index_dict['FZZZZZ'] = ['G']
index_dict['GZZZZZ'] = ['H']
index_dict['HZZZZZ'] = ['I']
index_dict['IZZZZZ'] = ['J']
index_dict['JZZZZZ'] = ['K']
index_dict['KZZZZZ'] = ['L']
index_dict['LZZZZZ'] = ['M']
index_dict['MZZZZZ'] = ['N']
index_dict['NZZZZZ'] = ['O']
index_dict['OZZZZZ'] = ['P']
index_dict['PZZZZZ'] = ['Q']
index_dict['QZZZZZ'] = ['R']
index_dict['RZZZZZ'] = ['S']
index_dict['SZZZZZ'] = ['T']
index_dict['TZZZZZ'] = ['U']
index_dict['UZZZZZ'] = ['V']
index_dict['VZZZZZ'] = ['W']
index_dict['WZZZZZ'] = ['X']
index_dict['XZZZZZ'] = ['Y']
index_dict['YZZZZZ'] = ['Z']

def get_name_en(game_id):
    sql = 'SELECT name FROM '+schema_name+'.'+table_name_en+' WHERE gameid = '+str(game_id)
    # print sql
    try:
        user_platform = platform.system()
        if user_platform == 'Linux':
            con = getdb('Linux_local')
        elif user_platform == 'Windows':
            con = getdb('Linux_remote')
        cur = con.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        con.close()
        data = list(records[0])
        name_en = data[0]
        # print('EN SQL EXECUTION SUCCESS!')
        return name_en
    except Exception as e:
        print(e)


def get_name_cn(game_id):
    sql = 'SELECT nameCN FROM '+schema_name+'.'+table_name_cn+' WHERE gameid = '+str(game_id)
    #print(sql)
    try:
        user_platform = platform.system()
        print(user_platform)
        if user_platform == 'Linux':
            con = getdb('Linux_local')
        elif user_platform == 'Windows':
            con = getdb('Linux_remote')
        cur = con.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        con.close()
        #print(records)
        data = list(records[0])
        # print data
        name_cn = data[0]
        # print('CN SQL EXECUTION SUCCESS!')
        return name_cn
    except Exception as e:
        print("get name cn")
        print(e)


def multi_get_letter(str_input,game_id):
    unicode_str = str_input
    return_list = []
    for one_unicode in unicode_str:
        #if(game_id==203716):
            #print(one_unicode)
        try:
            #if(game_id==203716):
                #print("in")
            letter = single_get_first(one_unicode,game_id).decode("UTF-8")
        except Exception as e:
            #if(game_id==203716):
                #print("in2")
            letter = single_get_first(one_unicode,game_id)
        return_list.append(letter)
        #if(game_id==203716):
    #print(return_list)
    return "".join(return_list)


def single_get_first(unicode_str,game_id):
    str1 = unicode_str.encode('GBK')
    #if(game_id==203716):
        #print(str1)
    try:
        ord(str1)
        # print str1
        return str1
    except Exception as e:
<<<<<<< HEAD
        #print(ord(str1[0]))
        #print(ord(str1[1]))
        #if(game_id==168700):
            #print(str1[0])
            #print(str1[1])
=======
        #print(e)
        # print(ord(str1[0]))
        # print(ord(str1[1]))
        # print(ord('a'))
>>>>>>> 6647068c060619b14f61b5f08ca19560783e398c
        asc = str1[0] * 256 + str1[1] - 65536
        ascPositive = asc + 65536
        # print asc
        #print(ascPositive)
        if -20284 >= asc >= -20319:
            return 'A'
        if -19776 >= asc >= -20283:
            return 'B'
        if -19219 >= asc >= -19775:
            return 'C'
        if -5919 >= asc >= -6471:
            return 'C'
        if -18711 >= asc >= -19218:
            return 'D'
        if ascPositive == 57301:
            return 'D'
        if -18527 >= asc >= -18710:
            return 'E'
        if -18240 >= asc >= -18526:
            return 'F'
        if -17923 >= asc >= -18239:
            return 'G'
        if -17418 >= asc >= -17922:
            return 'H'
        if -16475 >= asc >= -17417:
            return 'J'
        if ascPositive == 48629:
            return 'J'
        if -16213 >= asc >= -16474:
            return 'K'
        if -8239 >= asc >= -8239:
            return 'K'
        if -15641 >= asc >= -16212:
            return 'L'
        if -15166 >= asc >= -15640:
            return 'M'
        if -14923 >= asc >= -15165:
            return 'N'
        if -14915 >= asc >= -14922:
            return 'O'
        if -14631 >= asc >= -14914:
            return 'P'
        if -14150 >= asc >= -14630:
            return 'Q'
        if -14091 >= asc >= -14149:
            return 'R'
        if -13315 >= asc >= -14090:
            return 'S'
        if ascPositive == 57847:
            return 'S'
        if -12839 >= asc >= -13314:
            return 'T'
        if ascPositive == 57514:
            return 'T'
        if 57847 < ascPositive <= 63419:
            return 'T'
        if -12557 >= asc >= -12838:
            return 'W'
        if -11848 >= asc >= -12556:
            return 'X'
        if -11056 >= asc >= -11847:
            return 'Y'
        if -10247 >= asc >= -11055:
            return 'Z'
        return ''


def writejs(games_dict):
    for game_id in games_dict.keys():
        # yprint("in")
        # print(game_id)
        name_cn = get_name_cn(game_id)
        #print(name_cn)
        name_en = get_name_en(game_id)
        # print(name_en)
        capital_key = multi_get_letter(name_cn,game_id)
        #if game_id == 168700:
            #print(capital_key)
        #if game_id == 228867:
            #print(capital_key)
        if capital_key in index_dict:
            capital_key = capital_key + "-1"
        index_dict[capital_key] = [game_id, name_en, name_cn, capital_key]
        # print index_dict[capital_key]
        image_folder = boardgame_home + slash + image + slash + str(game_id)
        image_folder_1 = boardgame_home + slash + image + slash + str(game_id) + slash + 'setup'
        image_folder_2 = boardgame_home + slash + image + slash + str(game_id) + slash + 'flow'
        image_folder_3 = boardgame_home + slash + image + slash + str(game_id) + slash + 'end'
        image_folder_4 = boardgame_home + slash + image + slash + str(game_id) + slash + 'stuff'
        if not os.path.exists(image_folder):
            print("creating folder {}".format(image_folder))
            os.mkdir(image_folder)
        if not os.path.exists(image_folder_1):
            os.mkdir(image_folder_1)
        if not os.path.exists(image_folder_2):
            os.mkdir(image_folder_2)
        if not os.path.exists(image_folder_3):
            os.mkdir(image_folder_3)
        if not os.path.exists(image_folder_4):
            os.mkdir(image_folder_4)
    # print index_dict
    # default open file only accept ascii
    f = codecs.open(js_index_path, 'w', 'utf-8')
    f.write("var index_letters = [];\n")
    f.write("var index_games = [];\n")
    for i, letter in enumerate([chr(x) for x in range(65, 91)]):
        # print letter
        f.write('index_letters['+str(i)+']=\''+letter+'\';\n')
    for i, key in enumerate(sorted(index_dict.keys())):
        # print(key)
        gameinfo = index_dict[key]
        # print(gameinfo)
        if len(gameinfo) == 1:
            f.write(('index_games['+str(i)+']=[\''+gameinfo[0]+'\',\''+gameinfo[0]+'\'];\n'))
        elif len(gameinfo) == 4:
            part_2 = '\',\''+gameinfo[1].replace('\'', '\\\'')+'\',\''
            f.write(('index_games['+str(i)+']=['+str(gameinfo[0])+part_2+gameinfo[2]+'\',\''+gameinfo[3]+'\'];\n'))
    f.close()
    print("WRITTEN TO JS SUCCESS!")
    f = codecs.open("./gamelist", 'w', 'utf-8')
    for i, key in enumerate(sorted(index_dict.keys())):
        gameinfo = index_dict[key]
        #if key == 'JS':
            #print(gameinfo)
        if len(gameinfo) == 1:
            f.write(str(gameinfo[0])+'\n')
        elif len(gameinfo) == 4:
            f.write(str(gameinfo[2])+"-"+str(gameinfo[0])+'\n')
    f.close()
    print("WRITTEN TO LIST SUCCESS!")
    print(len(index_dict.keys())-27)


"""
if __name__ == '__main__':
    write_js()
"""
