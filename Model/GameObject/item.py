import Model.const as model_const

class Item(object):
    def __init__(self):
        pass

class Communism(Item):
    def __init__(self):
        pass

    def trigger(self, player_list):
        sum = 0
        for player in player_list:
            sum += player.value
        for player in player_list:
            player.value = sum / len(player_list)

class GoHome(Item):
    def __init__(self):
        pass

    def trigger(self, player_list, base_list):
        for player in player_list:
            player.position.x = base_list[ player.index ].position.x
            player.position.y = base_list[ player.index ].position.y

