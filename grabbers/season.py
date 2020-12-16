import json
import os
import re
import time
from config.file_config import FileConfig
from config.parse_config import ParseConfig
from config.site_config import SiteConfig
from grabbers.raw_content import retrieve_raw_site_contents
from parsers.game_parser import parse_game_metadata


def fetch_all_season_games(season: int, week: int):
    all_games_metadata = list()
    site_url = SiteConfig.base_season_url.format(season=season, week=week)
    raw_site_contents = retrieve_raw_site_contents(site=site_url)
    games_raw = raw_site_contents.findAll('table', attrs={'class': 'teams'})
    for game in games_raw:
        game_json = dict()
        game_json['season'] = season
        game_json['week'] = week
        game_json.update(parse_game_metadata(game, season))
        all_games_metadata.append(game_json)
    data_out = json.dumps(all_games_metadata)
    filepath_out = os.path.join(FileConfig.season_metadata_dir, str(season) + '_' + str(week))
    with open(filepath_out, 'w') as f:
        f.write(data_out)


def fetch_game(boxscore_ext: str):
    site_url = ''.join([SiteConfig.base_url, boxscore_ext])
    raw_site_contents = retrieve_raw_site_contents(site=site_url)
    return raw_site_contents


def fetch_raw_games_all(time_delay: float = 0.5):
    all_boxscore_list = list()
    season_metadata_files = os.listdir(FileConfig.season_metadata_dir)
    season_metadata_files.sort()
    for week_file in season_metadata_files:
        with open(os.path.join(FileConfig.season_metadata_dir, week_file)) as f:
            raw_data = f.read()
        game_json_list = json.loads(raw_data)
        for game in game_json_list:
            all_boxscore_list.append(game.get('boxscore'))
    for boxscore_ext in all_boxscore_list:
        to_scrub = '|'.join(['/', ParseConfig.boxscore_flag, ParseConfig.player_url_ext])
        game_id = re.sub(to_scrub, '', boxscore_ext)
        filepath_out = os.path.join(FileConfig.game_raw_dir, game_id)
        print(game_id)
        raw_site_contents = fetch_game(boxscore_ext)
        with open(filepath_out, 'w') as f:
            f.write(raw_site_contents.prettify())
        time.sleep(time_delay)