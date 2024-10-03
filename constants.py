import pygame
pygame.init()
from pygame.locals import *

from engine import *

REWARDS = {
    'xp' : pygame.image.load('sprites/icons/xp_ico.png').convert_alpha(),
    'money' : pygame.image.load('sprites/icons/money_ico.png').convert_alpha(),
}

CLOTHES = {

    '2/1' : "plain orange shirt",
    '3/1' : "simple brown pants",
    '3/2' : "simple bluesky pants",

}

CLOTHES_RARES = {
    'plain orange shirt' : 'обычный',
    'simple brown pants' : 'обычный',
    'simple bluesky pants' : 'обычный',
}

ITEM_PROPERTIES = {
    'мед' : {
        'голод' : 18,
        'здоровье' : 10
    }
}

ITEMS = {
    'камень' : {
        'use' : False,
        "name" : 'камень',
        "location" : 'лес',
        "buy" : 0,
        "sell" : 0,
        "rare" : "легендарный",
        'path' : 'rock',
        'describe' : 'обычный камень, таких полно в лесу'
    },
    'книга' : {
        'use' : False,
        "name" : "книга",
        "location" : 'библиотека',
        "buy" : 120,
        "sell" : 50,
        "rare" : "обычный",
        "path" : 'book',
        'describe' : 'Том попросил меня передать эту книгу Джеку'
    },
    'мед' : {
        'use' : True,
        "name" : "мед",
        "location" : 'библиотека',
        "buy" : 120,
        "sell" : 80,
        "rare" : "редкий",
        "path" : 'honey',
        "describe" : 'Достать такой товар достаточно нелегко'
    }
}