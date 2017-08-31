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
from gamelist import create_gamelist
from palette import create_colorlist
#from categorylist import *
from api_one import bgg_xml_reader
from translate_one import bgg_xml_translater
from style_one import bgg_xml_styler


nameCN_dict = create_gamelist()
color_dict = create_colorlist()
games_dict = dict()
schema_name = 'boardgames'
table_name = 'control_table'

try:
    mode = argv[1]
except:
    print "usage: python getData.py mode [gameid]"
    print "mode could be all one paint"

try:
    gameid = int(argv[2])
    games_dict[gameid] = nameCN_dict[gameid]
except:
    print "usage: python getData.py mode [gameid]"
    print "please specify mode"
    games_dict = nameCN_dict




if __name__ == '__main__':
    if mode == 'all':
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        bgg_xml_styler(games_dict)
    if mode == 'one':
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        bgg_xml_styler(games_dict)
    if mode == 'paint':
        bgg_xml_styler(games_dict)

