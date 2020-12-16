import re


def get_team_id_from_link(link: str, pattern: str):
    player_id = re.sub(link, '', pattern)
    return player_id