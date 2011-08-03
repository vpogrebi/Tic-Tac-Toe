import enum
import random

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
        self.board = boardProxy     # Reference to a game board's proxy
        self.player = player        # Auto-player
        self.currMove = None        # Used to store current move being evaluated by a _minMax() algorithm
        self.outcomes = {}          # Dictionary containing a list of scores (outcomes) for each possible move (key)
        
        self.strategyList = [
                             self._firstMove, 
                             self._immediateWinLose, 
                             self._minMax,
#                             self._randomChoice
                            ]
        
    def _judge(self, winner):
        """Assign 'score' based on whether current player 
        (self.player) is winner, loser or neither"""
        if winner == self.player:
            return +1
        if winner is None:
            return 0
        return -1

    def _evaluateMove(self, move, player):
        """Evaluate given move made by a given player.
        This is a recursive procedure - it evaluates given move based on
        outcomes of all possible subsequent outcomes (moves) of both players
        """
        row = move[0]
        col = move[1]
        
        try:
            self.board.updateData(row, col, player, updateBoard = False, sendNotifications = False)
            if self.board.gameOver(False):
                outcome = self._judge(self.board.winner)
                self.outcomes.setdefault(self.currMove, []).append(outcome)
                return outcome
            
            # Recursively, obtain a "score" - a value of a given move
            outcomes = (self._evaluateMove(next_move, enum.opponent[player]) for next_move in self.board.getValidMoves())
            if player == self.player:
                # return min(outcomes)
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o, min_element)
                return min_element
            else:
                # return max(outcomes)
                max_element = -1
                for outcome in outcomes:
                    if outcome == +1:
                        return outcome
                    max_element = max(outcome, max_element)
                return max_element
        finally:
            self.board.undoMove(row, col)
    
    def _firstMove(self):
        "Consider that center - is always best first move"
        if self.board.isBlank():
            return (self.board.center, None)
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
                            return ((row, col), None)
                        
        raise Exception, "No immediate win/loss opportunity"
    
    
    def _minMax(self):
        """A MinMax algorithm implementation - a sort-of 'brute force' computation algorithm
        that evaluates every possible move (for both players) and tries to select the best choice
        based on the all possible outcomes
        """        
        scores = {}         # Dictionary mapping numeric scores to a list of possible moves that result in that score 
        self.outcomes = {}  # Initialize dictionary containing a list of scores for each possible move (key)
        allMoves = self.board.getValidMoves()   # Get a list of all available moves 
        
        for move in allMoves:
            self.currMove = move
            # Evaluate given move by obtaining a list of all possible outcomes (scores) that may result from this move
            self._evaluateMove(move, self.player)
            # Sum up the scores corresponding to a given move
            totScore = sum(self.outcomes[move])
            scores.setdefault(totScore, []).append(move)
            
        # Get a list of moves that have highest score
        moves = scores[max(scores.keys())]
        # Randomly shuffle best moves
        random.shuffle(moves)
        # Return first best move and scores (a dictionary containing list of available moves that result in that score - used for testing)
        return(moves[0], scores)
    
    def _randomChoice(self, data):
        "Obtain a random move from the list of all possible available moves"
        avail = self.board.getValidMoves()
        return (avail[random.randrange(len(avail))], None)
    
    def suggestMove(self):
        for strategy in self.strategyList:
            try:
                (move, other) = strategy()
                return move
            except:
                pass