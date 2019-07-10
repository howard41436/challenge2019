class BaseEvent(object):
    """
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    """
    __slots__ = ('name',)
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class EventInitialize(BaseEvent):
    """
    Initialize event.
    """
    def __init__(self):
        self.name = "Initialize event"
    def __str__(self):
        return self.name

class EventRestart(BaseEvent):
    def __init__(self):
        self.name = "Restart event"
    def __str__(self):
        return self.name

class EventQuit(BaseEvent):
    """
    Quit event.
    """
    def __init__ (self):
        self.name = "Quit event"
    def __str__(self):
        return self.name

class EventStateChange(BaseEvent):
    """
    change state event.
    """
    __slots__ = ('name', 'state')
    def __init__(self, state):
        self.name = "StateChange event"
        self.state = state
    def __str__(self):
        return "{0} => StateTo: {1}".format(self.name, self.state)

class EventEveryTick(BaseEvent):
    """
    Tick event.
    """
    def __init__ (self):
        self.name = "Tick event"
    def __str__(self):
        return self.name

class EventEverySec(BaseEvent):
    """
    Sec event.
    """
    def __init__(self):
        self.name = "Sec event"
    def __str__(self):
        return self.name

class EventTimeUp(BaseEvent):
    """
    TimeUp event.
    """
    def __init__(self):
        self.name = "TimeUp event"
    def __str__(self):
        return self.name

class EventMove(BaseEvent):
    """
    Move event.
    """
    __slots__ = ('name', 'player_index', 'direction')
    def __init__(self, player_index, direction):
        self.name = "Move event"
        self.player_index = player_index
        self.direction = direction
    def __str__(self):
        return "{0} => player_index = {1}, DirectionTo: {2}".format(self.name, self.player_index, self.direction)

class EventTriggerItem(BaseEvent):
    """
    Buy/Use item.
    """
    __slots__ = ('name', 'player_index')
    def __init__(self, player_index):
        self.name = "Trigger item event"
        self.player_index = player_index
    def __str__(self):
        return f"{self.name} => player_index = {self.player_index}"


class EventEqualize(BaseEvent):
    """
    Equalize event.
    This event should be triggered when two player bump into each other.
    """
    __slots__ = ('name', 'position')
    def __init__(self, position):
        """
        position : tuple(x, y) or vec2(x, y) indicates the collision position
        """
        self.name = "Equalize event"
        self.position = position
    def __str__(self):
        return f"{self.name} => collision_position = {self.position}"
        

class EventIGoHome(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "I Go Home"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventOtherGoHome(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Other Go Home"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name


class EventShuffleBases(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Shuffle Bases"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name


class EventTheWorldStart(BaseEvent):
    '''
    A player trigger 'The World'(time stop)
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = f"Player {player.index} triggers The World"
        self.position = tuple(player.position)
        self.player_index = player.index
    def __str__(self):
        return self.name

class EventTheWorldStop(BaseEvent):
    '''
    The duration of 'The world' ends
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "The World Ends"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventMagnetAttractStart(BaseEvent):
    '''
    The duration of 'Magnet Attract' starts
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Magnet Attract Start"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventMagnetAttractStop(BaseEvent):
    '''
    The duration of 'Magnet Attract' ends
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Magnet AttractEnd"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventRadiationOil(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Radiation Oil"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventRadiusNotMoveStart(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "RadiusNotMove Start"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventRadiusNotMoveStop(BaseEvent):
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "RadiusNotMove End"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventInvincibleStart(BaseEvent):
    '''
    A player trigger 'Invincible'
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Invincible Start"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventInvincibleStop(BaseEvent):
    '''
    The duration of 'Invincible' ends
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "Invincible End"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventFaDaCaiStart(BaseEvent):
    '''
    A player trigger 'FaDaCai'
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "FaDaCai Start"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventFaDaCaiStop(BaseEvent):
    '''
    The duration of 'FaDaCai' ends
    '''
    __slots__ = ('name', 'player_index', 'position')
    def __init__(self, player):
        self.name = "FaDaCai End"
        self.player_index = player.index
        self.position = tuple(player.position)
    def __str__(self):
        return self.name

class EventCutInStart(BaseEvent):
    '''
    A player triggers a strong skill.
    '''
    __slots__ = ('name', 'player_index', 'skill_name')
    def __init__(self, player_index, skill_name):
        self.name = "Cut-In Start"
        self.player_index = player_index
        self.skill_name = skill_name
    def __str__(self):
        return self.name

class EventEatOil(BaseEvent):
    '''
    A player triggers a strong skill.
    '''
    __slots__ = ('name', 'oil_value')
    def __init__(self, oil_value):
        self.name = "Eat oil"
        self.oil_value = oil_value
    def __str__(self):
        return self.name

class EventStorePrice(BaseEvent):
    '''
    A player goes home and the score increases.
    This event is for triggering sound effect.
    '''
    __slots__ = ('name', 'store_price')
    def __init__(self, store_price):
        self.name = "Store Price"
        self.store_price = store_price
    def __str__(self):
        return self.name

class EventBuyItem(BaseEvent):
    '''
    A player buys a item from market
    '''
    __slots__ = ('name', 'bought_item')
    def __init__(self, item):
        self.name = f"{item.name} is brought"
        self.bought_item = item
    def __str__(self):
        return self.name

class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    __slots__ = ('name', 'listeners')
    def __init__(self):
        self.listeners = []

    def register_listener(self, listener):
        """ 
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        """ 
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        pass
        
    def post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        # # this segment use to debug
        # if not (isinstance(event, Event_EveryTick) or isinstance(event, Event_EverySec)):
        #     print( str(event) )
        for listener in self.listeners:
            listener.notify(event)
