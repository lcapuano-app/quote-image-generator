import os
from typing import Tuple


# Main dir
MAIN_DIR = os.path.dirname( os.path.abspath( __file__ ) )

# Project root
ROOT_DIR = os.path.dirname( MAIN_DIR )

WORKSPACE_DIR = os.path.dirname(ROOT_DIR)

ASSETS_DIR = os.path.join(WORKSPACE_DIR, 'assets')
FALLBACK_DIR = os.path.join(WORKSPACE_DIR, 'fallback')
LOGS_DIR = os.path.join(WORKSPACE_DIR, 'logs')
TEMP_DIR = os.path.join(WORKSPACE_DIR, 'temp')

# Server
HOST = 'localhost'
PORT = 4040

## IMAGE 
IM_MODE: int = 'RGBA'
IM_HEIGHT: int = 600
IM_WIDTH: int = 800

## IMAGE COLOR
COLOR_DARK: str        = 'rgba(51,51,51,255)'
COLOR_GOLD: str        = 'rgb(209,201,5)'
COLOR_LIGTH: str       = 'rgb(204,204,204)'
COLOR_AUTHOR: str      = COLOR_GOLD
COLOR_BG: str          = COLOR_DARK
COLOR_DECOR: str       = COLOR_GOLD
COLOR_QUOTE: str       = COLOR_LIGTH
COLOR_STROKE: str      = COLOR_GOLD
COLOR_TRANSPARENT: str = 'rgba(0,0,0,0)'

## IM REQUEST
IM_REQ_AUTHOR_NAME: str      = "Chaves"
IM_REQ_AUTHOR_IMG_NAME: str  = "chaves.png"
IM_REQ_QUOTE_ID: str         = "63139372217ba7e20813b92e"
IM_REQ_QUOTE_TEXT: str       = "Volta o cão arrependido, com suas orelhas tão fartas, com seu osso roído e com o rabo entre as patas."
IM_REQ_SIZE: Tuple[int, int] = (IM_WIDTH, IM_HEIGHT)
IM_MARGIN_RATIO: float       = 0.04

## AUTHOR
AUTHOR_IMG_ALPHA: int            = 100
AUTHOR_RESIZE_LIMIT_RATIO: float = 1.2
AUTHOR_ROTATE_ANGLE: float       = -10
AUTHOR_FILENAME: str             = 'default_author.png'
FONT_AUTHOR_SCALE_FACTOR: float  = 0.0325

## QUOTE
FONT_QUOTE_SCALE_FACTOR: float = 0.0275
QUOTE_STROKE_SIZE: int = 1
TEXT_MULTI_WRAP: int = 50


## EXT API
EXT_API_BASE_URL = 'https://lcapuano.app/valorant/bot'
EXT_API_ASSETS_URL = f'{EXT_API_BASE_URL}/assets/'
EXT_API_SAVE_QUOTE_URL = f'{EXT_API_BASE_URL}/save-quote.php'
EXT_API_OUTPUT_URL = f'{EXT_API_BASE_URL}/output'

###### ARRUMAR #####

DECOR_LINE_H_FACTOR: float = 0.0033
DECOR_SIZE_MARGIN_FACTOR: int = 3
DECOR_WALKER_FEET_PADDING_RATIO: float =  0.05 # walker feet is usually about it 

FONT_FACE: str = 'CursiveSerif-pj5Z.ttf'
FONT_SIZE_FACTOR: float = 0.025
FONT_SIZE: int = 18



