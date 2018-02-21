from sys import argv
import codecs

import platform
from api_one import *
from gamelist import create_gamelist
import mysql.connector

nameCN_dict = create_gamelist()
import os


from sys import argv

"""
try:
    environment = argv[1]
Exception:
    print 'usage: python index_gen.py'
"""
schema_name = 'boardgames'
table_name_en = 'bggdata'
table_name_cn = 'bggdatacn'
#img_home = os.getenv('IMG_HOME')

boardgame_home = os.getenv('BG_HOME')
pageGenerator_home = os.getenv('PG_HOME')
img_home = os.getenv('IMG_HOME')
#print boardgame_home

slash = '/'
image = 'img'
jsFolder = 'js'
indexFolder = 'index'
pageFolder = 'page'
variablesFolder = 'variables'
index_variables_filename = 'index.variables.js'

#js_page_folder = boardgame_home + slash + jsFolder + slash + pageFolder + slash

js_page_folder = boardgame_home + slash + indexFolder + slash + variablesFolder + slash
#/opt/mount/apache-tomcat-9.0.0.M21/webapps/boardgamerules/index/variables

js_index_path = js_page_folder + index_variables_filename
cur = None

def getnameEN(gameid):
    global cur
    sql = 'SELECT name FROM '+schema_name+'.'+table_name_en+' WHERE gameid = '+str(gameid)
        #print sql
    try:
        cur.execute(sql)
        records = cur.fetchall()
        data = list(records[0])
        nameEN = data[0]
        #print('EN SQL EXECUTION SUCCESS!')
        return nameEN
    except Exception as e:
        print(sql)
        print(e)

def getnameCN(gameid):
    global cur
    sql = 'SELECT nameCN FROM '+schema_name+'.'+table_name_cn+' WHERE gameid = '+str(gameid)
        #print sql
    try:
        cur.execute(sql)
        records = cur.fetchall()
        #print records
        data = list(records[0])
        #print data
        nameCN = data[0]
        #print('CN SQL EXECUTION SUCCESS!')
        return nameCN
    except Exception as e:
        print(e)

def multi_get_letter(str_input):
    unicode_str = str_input
    return_list = []
    for one_unicode in unicode_str:
        #print one_unicode
        return_list.append(str(single_get_first(one_unicode)))
    return "".join(return_list)

def single_get_first(unicode_str):
    str1 = unicode_str.encode('GBK')
    #print(str1)
    try:
        ord(str1)
        #print str1
        return str1
    except:
        #print(ord(str1[0]))
        #print(ord(str1[1]))
        #print(ord('a'))
        asc = str1[0] * 256 + str1[1] - 65536
        #print asc
        if asc >= -20319 and asc <= -20284:
          return 'A'
        if asc >= -20283 and asc <= -19776:
          return 'B'
        if asc >= -19775 and asc <= -19219:
          return 'C'
        if asc >= -6471 and asc <= -5919:
          return 'C'
        if asc >= -19218 and asc <= -18711:
          return 'D'
        if asc >= -18710 and asc <= -18527:
          return 'E'
        if asc >= -18526 and asc <= -18240:
          return 'F'
        if asc >= -18239 and asc <= -17923:
          return 'G'
        if asc >= -17922 and asc <= -17418:
          return 'H'
        if asc >= -17417 and asc <= -16475:
          return 'J'
        if asc >= -16474 and asc <= -16213:
          return 'K'
        if asc >= -8239 and asc <= -8239:
          return 'K'
        if asc >= -16212 and asc <= -15641:
          return 'L'
        if asc >= -15640 and asc <= -15166:
          return 'M'
        if asc >= -15165 and asc <= -14923:
          return 'N'
        if asc >= -14922 and asc <= -14915:
          return 'O'
        if asc >= -14914 and asc <= -14631:
          return 'P'
        if asc >= -14630 and asc <= -14150:
          return 'Q'
        if asc >= -14149 and asc <= -14091:
          return 'R'
        if asc >= -14090 and asc <= -13315:
          return 'S'
        if asc >= -13314 and asc <= -12839:
          return 'T'
        if asc >= -12838 and asc <= -12557:
          return 'W'
        if asc >= -12556 and asc <= -11848:
          return 'X'
        if asc >= -11847 and asc <= -11056:
          return 'Y'
        if asc >= -11055 and asc <= -10247:
          return 'Z'
    return ''

