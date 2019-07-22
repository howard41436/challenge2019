import sys

import Events.Manager   as EventManager
import Model.main       as model
import View.main        as view
import Controller.main  as controller
import Interface.main   as helper

import random
import numpy as np

def main(argv):
    seed = 41436
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
