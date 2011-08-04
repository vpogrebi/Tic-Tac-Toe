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
        self.board = boardProxy # Game board proxy (manages game's data and contains methods used in this module)    
        self.player = player    # Auto-player's instance
        self.scores = {}        # Dictionary used to assist self._maxiMin() (MaxiMin or MiniMax algorithm implementation) in suggesting best moves
        self.strategyList = [   # List of strategies in the order they are evaluated
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

    def _maximizedMove(self, depth = 0):
        "Find maximized move"
            
        bestscore = None
        bestmove = None
        
        for move in self.board.getValidMoves():
            (row, col) = move
            self.board.updateData(row, col, self.player, updateBoard = False, sendNotifications = False)

            if depth == 0:
                self.currMove = move    # Save our current move
                self.scores[self.currMove] = {'score': None, 'totScore': 0}
            
            if self.board.gameOver(False):
                score = self._getScore()
                # Add current score to the self.scores[self.currMove]['totScore'] value
                self.scores[self.currMove]['totScore'] += score
            else:
                (next_move, score) = self._minimizedMove(depth + 1)
       
            self.scores[self.currMove]['score'] = score
            self.board.undoMove(row, col)
           
            if bestscore == None or score > bestscore:
                bestscore = score
                bestmove = move

        return bestmove, bestscore
    
    def _minimizedMove(self, depth):
        "Find the minimized move"

        bestscore = None
        bestmove = None

        for move in self.board.getValidMoves():
            (row, col) = move
            self.board.updateData(row, col, enum.opponent[self.player], updateBoard = False, sendNotifications = False)

            if self.board.gameOver(False):
                score = self._getScore()
                # Add current score to the self.scores[self.currMove]['totScore'] value
                self.scores[self.currMove]['totScore'] += score
            else:
                (next_move, score) = self._maximizedMove(depth + 1)
       
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
        # Obtain a list of auto-player's moves that have best score
        bestMoves = [move for move in self.scores.keys() if self.scores[move]['score'] == bestScore]
        # Find highest TOTAL score among these moves
        highestTotScore = max([self.scores[move]['totScore'] for move in bestMoves])
        # Obtain a list of moves that have total score equal to <highestTotScore> (these moves would have highest probability of NOT LOSING)
        best_bestMoves = [move for move in bestMoves if self.scores[move]['totScore'] == highestTotScore]
        # Randomly shuffle this list if it has more than one item - to get different results to make game more interesting
        if len(best_bestMoves) > 1:
            random.shuffle(best_bestMoves)
        return best_bestMoves[0]
    
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