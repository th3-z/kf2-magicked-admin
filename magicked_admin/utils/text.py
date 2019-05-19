import math

CHAT_LINE_HEIGHT = 8

def millify(n):
    if not n: return '0'

    millnames = ['', 'K', 'M', 'B', 'T']
        
    n = float(n)
    millidx = max(0,
                  min(len(millnames)-1,
                      int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def trim_string(input_str, length):
    return (input_str[:length-2] + '..') if len(input_str) > length \
        else input_str


def str_to_bool(s):
    if s in ['True', 'true', '1']:
        return True
    elif s in ['False', 'false', '0']:
        return False
    else:
        raise ValueError


def pad_output(message):
    if not message:
        return None

    message_height = len(message.split('\n'))
    padding_lines = CHAT_LINE_HEIGHT - message_height

    if padding_lines > 0:
        return '\n'*padding_lines + message
    else:
        return message
