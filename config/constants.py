
class Constants():


  IMG_EXT = '.png'
  SRC_DIR = 'assets/'

  API_HOST = 'lcapuano.app'
  API_BASE_URL = 'https://lcapuano.app/valorant/bot/'
  API_OUTPUT_DIR = 'https://lcapuano.app/valorant/bot/output/'
  API_OUTPU_DFLT_IMG = 'https://lcapuano.app/valorant/bot/output/default.png'
  API_UPLOAD_URL = '/valorant/bot/save-quote.php'
  #API_UPLOAD_URL = API_BASE_URL + 'save-quote.php'
  ASSETS_BASE_URL = API_BASE_URL + 'assets/'

  AUTHOR_IMG_ALPHA = 100
  AUTHOR_RESIZE_LIMIT_RATIO = 1.2
  AUTHOR_ROTATE_ANGLE = -10
  AUTHOR_IMG_FALLBACK = SRC_DIR + 'default' + IMG_EXT


  FONT_FACE = 'CursiveSerif-pj5Z.ttf'
  FONT_SIZE_FACTOR = 0.025

  IMG_SIZE = ( 800, 600 )

  MARGIN_RATIO = 0.04

  QUOTE_TXT_RGB = 'rgb(204,204,204)'
  QUOTE_TXT_STROKE = 'rgb(166,160,0)'

  TEXT_COLOR_RGB = 'rgb(209,201,5)'
  TEXT_MULTI_WRAP = 50

  WALKER_ASSET_NAME = 'walker.png'
  WALKER_ASSET_PATH = SRC_DIR + WALKER_ASSET_NAME
  WALKER_FEET_RATIO = 0.05 # walker feet is allways about it

