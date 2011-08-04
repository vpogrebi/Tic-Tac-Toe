import enum
import random

cnt1 = 0
cnt2 = 0

class Assistant(object):
    """Assistant - is a helper class developed to assist application's model
    (model.GameBoardProxy) in suggesting an automated move. It is
    instantiated by GameBoardProxy.initialize() method. Four strategies are
    defined that assist in computing auto-player's move (though one strategy
    is no longer used).
    
    suggestMove() - is the only "public" method defined by this class. 
    It is being called from model.GameBoardProxy.suggestMove() method
    """
    board = None
    
    def __init__(self, boardProxy, player):
        self.board = boardProxy        
        self.player = player
        self.scores = {}        
        self.strategyList = [
                             self._firstMove, 
                             self._immediateWinLose,
                             self._maxiMin, 
#                             self._randomChoice
                            ]
        
    def _getScore(self):
        """Get 'score' based on whether current player 
        (self.player) is winner, loser or neither"""
        score = 0
        if self.board.winner == self.player:
            score = 1
        elif self.board.winner == enum.opponent[self.player]:
            score = -1
        return score

    def _maximizedMove(self):
        ''' Find maximized move'''
            
        bestscore = None
        bestmove = None
        
        for move in self.board.getValidMoves():
            (row, col) = move
            self.board.updateData(row, col, self.player, updateBoard = False, sendNotifications = False)
            
            if self.board.gameOver(False):
                score = self._getScore()
            else:
                next_move, score = self._minimizedMove()
       
            self.scores[move] = score
            self.board.undoMove(row, col)
           
            if bestscore == None or score > bestscore:
                bestscore = score
                bestmove = move

        return bestmove, bestscore
    
    def _minimizedMove(self):
        ''' Find the minimized move'''

        bestscore = None
        bestmove = None

        for move in self.board.getValidMoves():
            (row, col) = move
            self.board.updateData(row, col, enum.opponent[self.player], updateBoard = False, sendNotifications = False)

            if self.board.gameOver(False):
                score = self._getScore()
            else:
                next_move, score = self._maximizedMove()
       
            self.board.undoMove(row, col)
           
            if bestscore == None or score < bestscore:
                bestscore = score
                bestmove = move

        return bestmove, bestscore

    def _firstMove(self):
        "Consider that center - is always best first move"
        if self.board.isBlank():
            return self.board.center
        else:
            raise Exception, "Game board is not blank"
        
    def _immediateWinLose(self):
        "Checks if we can detect immediate win/lose opportunity"
        for value in (self.player, enum.opponent[self.player]):
            for combo in self.board.getWinCombos():
                cnt = self.board.cntForCombo(combo, value)
                if cnt == 2:
                    for item in combo:
                        row = item / 3
                        col = item % 3
                        if not self.board.data[row][col]:
                            # We found item that will either give us a win, or protect from loss
                            return (row, col)
                        
        raise Exception, "No immediate win/loss opportunity"
    
    def _maxiMin(self):
        self.scores = {}
        (bestMove, bestScore) = self._maximizedMove()
        return bestMove
    
    def _randomChoice(self, data):
        "Obtain a random move from the list of all possible available moves"
        avail = self.board.getValidMoves()
        return avail[random.randrange(len(avail))]
    
    def suggestMove(self):
        for strategy in self.strategyList:
            try:
                return strategy()
            except:
                pass