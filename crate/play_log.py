import numpy as np
import re
from config.play_config import PlayParse, PlayConfig
from parsers.pass_play_parser import pass_complete


class PlayLog:
    '''
        Quarter|Time|Down|ToGo|Location|Detail|DAL|WAS|EPB|EPA
        Need to pass in piped string from BeautifulSoup [comments.('tr').stripped_strings]
    '''
    def __init__(self):
        self._parsed            = False
        self._play_type         = None
        self._pipe_string       = None
        self._left_pad_size     = 5
        self._right_pad_size    = 4
        self._info_dict         = self._play_info_init()

        self._defense_play_words    = PlayParse.defense_play_words
        self._odd_words             = PlayParse.odd_words
        self._pass_flag_words       = PlayParse.pass_flag_words
        self._run_flag_words        = PlayParse.run_flag_words
        self._skip_words            = PlayParse.skip_words
        self._special_team_words    = PlayParse.special_team_words

    def parse_log(self, pipe_string: str):
        self._info_dict = self._play_info_init()
        self._pipe_string = pipe_string
        pipe_string_split = pipe_string.split('|')
        if len(pipe_string_split) < self._left_pad_size + self._right_pad_size:
            self._info_dict['delete'] = 1
            return

        left_pad = pipe_string_split[:self._left_pad_size]
        right_pad = pipe_string_split[-self._right_pad_size:]
        left_pad_dict, right_pad_dict = self._get_pad_dicts(left_pad, right_pad)
        play_details_list = pipe_string_split[self._left_pad_size:-self._right_pad_size]
        play_details_str = ' '.join(play_details_list)
        play_details_str_clean = re.sub('\s+', ' ', play_details_str)
        play_type_one_hot = self._check_play_type(play_details_str=play_details_str)
        play_type = PlayConfig.play_types[np.argmax(play_type_one_hot)]
        self._info_dict.update(left_pad_dict)
        self._info_dict.update(right_pad_dict)
        self._info_dict.update({'type': play_type})
        self._info_dict.update({'play_details': play_details_str_clean})

        if play_type == 'pass' or play_type == 'run':
            self._info_dict.update({play_type: play_details_list[0]})
        if play_type == 'pass':
            pass_completed, receive, yards = pass_complete(play_details_list)
            self._info_dict.update({'receive': receive, 'yards': yards})
        return self._info_dict

    def _get_pad_dicts(self, left_pad, right_pad):
        left_pad_dict = {PlayConfig.left_pad_keys[i]: left_pad[i] for i in range(len(PlayConfig.left_pad_keys))}
        right_pad_dict = {PlayConfig.right_pad_keys[i]: right_pad[i] for i in range(len(PlayConfig.right_pad_keys))}
        return left_pad_dict, right_pad_dict

    def _play_info_init(self) -> dict:
        info_dict = {key: None for key in PlayConfig.info_dict_keys}
        return info_dict

    def _check_play_type(self, play_details_str):
        defense_play_str        = '|'.join(self._defense_play_words)
        odd_play_str            = '|'.join(self._odd_words)
        pass_play_str           = '|'.join(self._pass_flag_words)
        run_play_str            = '|'.join(self._run_flag_words)
        skip_play_str           = '|'.join(self._skip_words)
        special_teams_play_str  = '|'.join(self._special_team_words)
        defense_match           = min(1, len(re.findall(defense_play_str, play_details_str)))
        odd_match               = min(1, len(re.findall(odd_play_str, play_details_str)))
        pass_match              = min(1, len(re.findall(pass_play_str, play_details_str)))
        run_match               = min(1, len(re.findall(run_play_str, play_details_str)))
        skip_match              = min(1, len(re.findall(skip_play_str, play_details_str)))
        special_teams_match     = min(1, len(re.findall(special_teams_play_str, play_details_str)))
        return defense_match, odd_match, pass_match, run_match, skip_match, special_teams_match
