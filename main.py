import sys

import Events.Manager   as EventManager
import Model.main       as model
import View.main        as view
import Controller.main  as controller
import Interface.main   as helper

import random
import numpy as np

seeds = {
    '3 6 9 4': 55158,
    '2 1 5 6': 67233,
    '2 3 7 10': 8080,
    '8 1 7 6': 79038,
    '2 1 9 4': 80786,
    '8 3 5 9': 79964,
    '2 8 6 10': 12973,
    '5 7 9 10': 50712,
    '3 1 4 10': 43959,
    '8 5 7 4': 57607,
    'master 2 3 8': 8467,
}

def main(argv):
    seed = seeds[' '.join(argv[1:5]).strip()]
    random.seed(seed)
    np.random.seed(seed)

    evManager = EventManager.EventManager()
    gamemodel = model.GameEngine(evManager, argv[1:])
    Control   = controller.Control(evManager, gamemodel)
    interface = helper.Interface(evManager, gamemodel)
    graphics  = view.GraphicalView(evManager, gamemodel)
    sound = view.Sound(evManager, gamemodel)

    gamemodel.run()
 
    return 0
  
if __name__ == '__main__':
    sys.exit(main(sys.argv))
