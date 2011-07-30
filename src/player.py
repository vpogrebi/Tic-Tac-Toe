import enum

class Player(object):
    type = None
    role = None
    
    def __init__(self):
        self.type = None
        self.role = None
        self.moveAllowed = False
        _isAuto = False
        
    def _setRole(self, role):
        self.role = role 
    
    def _setType(self, type):
        self.type = type
        
    def isAuto(self):
        return self._isAuto
        
    def allowTurn(self):
        self.moveAllowed = True
        
class PlayerUser(Player):
    def __init__(self):
        super(PlayerUser, self).__init__()
        self.type = enum.PLAYER_USER
        self._isAuto = False
        
class PlayerAuto(Player):
    def __init__(self):
        super(PlayerAuto, self).__init__()
        self.type = enum.PLAYER_AUTO
        self._isAuto = True
        
    def takeTurn(self, data):
        return (0, 0)
