# Define some colors
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (206, 251, 255)
GREY = (200, 210, 227)

BLUE_LIGHT = (0, 128, 255)
GREY_LIGHT = (61, 62, 64)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 70
HEIGHT = 70

MYSTERY_BOX_WIDTH = 35
MYSTERY_BOX_HEIGHT = 35

# This sets the margin between each cell
MARGIN = 1
MARGIN_TRIANGLE = MARGIN * 2
WIDTH_TRIANGLE = (WIDTH / 60) * 16
MENU_HEIGHT = WIDTH * (10 / 6)

# FONTS
# capelito_FONT_SIZE = int((WIDTH/60)*8)
DEFINITION_FONT_SIZE = 10
MYSTERY_FONT_SIZE = 15
PANEL_MYSTERY_WORD_HEIGHT = DEFINITION_FONT_SIZE * 13
MENU_FONT_SIZE = 14
LETTER_FONT_SIZE = 18

# MAIN_FONT = 'arial'
MAIN_FONT_PATH = "back/resources/fonts/trebuchet-ms-grassetto.ttf"
ITALIC_FONT_PATH = "back/resources/fonts/Trebuchet-MS-Italic.ttf"


class TEXT_EDITING:
    WORD_DEFINITION = "WORD_DEFINITION"
    MYSTERY_DEFINITION = "MYSTERY_DEFINITION"
