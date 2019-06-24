import Model.const as model_const

class Item(object):
    def __init__(self):
        self.position = position

class Communism(Item):
    def __init__(self):
        pass

    def trigger(self, player_list):
        total = sum(player.value for player in player_list)
        for player in player_list:
            player.value = total / len(player_list)

class GoHome(Item):
    def __init__(self):
        pass

    def trigger(self, player_list, base_list):
        for player in player_list:
            player.position.x = base_list[player.index].position.x
            player.position.y = base_list[player.index].position.y

class Teleport(Item):
    def __init__(self):
        pass
    
