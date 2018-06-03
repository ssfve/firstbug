# -*- coding:utf-8 -*-

import os
import io
import requests
import random
from sys import argv

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import mysql.connector
from gamelist import create_gamelist
import platform
from api_one import *
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
table_name = 'bggdata'
table_name_cn = 'bggdatacn'

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

if __name__ == '__main__':
    a=dict()
    b="{\"key\":\"value\"}"
    a=eval(b)
    print(a["key"])