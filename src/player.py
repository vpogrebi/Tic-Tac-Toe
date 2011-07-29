import enum

class Player(object):
    type = None
    marker = None
    
    def __init__(self):
        self.type = None
        self.marker = None

    def _isValid(self):
        if self.type not in enum.PlayerTypes:
            raise Exception, "Invalid player type submitted ('%s'). Allowed types: (%s)" % (self.type, enum.PlayerTypes) 
        if self.marker not in enum.MarkerTypes:
            raise Exception, "Invalid marker type submitted ('%s'). Allowed types: (%s)" % (self.marker, enum.MarkerTypes)
        
    def _setMarker(self, marker):
        self.marker = marker 
            
    def takeTurn(self):
        pass
    
class PlayerUser(Player):
    def __init__(self):
        super(PlayerUser, self).__init__()
        self.type = enum.PLAYER_USER
        
    def takeTurn(self):
        pass
    
class PlayerAuto(Player):
    def __init__(self):
        super(PlayerAuto, self).__init__()
        self.type = enum.PLAYER_AUTO
        
    def takeTurn(self):
        pass
