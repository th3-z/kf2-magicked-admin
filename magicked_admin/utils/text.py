import math
from utils.font import c_width, avg_width

motd_width = 196 * 200  # Measured using 'i'
motd_lines = 10

chat_width = 101 * 200
chat_lines = 7


def millify(n):
    if not n:
        return '0'

    millnames = ['', 'K', 'M', 'B', 'T']

    n = float(n)
    millidx = max(0,
                  min(len(millnames) - 1,
                      int(math.floor(
                          0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


def trim_string(input_str, length):
    if not input_str:
        return ""
    return (input_str[:length - 2] + '..') if len(input_str) > length \
        else input_str


def str_to_bool(s):
    if s in ['True', 'true', '1']:
        return True
    elif s in ['False', 'false', '0']:
        return False
    else:
        raise ValueError

def str_width(s):
    width = 0

    for char in s:
        if char in c_width.keys():
            width += c_width[char]
        else:
            width += avg_width
    
    return width

def pad_width(width, text):
    text_w = str_width(text)
    sp_w = str_width(" ")

    if text_w < width:
        text +=" " * int(round((width - text_w) / sp_w))

    return text

def center_str(text):
    text_w = str_width(text)
    remaining = chat_width - text_w
    sp_w = str_width(" ")

    padding = " " * int(round((remaining / sp_w) / 2))

    return padding + text