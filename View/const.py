# Window hyperparameters
import os.path

game_caption = "Challenge 2019"
screen_size  = (1280, 800)
game_size    = (800, 800)

frame_per_sec = 60

# Table of colors
# Using these monotone colors is discouraged
COLOR_WHITE          = (255, 255, 255)
COLOR_BLACK          = (  0,   0,   0)
COLOR_BLUE           = (  0,   0, 255)
COLOR_GREEN          = (  0, 255,   0)
COLOR_RED            = (255,   0,   0)
COLOR_GRAY           = (128, 128, 128)


# These cooler colors are preferred
COLOR_TURQUOISE      = ( 64, 224, 208)
COLOR_LIGHTCORAL     = (240, 128, 128)
COLOR_ORANGERED      = (255,  69,   0)
COLOR_DARKKHAKI      = (189, 183, 107)
COLOR_GOLD           = (255, 215,   0)
COLOR_VIOLET         = (238, 130, 238)
COLOR_DARKVIOLET     = (148,   0, 211)
COLOR_LIMEGREEN      = ( 50, 205,  50)
COLOR_OLIVE          = (128, 128,   0)
COLOR_ROYALBLUE      = ( 65, 105, 225)
COLOR_BURLYWOOD      = (222, 184, 135)
COLOR_SILVER         = (192, 192, 192)
COLOR_GAINSBORO      = (220, 220, 220)
COLOR_SNOW           = (255, 250, 250)
COLOR_LIGHTGRAY      = (211, 211, 211)
COLOR_FIREBRICK      = (178,  34,  34)
COLOR_SADDLEBROWN    = (139,  69,  19)
COLOR_DARKOLIVEGREEN = ( 85, 107,  47)
COLOR_DARKRED        = (139,   0,   0)

# Predefined Colors
bgColor           =  COLOR_GAINSBORO
sbColor           =  COLOR_BLACK # scoreboard
aliveTeamColor    =  COLOR_BLACK
deadTeamColor     =  COLOR_RED
teamLengthColor   =  COLOR_SNOW
wbColor           =  COLOR_SNOW
gravColor         =  COLOR_LIGHTGRAY
explosive_color   =  COLOR_FIREBRICK
multibullet_color =  COLOR_LIMEGREEN
bigbullet_color   =  COLOR_BURLYWOOD
playerColor       = [COLOR_DARKVIOLET,     COLOR_ROYALBLUE, COLOR_SADDLEBROWN,
                     COLOR_DARKOLIVEGREEN, COLOR_GOLD,      COLOR_VIOLET,
                     COLOR_TURQUOISE,      COLOR_LIMEGREEN, COLOR_DARKKHAKI,
                     COLOR_LIGHTCORAL,     COLOR_BURLYWOOD, COLOR_SILVER]

# Durations
magicCircleGenerationTime = 120
timeLimitExceedStampTime  = 30
scoreFlagEmergeTime       = 60
thermometerEmergeTime     = 120
explosionTime             = 30
killedExplosionRadius     = 200
killedExplosionTime       = 90
bulletFlickerCycle        = 15
whiteBallGenerationTime   = 30
itemGenerationTime        = 60

# skill card phrases
# phrase1 : two thin  lines run right
# phrase2 : two thick lines run left
# phrase3 : silouette runs left
# phrase4 : flash
# phrase5 : silouette becomes picture, and big picture appears
# phrase6 : silouette and big picture accelerates and disappears

# Size
player_height = 100
player_width = 100

# Font

board_name_font = os.path.join('Font', 'Noto', 'NotoSansCJK-Black.ttc')
board_num_font = os.path.join('Font', 'Noto', 'NotoSansCJK-Black.ttc')

# Path
IMAGE_PATH = os.path.join('View', 'image')
