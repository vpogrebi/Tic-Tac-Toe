'''
Created on Aug 1, 2011

@author: valeriy
'''
import copy
import enum
import model
import unittest
import assistant

class AssistantTest(unittest.TestCase):
    """Tests assistant.Assistant class"""

    def setUp(self):
        self.testPlayer = enum.PLAYER_X
        self.boardProxy = model.GameBoardProxy(None)
        self.assistant = assistant.Assistant(self.boardProxy, self.testPlayer)

    def tearDown(self):
        pass

    def test__getScore_PLAYER_WINS(self):
        "Test that Assistant._getScore() returns 1 when given player is a winner"
        self.boardProxy.winner = self.testPlayer
        self.assertEquals(1, self.assistant._getScore())

    def test__getScore_OPPONENT_WINS(self):
        "Test that Assistant._getScore() returns -1 when given player is a loser"
        self.boardProxy.winner = enum.opponent[self.testPlayer]
        self.assertEquals(-1, self.assistant._getScore())

    def test__getScore_NO_WINNER(self):
        "Test that Assistant._getScore() returns 0 when there is no winner"
        self.boardProxy.winner = None
        self.assertEquals(0, self.assistant._getScore())
        
    def test__firstMove_BOARD_IS_BLANK(self):
        "Test that Assistant._firstMove() returns center position when board is blank"
        # Our initial test setup sets game board to a blank state
        self.assertEquals(self.boardProxy.center, self.assistant._firstMove())

    def test__firstMove_BOARD_IS_NOT_BLANK(self):
        "Test that Assistant._firstMove() raises exception when board is blank"
        # Our initial test setup sets game board to a blank state
        self.boardProxy.data[0][0] = self.testPlayer
        self.assertRaises(Exception, self.assistant._firstMove)
        
    def test__immediateWinLose_WIN_LOSE(self):
        "Test that Assistant._immediateWinLose() returns correct move when there is an imminent win/lose opportunity"
        testCases = {'win': [self.testPlayer, None, self.testPlayer],
                     'loss': [enum.opponent[self.testPlayer], None, enum.opponent[self.testPlayer]]}
        expectMove = (0, 1)
        for testCase in testCases:
            self.boardProxy.data[0] = testCases[testCase]
            move = self.assistant._immediateWinLose()
            self.assertEquals(expectMove, move)

    def test__immediateWinLose_NO_IMMEDIATE_WIN_OR_LOSE(self):
        "Test that Assistant._immediateWinLose() raises exception when there is no imminent win/lose opportunity"
        self.assertRaises(Exception, self.assistant._immediateWinLose)

    def test__maxiMin(self):
        "Test that Assistant._maxiMin() returns best possible move"
        dataBefore = copy.deepcopy(self.boardProxy.data)
        bestMove = self.assistant._maxiMin()
        dataAfter = self.boardProxy.data
        # 1 . Check that _maxiMin() does not modify game board's data
        self.assertEquals(dataBefore, dataAfter)
        # 2. Check that ALL possible moves were evaluated
        self.assertEquals(len(self.assistant.scores), 9)
        # 3. Check that suggested move has highest TOTAL score
        bestScore = max([self.assistant.scores[move]['totScore'] for move in self.assistant.scores.keys()])
        self.assertTrue(bestScore, self.assistant.scores[bestMove]['totScore'])
        
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()