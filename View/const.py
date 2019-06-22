# Window hyperparameters
GameCaption = "Challenge 2019"
ScreenSize  = (1280, 800)
GameSize    = (800, 800)

# Display setting
# To be adjusted
FramePerSec = 60

# Table of colors
# Using these monotone colors is discouraged
Color_White          = (255, 255, 255)
Color_Black          = (  0,   0,   0)
Color_Blue           = (  0,   0, 255)
Color_Green          = (  0, 255,   0)
Color_Red            = (255,   0,   0)
Color_Gray           = (128, 128, 128)

# These cooler colors are preferred
Color_Turquoise      = ( 64, 224, 208)
Color_Lightcoral     = (240, 128, 128)
Color_Orangered      = (255,  69,   0)
Color_Darkkhaki      = (189, 183, 107)
Color_Gold           = (255, 215,   0)
Color_Violet         = (238, 130, 238)
Color_Darkviolet     = (148,   0, 211)
Color_Limegreen      = ( 50, 205,  50)
Color_Olive          = (128, 128,   0)
Color_Royalblue      = ( 65, 105, 225)
Color_Burlywood      = (222, 184, 135)
Color_Silver         = (192, 192, 192)
Color_Gainsboro      = (220, 220, 220)
Color_Snow           = (255, 250, 250)
Color_Lightgray      = (211, 211, 211)
Color_Firebrick      = (178,  34,  34)
Color_Saddlebrown    = (139,  69,  19)
Color_Darkolivegreen = ( 85, 107,  47)
Color_Darkred        = (139,   0,   0)

# Predefined Colors
bgColor           =  Color_Gainsboro
sbColor           =  Color_Black # scoreboard
aliveTeamColor    =  Color_Black
deadTeamColor     =  Color_Red
teamLengthColor   =  Color_Snow
wbColor           =  Color_Snow
gravColor         =  Color_Lightgray
explosive_color   =  Color_Firebrick
multibullet_color =  Color_Limegreen
bigbullet_color   =  Color_Burlywood
playerColor       = [Color_Darkviolet,     Color_Royalblue, Color_Saddlebrown,
                     Color_Darkolivegreen, Color_Gold,      Color_Violet,
                     Color_Turquoise,      Color_Limegreen, Color_Darkkhaki,
                     Color_Lightcoral,     Color_Burlywood, Color_Silver]

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

skillCardCutInTimePhrases  = [10, 10, 20, 10, 20, 15]
skillCardCutInTime         = sum(skillCardCutInTimePhrases)

skillCardCutInTimesteps    = [skillCardCutInTime - sum(skillCardCutInTimePhrases[:idx])
                              for idx in range(len(skillCardCutInTimePhrases))]

skillCardCutInPicSize      = (225, 225)
skillCardSmallScaleRate    = 1.0
skillCardCutInPicSmallSize = tuple([int(x * skillCardSmallScaleRate) for x in skillCardCutInPicSize])
skillCardLargeScaleRate    = 1.5
skillCardCutInPicLargeSize = tuple([int(x * skillCardLargeScaleRate) for x in skillCardCutInPicSize])

# Size
thermometerBallSize = 80
thermometerBarWidth = 40

# Font
titleFont          = 'View/Font/makinas_scrap/Makinas-Scrap-5.otf'
titleFontSize      = 200

titleSmallFont     = 'View/Font/makinas_scrap/Makinas-Scrap-5.otf'
titleSmallFontSize = 60

teamNameFont       = 'View/Font/Noto/NotoSansCJK-Black.ttc'
teamNameFontSize   = 20

teamLengthFont     = 'View/Font/Noto/NotoSansCJK-Black.ttc'
teamLengthFontSize = 40

teamScoreFont      = 'View/Font/Noto/NotoSansCJK-Black.ttc'
teamScoreFontSize  = 60

countDownFont      = 'View/Font/Noto/NotoSansCJK-Black.ttc'
countDownFontSize  = 200

tmpScoreFont       = 'View/Font/Noto/NotoSansCJK-Black.ttc'
tmpScoreFontSize   = 80
