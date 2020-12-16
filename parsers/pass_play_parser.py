import re


def get_pass_yards(play_details_list: list) -> int:
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


def pass_complete(play_details_list: list):
    receiver_idx = 2
    play_details_pipe = '|'.join(play_details_list)
    if play_details_pipe.find(' complete ') != -1:
        return True, play_details_list[receiver_idx], get_pass_yards(play_details_list)
    return False, None, None


