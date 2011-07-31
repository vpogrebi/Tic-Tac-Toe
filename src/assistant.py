import enum
import random

class Assistant(object):
    def __init__(self, winCombos):
        self.winCombos = winCombos        
        self.myRole = None
        self.otherRole = None
        
        self.centerRow  = 1
        self.centerCol  = 1
        self.blankBoard = [[None, None, None],
                           [None, None, None],
                           [None, None, None]]

        self.checkList = [self._firstMove, 
                          self._immediateCoice, 
#                          self._complexChoice, 
                          self._centerChoice, 
                          self._randomChoice]
        
    def _isBlank(self, data):
        return data == self.blankBoard
    
    def _getAvail(self, data):
        return([(row, col) for row in range(len(data))
                            for col in range(len(data[row]))
                            if data[row][col] is None])
        
    def _countForCombo(self, data, combo, value):
        cnt = 0
        for item in combo:
            row = item / 3
            col = item % 3
            if data[row][col] == value:
                cnt += 1
        
        return cnt
    
    def _firstMove(self, data):
        if self._isBlank(data):
            return (self.centerRow, self.centerCol)
        
    def _immediateCoice(self, data):
        for value in (self.myRole, self.otherRole):
            for combo in self.winCombos:
                cnt = self._countForCombo(data, combo, value)
                if cnt == 2:
                    for item in combo:
                        row = item / 3
                        col = item % 3
                        if not data[row][col]:
                            # We found item that will either give us a win, or protect from loss
                            return (row, col)
                    
        return None
    
    def _centerChoice(self, data):
        if not data[self.centerRow][self.centerCol]:
            return (self.centerRow, self.centerCol)
        
    def _randomChoice(self, data):
        avail = self._getAvail(data)
        return avail[random.randrange(len(avail))]
    
    def setRoles(self, role):
        self.myRole = role
        if role is enum.MARKER_O:
            self.otherRole = enum.MARKER_X
        else:
            self.otherRole = enum.MARKER_O
            
    def suggestMove(self, data):
        for check in self.checkList:
            pos = check(data)
            if pos:
                return pos

