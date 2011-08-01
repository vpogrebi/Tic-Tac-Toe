import time
import enum
import random

Empty = ' '
Player_X = 'x'
Player_O = 'o'

def allEqual(list):
    """returns True if all the elements in a list are equal, or if the list is empty."""
    return not list or list == [list[0]] * len(list)

def computerPlayer(board, player):
    """Function for the computer player"""
    t0 = time.time()
    opponent = { Player_O : Player_X, Player_X : Player_O }

    def judge(winner):
        if winner == player:
            return +1
        if winner == None:
            return 0
        return -1

    def evaluateMove(self, move, p=player):
        try:
            board.makeMove(move, p)
            if board.gameOver():
                return judge(board.winner())
            outcomes = (evaluateMove(next_move, opponent[p]) for next_move in board.getValidMoves())
            if p == player:
                #return min(outcomes)
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o,min_element)
                return min_element
            else:
                #return max(outcomes)
                max_element = -1
                for o in outcomes:
                    if o == +1:
                        return o
                    max_element = max(o,max_element)
                return max_element
        finally:
            board.undoMove(move)

    moves = [(move, evaluateMove(move)) for move in board.getValidMoves()]
    random.shuffle(moves)
    moves.sort(key = lambda (move, winner): winner)
#    board.makeMove(moves[-1][0], player)
    return(moves[-1][0])


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
    
    def _miniMax(self, data):
        move = computerPlayer(board, player)
    

    
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

class TestBoard(object):
    """This class represents a tic tac toe board state."""
    def __init__(self, data):
        """Initialize all members."""
        for row in data:
            for col in data[row]:
                if not data[row][col]:
                    piece = Empty
                elif data[row][col] == enum.MARKER_X:
                    piece = Player_X
                else:
                    piece = Player_O
                self.pieces[row * 3 + col] = piece
        
        self.field_names = '123456789'

    def winner(self):
        """Determine if one player has won the game. Returns Player_X, Player_O or None"""
        winning_rows = [[0,1,2],[3,4,5],[6,7,8], # vertical
                        [0,3,6],[1,4,7],[2,5,8], # horizontal
                        [0,4,8],[2,4,6]]         # diagonal
        for row in winning_rows:
            if self.pieces[row[0]] != Empty and allEqual([self.pieces[i] for i in row]):
                return self.pieces[row[0]]

    def getValidMoves(self):
        """Returns a list of valid moves. A move can be passed to getMoveName to 
        retrieve a human-readable name or to makeMove/undoMove to play it."""
        return [pos for pos in range(9) if self.pieces[pos] == Empty]

    def gameOver(self):
        """Returns true if one player has won or if there are no valid moves left."""
        return self.winner() or not self.getValidMoves()

    def getMoveName(self, move):
        """Returns a human-readable name for a move"""
        return self.field_names[move]
    
    def makeMove(self, move, player):
        """Plays a move. Note: this doesn't check if the move is legal!"""
        self.pieces[move] = player
    
    def undoMove(self, move):
        """Undoes a move/removes a piece of the board."""
        self.makeMove(move, Empty)
