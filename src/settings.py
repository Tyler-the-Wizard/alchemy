from src.objs import Inventory

def init():
    global CRAFT_PROMPT
    CRAFT_PROMPT = ':: '

    global CURRENT_SAVE
    CURRENT_SAVE = None

    global DATA_DIR
    DATA_DIR = 'data'

    global DEBUG_MODE
    DEBUG_MODE = False

    global INV
    INV = Inventory()

    global PROMPT
    PROMPT = ' > '

    global RECIPES
    RECIPES = []

    global SAVE_DIR
    SAVE_DIR = 'saves'

    global UNSAVED_CHANGES
    UNSAVED_CHANGES = False

    global VERSION
    VERSION = open('version').read()

    global YN_PROMPT
    YN_PROMPT = '(y/n) > '
