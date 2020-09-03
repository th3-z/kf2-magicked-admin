"""
# The in-game chat uses the font 'TeX Gyre Adventor regular', the following
# code generates the character widths seen below.

import fontforge
import string

chars = [char for char in string.printable] 
chars.remove("\n")
chars.remove("\r")
chars.remove("\x0b")
chars.remove("\x0c")

f = fontforge.open("texgyreadventor-regular.otf")

print("c_width = {")
for glyph in f.glyphs():
    try:
        if chr(glyph.unicode) in chars:
            c, w = chr(glyph.unicode), str(glyph.width)
            print("    '{}': {},".format(c,w))
    except:
        continue
print("}")
"""

avg_width = 544.79

c_width = {
    'A': 740,
    'a': 683,
    '&': 757,
    '^': 606,
    '~': 606,
    '*': 425,
    '@': 867,
    'B': 574,
    'b': 682,
    '\\': 605,
    '|': 672,
    '{': 351,
    '}': 351,
    '[': 351,
    ']': 351,
    'C': 813,
    'c': 647,
    ':': 277,
    ',': 277,
    'D': 744,
    'd': 685,
    '$': 554,
    'E': 536,
    'e': 650,
    '8': 554,
    '=': 606,
    '!': 295,
    'F': 485,
    'f': 314,
    '5': 554,
    '4': 554,
    'G': 872,
    'g': 673,
    '`': 375,
    '>': 606,
    'H': 683,
    'h': 610,
    '-': 332,
    'I': 226,
    'i': 200,
    'J': 482,
    'j': 203,
    'K': 591,
    'k': 502,
    'L': 462,
    'l': 200,
    '<': 606,
    'M': 919,
    'm': 938,
    'N': 740,
    'n': 610,
    '9': 554,
    '#': 554,
    'O': 869,
    'o': 655,
    '1': 554,
    'P': 592,
    'p': 682,
    '(': 369,
    ')': 369,
    '%': 775,
    '.': 277,
    '+': 606,
    'Q': 871,
    'q': 682,
    '?': 591,
    '"': 309,
    '\'': 198,
    'R': 607,
    'r': 301,
    'S': 498,
    's': 388,
    ';': 277,
    '7': 554,
    '6': 554,
    '/': 437,
    ' ': 277,
    'T': 426,
    't': 339,
    '3': 554,
    '2': 554,
    'U': 655,
    'u': 608,
    '_': 500,
    'V': 702,
    'v': 554,
    'W': 960,
    'w': 831,
    'X': 609,
    'x': 480,
    'Y': 592,
    'y': 536,
    'Z': 480,
    'z': 425,
    '0': 554,
}
