from os import system
from src.items import *
system('color')

def colorize(text, color_code):
    return f'\33[{color_code}m{text}\33[0m'

def GRAY(text):
    return colorize(text, 30)
def RED(text):
    return colorize(text, 31)
def GREEN(text):
    return colorize(text, 32)
def YELLOW(text):
    return colorize(text, 33)
def BLUE(text):
    return colorize(text, 34)
def PURPLE(text):
    return colorize(text, 35)
def CYAN(text):
    return colorize(text, 36)

def rarity_to_color(rarity):
    if rarity == rarities.Common:
        return lambda text : text
    elif rarity == rarities.Uncommon:
        return BLUE
    elif rarity == rarities.Rare:
        return YELLOW
    elif rarity == rarities.Super:
        return CYAN
    elif rarity == rarities.Ultra:
        return PURPLE
    
    else:
        return GRAY

def by_rarity(text):
    """Colorizes the text based on its
    rarity in the lookup table above"""
    if text in item_rarity_index.keys():
        return rarity_to_color(item_rarity_index[text])(text)
    else:
        return RED(text)