#a = multi_get_letter(u'欢迎你')
#print a

def index_gen():
    global cur
    try:
        #gameid = int(argv[1])
        userPlatform=platform.system()
        if(userPlatform=='Linux'):
            con = getdb('Linux_local')
        elif(userPlatform=='Windows'):
            con = getdb('Windows_local')
        cur = con.cursor()
    except:
        print('usage: python index_gen.py local/remote/linux')
        sys.exit(0)

    index_dict = dict()
    index_dict['A0']=['A']
    index_dict['B0']=['B']
    index_dict['C0']=['C']
    index_dict['D0']=['D']
    index_dict['E0']=['E']
    index_dict['F0']=['F']
    index_dict['G0']=['G']
    index_dict['H0']=['H']
    index_dict['I0']=['I']
    index_dict['J0']=['J']
    index_dict['K0']=['K']
    index_dict['L0']=['L']
    index_dict['M0']=['M']
    index_dict['N0']=['N']
    index_dict['O0']=['O']
    index_dict['P0']=['P']
    index_dict['Q0']=['Q']
    index_dict['R0']=['R']
    index_dict['S0']=['S']
    index_dict['T0']=['T']
    index_dict['U0']=['U']
    index_dict['V0']=['V']
    index_dict['W0']=['W']
    index_dict['X0']=['X']
    index_dict['Y0']=['Y']
    index_dict['Z0']=['Z']

    for gameid in nameCN_dict.keys():
        #print gameid
        nameCN = getnameCN(gameid)
        #print nameCN
        nameEN = getnameEN(gameid)
        #print nameEN
        capital_key = multi_get_letter(nameCN)
        index_dict[capital_key]=[gameid,nameEN,nameCN,capital_key]
        #print index_dict[capital_key]

        imgfolder = boardgame_home + slash + image + slash + str(gameid)
        imgfolder_1 = boardgame_home + slash + image + slash + str(gameid) + slash + 'setup'
        imgfolder_2 = boardgame_home + slash + image + slash + str(gameid) + slash + 'flow'
        imgfolder_3 = boardgame_home + slash + image + slash + str(gameid) + slash + 'end'
        imgfolder_4 = boardgame_home + slash + image + slash + str(gameid) + slash + 'stuff'
        if not os.path.exists(imgfolder):
            os.mkdir(imgfolder)
        if not os.path.exists(imgfolder_1):
            os.mkdir(imgfolder_1)
        if not os.path.exists(imgfolder_2):
            os.mkdir(imgfolder_2)
        if not os.path.exists(imgfolder_3):
            os.mkdir(imgfolder_3)
        if not os.path.exists(imgfolder_4):
            os.mkdir(imgfolder_4)

    #print index_dict
    #default open file only accept ascii
    f = codecs.open(js_index_path,'w','utf-8')
    f.write("var index_letters = [];\n")
    f.write("var index_games = [];\n")
    for i, letter in enumerate([chr(x) for x in range(65,91)]):
        #print letter
        f.write('index_letters['+str(i)+']=\''+letter+'\';\n')

    for i, key in enumerate(sorted(index_dict.keys())):
        gameinfo = index_dict[key]
        #print(gameinfo)
        if len(gameinfo) == 1:
            f.write(('index_games['+str(i)+']=[\''+gameinfo[0]+'\',\''+gameinfo[0]+'\'];\n'))
        elif len(gameinfo) == 4:
            f.write(('index_games['+str(i)+']=['+str(gameinfo[0])+',\''+gameinfo[1].replace('\'','\\\'')+'\',\''+gameinfo[2]+'\',\''+gameinfo[3]+'\'];\n'))
    f.close()
    print("SUCCESS!")


