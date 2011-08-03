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

    def test__judge_PLAYER_WINS(self):
        "Test that Assistant._judge() returns 1 when given player is a winner"
        self.assertEquals(1, self.assistant._judge(self.testPlayer))

    def test__judge_OPPONENT_WINS(self):
        "Test that Assistant._judge() returns -1 when given player is a loser"
        self.assertEquals(-1, self.assistant._judge(enum.opponent[self.testPlayer]))

    def test__judge_NO_WINNER(self):
        "Test that Assistant._judge() returns 0 when there is no winner"
        self.assertEquals(0, self.assistant._judge(None))
        
    def test__evaluateMove_RESTORES_BOARD(self):
        "Test that Assistant._evaluateMove() does not modify game board's data"
        dataBefore = copy.deepcopy(self.boardProxy.data)
        testMove = [1, 1]
        self.assistant._evaluateMove(testMove, self.testPlayer)
        dataAfter = self.boardProxy.data
        self.assertEquals(dataBefore, dataAfter)
        
    def test__evaluateMove_WIN_OR_LOSS(self):
        "Test that Assistant._evaluateMove() returns 1 or -1 when there is a win or loss situation"
        testCases = {'win': {'pos': [self.testPlayer, None, self.testPlayer], 'move': [0, 1], 'expect': 1},
                     'loss': {'pos': [enum.opponent[self.testPlayer], None, enum.opponent[self.testPlayer]], 'move': [1, 1], 'expect': -1}}
        for testCase in testCases:
            self.boardProxy.data[0] = testCases[testCase]['pos']
            res = self.assistant._evaluateMove(testCases[testCase]['move'], self.testPlayer)
            self.assertEquals(testCases[testCase]['expect'], res)
            
    def test__firstMove_BOARD_IS_BLANK(self):
        "Test that Assistant._firstMove() returns center position when board is blank"
        # Our initial test setup sets game board to a blank state
        self.assertEquals(self.boardProxy.center, self.assistant._firstMove()[0])

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
            (move, other) = self.assistant._immediateWinLose()
            self.assertEquals(expectMove, move)

    def test__immediateWinLose_NO_IMMEDIATE_WIN_OR_LOSE(self):
        "Test that Assistant._immediateWinLose() raises exception when there is no imminent win/lose opportunity"
        self.assertRaises(Exception, self.assistant._immediateWinLose)

    def test__minMax(self):
        "Test that Assistant._minMax() returns best possible move"
        (suggestedMove, scores) = self.assistant._minMax()
        # 1. Check that ALL possible moves were evaluated
        self.assertEquals(len(scores), 9)
        # 2. Check that suggested move is among best moves
        bestMoves = scores[max(scores.keys())]
        self.assertTrue(suggestedMove in bestMoves)
        
                
if __name__ == "__main__":
    unittest.main()