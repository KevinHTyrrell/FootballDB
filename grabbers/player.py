import json
import os
import pandas as pd
import time
from bs4 import BeautifulSoup
from config.file_config import FileConfig
from config.parse_config import ParseConfig
from config.site_config import SiteConfig
from grabbers.raw_content import retrieve_raw_site_contents
from parsers.player_parser import get_player_id_from_link


def retrieve_raw_player_letter_list(letter: str) -> BeautifulSoup:
    print(letter)
    base_url = SiteConfig.player_letter_url
    site_url = base_url.format(letter=letter)
    site_content = retrieve_raw_site_contents(site_url)
    return site_content


def get_player_link_info(site_contents: BeautifulSoup, letter: str) -> list:
    player_link_list = list()
    link_flag = ParseConfig.player_link_flag.format(letter=letter)
    tags = site_contents.find_all('a')
    for item in tags:
        item_href = item.get('href', '')
        if item_href.find(link_flag) != -1:
            to_replace = '|'.join([link_flag, ParseConfig.player_url_ext])
            item_string = item.string
            player_link_list.append({
                'player_name'       : item_string.strip().lower(),
                'player_link_ext'   : item_href,
                'player_id'         : get_player_id_from_link(to_replace, item_href)
            })
    return player_link_list


def get_all_player_links(delay: int = 5, overwrite: bool = False):
    player_link_info = list()
    letters = [chr(i) for i in range(65, 91)]
    for letter in letters:
        letter_page_info = retrieve_raw_player_letter_list(letter=letter)
        player_link_letter_link = get_player_link_info(letter_page_info, letter)
        player_link_info += player_link_letter_link
        time.sleep(delay)
    filepath_out = os.path.join(FileConfig.player_metadata_dir, FileConfig.player_id_file)
    player_info_out = json.dumps(player_link_info)
    if not os.path.exists(filepath_out) or overwrite:
        with open(filepath_out, 'w') as f:
            f.write(player_info_out)