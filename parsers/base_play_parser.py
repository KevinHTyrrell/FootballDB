from abc import ABC
import numpy as np
import pandas as pd
import re
from config.play_config import PlayConfig


class BasePlayParser(ABC):
    def get_subject(self, play_details_list: list):
        return play_details_list[0]

    def get_yards(self, play_details_list: list) -> int:
        play_details_pipe = '|'.join(play_details_list)
        play_details_pipe_all = re.sub('\(|\)', '|', play_details_pipe)
        play_details_list_all = play_details_pipe_all.split('|')
        yard_str = None
        for play_str in play_details_list_all:
            if play_str.find('yard') != -1:
                yard_str = play_str
                break
        if yard_str is None:
            return 0
        yard_str_split = re.split('\s+', yard_str)
        for word in yard_str_split:
            if word.isnumeric():
                return int(word)
        return 0
