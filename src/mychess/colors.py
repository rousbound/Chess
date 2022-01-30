"""
Module made only to convert and save colors
"""

def hex2rgb(hex_string):
    '''Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).'''
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

square_bright = hex2rgb("#f0d9b5")
square_dark = hex2rgb("#b58863")
last_move_square_dark = hex2rgb("#aba23b")
last_move_square_bright = hex2rgb("#cdd26b")
capturing_square_bright = hex2rgb("#829769")
capturing_square_dark = hex2rgb("#84794e")
circle_color = hex2rgb("#718a53")
background_promotion = (125,125,125,0)
red = (255,125,125,0)
