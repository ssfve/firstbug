from gamelist import create_gamelist
from palette import create_colorlist
from api_one import bgg_xml_reader
from translate_one import bgg_xml_translater
from style_one import bgg_xml_styler
from index_gen import write_js

nameCN_dict = create_gamelist()
color_dict = create_colorlist()
games_dict = dict()
schema_name = 'boardgames'
table_name = 'control_table'

global mode
try:
    #print("using default mode \"all\"?(y/n)")
    print("mode could be all one paint")
    default_enabled = input("using default mode \"all\"?(y/n): ")
    if(default_enabled == 'y'):
        mode = 'all'
    else:
        mode = 'all'
except:
    print("usage: python getData.py mode [gameid]")

global gameid

try:
    gameid = input("please input BGG game id: ")
    #print(gameid)
    #print(int(gameid))
    games_dict[gameid] = nameCN_dict[int(gameid)]
except:
    print("usage: python getData.py mode [gameid]")
    print("please specify mode")
    games_dict = nameCN_dict

if __name__ == '__main__':
    if mode == 'all':
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        write_js()
        bgg_xml_styler(games_dict)
        print("http://www.boardgamerules.cn/index/gameCover.html?id={0}".format(gameid))
    if mode == 'one':
        bgg_xml_reader(games_dict)
        bgg_xml_translater(games_dict)
        bgg_xml_styler(games_dict)
    if mode == 'paint':
        bgg_xml_styler(games_dict)

