from data.modules.delta_time import DeltaTime
#! Will be changed later. Loading from settings file

RESOLUTION = (1280,720)

WIDTH = RESOLUTION[0]
HEIGHT = RESOLUTION[1]

HALF_WIDTH = WIDTH >> 1
HALF_HEIGHT = HEIGHT >> 1

QUARTER_WIDTH = WIDTH >> 2
QUARTER_HEIGHT = HEIGHT >> 2

FPS = 60
TITLE = "Pygame Engine"
ICON_PATH = None

GLOBAL_DELTA_TIME = DeltaTime()

TEXT_COLOR = '#a6a6a6'
DEFAULT_BACKGROUND_COLOR = '#242424'
MEDIUM_BACKGROUND_COLOR = '#484848'

HIGHLIGHT_TEXT_COLOR = '#d2d2d2'
PRESSED_TEXT_COLOR = '#ffffff'

IMAGE_PATH = 'data\\bin\\img\\'
