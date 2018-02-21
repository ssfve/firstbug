from sys import argv
from gamelist import create_gamelist
from palette import create_colorlist
from api_one import bgg_xml_reader
from translate_one import bgg_xml_translater
from style_one import bgg_xml_styler
from index_gen import *

nameCN_dict = create_gamelist()
color_dict = create_colorlist()
games_dict = dict()
schema_name = 'boardgames'
table_name = 'control_table'

try:
    mode = argv[1]
except:
    print("usage: python getData.py mode [gameid]")
    print("mode could be all one paint")

try:
    gameid = int(argv[2])
    games_dict[gameid] = nameCN_dict[gameid]
except:
    print("usage: python getData.py mode [gameid]")
    print("please specify mode")
    games_dict = nameCN_dict




if __name__ == '__main__':
    if mode == 'all':
        print('starting...')
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        bgg_xml_styler(games_dict)
        index_gen()
    if mode == 'one':
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        bgg_xml_styler(games_dict)
    if mode == 'paint':
        bgg_xml_styler(games_dict)

