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
index_dict['00'] = ['#']
index_dict['A0'] = ['A']
index_dict['B0'] = ['B']
index_dict['C0'] = ['C']
index_dict['D0'] = ['D']
index_dict['E0'] = ['E']
index_dict['F0'] = ['F']
index_dict['G0'] = ['G']
index_dict['H0'] = ['H']
index_dict['I0'] = ['I']
index_dict['J0'] = ['J']
index_dict['K0'] = ['K']
index_dict['L0'] = ['L']
index_dict['M0'] = ['M']
index_dict['N0'] = ['N']
index_dict['O0'] = ['O']
index_dict['P0'] = ['P']
index_dict['Q0'] = ['Q']
index_dict['R0'] = ['R']
index_dict['S0'] = ['S']
index_dict['T0'] = ['T']
index_dict['U0'] = ['U']
index_dict['V0'] = ['V']
index_dict['W0'] = ['W']
index_dict['X0'] = ['X']
index_dict['Y0'] = ['Y']
index_dict['Z0'] = ['Z']

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
        # print records
        data = list(records[0])
        # print data
        name_cn = data[0]
        # print('CN SQL EXECUTION SUCCESS!')
        return name_cn
    except Exception as e:
        print("get name cn")
        print(e)


def multi_get_letter(str_input):
    unicode_str = str_input
    return_list = []
    for one_unicode in unicode_str:
        # print one_unicode
        try:
            letter = single_get_first(one_unicode).decode("UTF-8")
        except Exception as e:
            print(e)
            letter = single_get_first(one_unicode)
        return_list.append(letter)
    # print(return_list)
    return "".join(return_list)


def single_get_first(unicode_str):
    str1 = unicode_str.encode('GBK')
    # print(str1)
    try:
        ord(str1)
        # print str1
        return str1
    except Exception as e:
        #print(e)
        # print(ord(str1[0]))
        # print(ord(str1[1]))
        # print(ord('a'))
        asc = str1[0] * 256 + str1[1] - 65536
        # print asc
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
        if -12839 >= asc >= -13314:
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
        print("in")
        # print game_id
        name_cn = get_name_cn(game_id)
        # print(name_cn)
        name_en = get_name_en(game_id)
        # print(name_en)
        capital_key = multi_get_letter(name_cn)
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
        if len(gameinfo) == 1:
            f.write(str(gameinfo[0])+'\n')
        elif len(gameinfo) == 4:
            f.write(str(gameinfo[2])+'\n')
    f.close()
    print("WRITTEN TO LIST SUCCESS!")
    print(len(index_dict.keys())-27)


"""
if __name__ == '__main__':
    write_js()
"""
