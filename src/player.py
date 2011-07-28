import enum

class Player(object):
    type = None
    marker = None
    
    def __init__(self, type, marker):
        self.type = type
        self.marker = marker
        self.isValid()

    def isValid(self):
        if self.type not in enum.PlayerTypes:
            raise Exception, "Invalid player type submitted ('%s'). Allowed types: (%s)" % (self.type, enum.PlayerTypes) 
        if self.marker not in enum.MarkerTypes:
            raise Exception, "Invalid marker type submitted ('%s'). Allowed types: (%s)" % (self.marker, enum.MarkerTypes) 
            
    def takeTurn(self):
        pass
    
class PlayerUser(Player):
    def __init__(self, args):
        super(PlayerUser, self).__init__(args)
        
    def takeTurn(self):
        pass
    
class PlayerAuto(Player):
    def __init__(self, args):
        super(PlayerAuto, self).__init__(args)
        
    def takeTurn(self):
        pass
