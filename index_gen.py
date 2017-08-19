#coding:utf-8

from sys import argv
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import codecs

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

try:
    #gameid = int(argv[1])
    environment = argv[1]
except:
    print 'usage: python index_gen.py local/remote/linux'
    sys.exit(0)

if environment == 'local':
    con = mysql.connector.connect(host='localhost',port=3306,user='root',password='b0@rdg@merule5')
elif environment == 'remote':
    con = mysql.connector.connect(host='180.76.244.130',port=3306,user='mysql',password='MyNewPass4!')
elif environment == 'linux':
    con = mysql.connector.connect(host='localhost',port=3306,user='mysql',password='MyNewPass4!')

cur = con.cursor()

def getnameEN(gameid):
    sql = 'SELECT name FROM '+schema_name+'.'+table_name_en+' WHERE gameid = '+str(gameid)
        #print sql
    try:
        cur.execute(sql)
        records = cur.fetchall()
        data = list(records[0])
        nameEN = data[0]
        #print('EN SQL EXECUTION SUCCESS!')
        return nameEN
    except Exception,e:
        print('error when executing sql')
        print(sql)
        #print boardgamepublisher.encode('GBK', 'ignore')
        print(e)

def getnameCN(gameid):
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
    except Exception,e:
        print('\n')
        print('error when executing sql')
        #print(nameCN)
        print(e)
        print('\n')

def multi_get_letter(str_input):
    if isinstance(str_input, unicode):
        unicode_str = str_input
    else:
        try:
            unicode_str = str_input.decode('utf8')
        except:
            try:
                unicode_str = str_input.decode('gbk')
            except:
                print str_input
                print 'unknown coding'
                return
    return_list = []
    for one_unicode in unicode_str:
        return_list.append(single_get_first(one_unicode))
    return "".join(return_list)

def single_get_first(unicode_str):
    str1 = unicode_str.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        #print ord(str1[0])
        #print ord(str1[1])
        #print ord('a')
        asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
        if asc >= -20319 and asc <= -20284:
          return 'A'
        if asc >= -20283 and asc <= -19776:
          return 'B'
        if asc >= -19775 and asc <= -19219:
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
        if asc >= -14090 and asc <= -13119:
          return 'S'
        if asc >= -13118 and asc <= -12839:
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

jsFolder = 'js'
indexFolder = 'index'
pageFolder = 'page'
variablesFolder = 'variables'
slash = '/'
index_dict = dict()
index_dict['A']=['A']
index_dict['B']=['B']
index_dict['C']=['C']
index_dict['D']=['D']
index_dict['E']=['E']
index_dict['F']=['F']
index_dict['G']=['G']
index_dict['H']=['H']
index_dict['I']=['I']
index_dict['J']=['J']
index_dict['K']=['K']
index_dict['L']=['L']
index_dict['M']=['M']
index_dict['N']=['N']
index_dict['O']=['O']
index_dict['P']=['P']
index_dict['Q']=['Q']
index_dict['R']=['R']
index_dict['S']=['S']
index_dict['T']=['T']
index_dict['U']=['U']
index_dict['V']=['V']
index_dict['W']=['W']
index_dict['X']=['X']
index_dict['Y']=['Y']
index_dict['Z']=['Z']

for gameid in nameCN_dict.keys():
    #print gameid
    nameCN = getnameCN(gameid)
    #print nameCN
    nameEN = getnameEN(gameid)
    #print nameEN
    capital_key = multi_get_letter(nameCN)
    index_dict[capital_key]=[gameid,nameEN,nameCN,capital_key]
    print index_dict[capital_key]


#print index_dict



boardgame_home = os.getenv('BG_HOME')
pageGenerator_home = os.getenv('PG_HOME')

index_variables_filename = 'index.variables.js'

#js_page_folder = boardgame_home + slash + jsFolder + slash + pageFolder + slash
js_page_folder = boardgame_home + slash + indexFolder + slash + variablesFolder + slash
js_index_path = js_page_folder + index_variables_filename

#default open file only accept ascii
f = codecs.open(js_index_path,'w','utf-8')
f.write("var index_letters = [];\n")
f.write("var index_games = [];\n")
for i, letter in enumerate([chr(x) for x in range(65,91)]):
    f.write('index_letters['+str(i)+']=\''+letter+'\';\n')

for i, key in enumerate(sorted(index_dict.keys())):
    gameinfo = index_dict[key]
    if len(gameinfo) == 1:
        f.write(('index_games['+str(i)+']=[\''+gameinfo[0]+'\',\''+gameinfo[0]+'\'];\n'))
    elif len(gameinfo) == 4:
        f.write(('index_games['+str(i)+']=['+str(gameinfo[0])+',\''+gameinfo[1]+'\',\''+gameinfo[2]+'\',\''+gameinfo[3]+'\'];\n'))
f.close()

print "SUCCESS!"


