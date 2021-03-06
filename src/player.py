import enum

class Player(object):
    "Implements player's functionality"
    def __init__(self, type = None, role = None):
        self.type = None
        self.role = None
        self.moveAllowed = False
        if type:
            self._setType(type)
        if role:
            self._setRole(role)
        
    def _setRole(self, role):
        if not role in enum.RoleTypes:
            raise Exception, "Invalid role selection"
        self.role = role 
    
    def _setType(self, type):
        if not type in enum.PlayerTypes:
            raise Exception, "Invalid player type"
        self.type = type
        
    def isAuto(self):
        return self.type is enum.PLAYER_AUTO
        
    def allowTurn(self, status):
        self.moveAllowed = status
        
