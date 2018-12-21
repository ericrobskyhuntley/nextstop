import numpy as np
import os

MAX_FEATURES = 800
GOOD_MATCH_PERCENT = 0.05
FRONT_MASK_COLOR_WINDOW = 25
CHECKBOX_SIZE = 23
CHECKBOX_THRESH = 300
Q_COLOR_WINDOW = 15

PROJ_DATA_DIR = '/home/cddl/scans/'
SCAN_DIR = PROJ_DATA_DIR + 'raw/'

SERVER_URL = '/static/cards/exhibit/'
SERVER_DATA_DIR = '/home/ehuntley/scans/'
SERVER_RAW = SERVER_DATA_DIR + 'raw/'
SERVER_PROCESSED = '/home/ehuntley/www/nextstop/static/cards/exhibit/'
SERVER_TEMPLATES = SERVER_DATA_DIR + 'templates/'

# x, y
QUESTION_HUES = [
    # 4: My preferred transport mode(s) in 2020 will be...
    (4, np.array([1, 170, 180])),
    # 5: In 2040, the average person will...
    (5, np.array([176, 130, 83])),
    # Responsibility for autonomous vehicle accidents belongs to...
    (6, np.array([24, 130, 230])),
    # In 2040, commuting will take...
    (7, np.array([62, 100, 159])),
    # In 2040, everyone will have access to...
    (8, np.array([101, 118, 68])),
    # The future of mobility will make the world
    (9, np.array([142, 87, 93])),
    # In the future, my transportation costs will...
    (10, np.array([76, 126, 106])),
    # Future mobility options will have the greatest imapact on...
    (12, np.array([171, 146, 194])),
    # In 2040...
    (13, np.array([107, 100, 130])),
    # Travel in the future will be more dangerous for...
    (14, np.array([6, 196, 232])),
]

OLD_QUESTION_HUES = [
    # 4: My preferred transport mode(s) in 2020 will be...
    (4, np.array([1, 232, 190])),
    # 5: In 2040, the average person will...
    (5, np.array([0, 255, 62])),
    # Responsibility for autonomous vehicle accidents belongs to...
    (6, np.array([27, 176, 242])),
    # In 2040, commuting will take...
    (7, np.array([60, 135, 150])),
    # In 2040, everyone will have access to...
    (8, np.array([107, 255, 42])),
    # The future of mobility will make the world
    (9, np.array([142, 192, 70])),
    # In the future, my transportation costs will...
    (10, np.array([88, 255, 62])),
    # Future mobility options will have the greatest imapact on...
    (12, np.array([174, 156, 208])),
    # In 2040...
    (13, np.array([106, 205, 120])),
    # Travel in the future will be more dangerous for...
    (14, np.array([13, 250, 243])),
]
