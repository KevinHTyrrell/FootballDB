import bs4
import re
from config.parse_config import ParseConfig
from parsers.team_parser import get_team_id_from_link


def get_teams(raw_site_contents: bs4.BeautifulSoup) -> dict:
    flagged_lines = raw_site_contents.find_all('a', attrs=ParseConfig.team_flag_dict)
    assert len(flagged_lines) == 2
    teams = {'away': flagged_lines[0].string, 'home': flagged_lines[1].string}
    return teams


def get_date_from_boxscore_link(boxscore_link: str):
    boxscore_link_split = boxscore_link.split('/')
    boxscore_id = boxscore_link_split[-1]
    boxscore_date = boxscore_id[:8]
    return boxscore_date


def parse_game_metadata(item: bs4.Tag, season: int) -> dict:
    item_str = str(item)
    season_str = str(season)
    item_soup = bs4.BeautifulSoup(item_str, ParseConfig.default_parser)
    item_tr = item_soup.find_all('tr')
    soup = bs4.BeautifulSoup(''.join(item_tr[1:].__str__()), ParseConfig.default_parser)
    all_links = [team['href'] for team in soup.find_all('a')]
    boxscore_idx = [i for i in range(len(all_links)) if all_links[i].find(ParseConfig.boxscore_flag) != -1]
    boxscore_link = all_links.pop(boxscore_idx[0])
    team_link_trim = '|'.join([ParseConfig.team_link_flag, ParseConfig.player_url_ext, '/', season_str])
    away_team = get_team_id_from_link(team_link_trim, all_links.pop(0))
    home_team = get_team_id_from_link(team_link_trim, all_links.pop(0))
    game_date = get_date_from_boxscore_link(boxscore_link)
    game_dict = {'date': game_date, 'away': away_team, 'home': home_team, 'boxscore': boxscore_link}
    return game_dict


def get_play_by_play_parsed(filename: str):
    with open(filename, 'r') as f:
        raw_data = f.read()
    soupy = bs4.BeautifulSoup(raw_data, ParseConfig.default_parser)
    flagged_content_list = list()
    flag_phrase = ParseConfig.play_by_play_flag
    comments = soupy.find_all(string=lambda text: isinstance(text, bs4.Comment))
    for item in comments:
        if item.__str__().find(flag_phrase) != -1:
            flagged_content_list.append(item)
    flagged_content = ''.join(flagged_content_list)
    flagged_soup = bs4.BeautifulSoup(flagged_content, ParseConfig.default_parser)
    flagged_soup_tr = flagged_soup.find_all('tr')
    play_list = list()
    for item in flagged_soup_tr:
        play = item.stripped_strings
        play_string = '|'.join([segment for segment in play])
        play_string = re.sub('\(|\)|,|\.', '|', play_string)
        play_list.append(play_string)
    return play_list


def clean_pipe_string(pipe_string: str) -> str:
    pipe_string_split = pipe_string.split('|')
    pipe_string_split_clean = [segment.replace(':', '').lstrip().rstrip() for segment in pipe_string_split if len(segment) > 0]
    pipe_string_clean = '|'.join(pipe_string_split_clean)
    return pipe_string_clean
