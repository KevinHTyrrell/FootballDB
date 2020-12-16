import json
import os
from config.file_config import FileConfig
from config.parse_config import ParseConfig
from config.site_config import SiteConfig
from grabbers.raw_content import retrieve_raw_site_contents
from parsers.team_parser import get_team_id_from_link


def get_team_link_info(overwrite: bool = False):
    team_link_list = list()
    team_url = SiteConfig.team_url
    raw_data = retrieve_raw_site_contents(team_url)
    tmp = raw_data.find_all('a', href=True)
    for item in tmp:
        if item.__str__().find(ParseConfig.team_link_flag) != -1 and item.string.find(' ') != -1:
            if item.__str__().find('2020') != -1:
                continue
            to_replace = '|'.join([ParseConfig.team_link_flag, '/', ParseConfig.player_url_ext])
            team_name = item.string
            team_link_ext = item.get('href')
            team_abbrev = get_team_id_from_link(to_replace, team_link_ext)
            team_link_list.append({
                'team_name'       : team_name.strip().lower(),
                'team_link_ext'   : team_link_ext,
                'team_id'         : team_abbrev
            })
    filepath_out = os.path.join(FileConfig.team_metadata_dir, FileConfig.team_id_file)
    team_info_out = json.dumps(team_link_list)
    if not os.path.exists(filepath_out) or overwrite:
        with open(filepath_out, 'w') as f:
            f.write(team_info_out)