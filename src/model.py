import puremvc.patterns.proxy

import copy
import enum
import player
import assistant
import tictactoe

class PlayerProxy(puremvc.patterns.proxy.Proxy):
	"""PlayerProxy class defines functionality responsible for "managing"
	players (player.Player objects) and their actions. 
	"""
	NAME = "PlayerProxy"
	queue = []		# Player queue - defines sequence in which players take turns
	players = []	# Players list (just two)
	
	def __init__(self):		
		super(PlayerProxy, self).__init__(PlayerProxy.NAME, [])
		# Initialize important player "handlers" that simplify the game
		self.playerX = None		# 'X' player
		self.playerO = None		# 'O' player
		self.currPlayer = None	# Player who is currently taking turn
		self._dataProxy = None	# Game's data proxy
		self.gameEnabled = True	# Flag indicating whether or not game can go on
		
	def _assignRoles(self, userRole):
		"Assign player roles in the game"
		self._userPlayer._setRole(userRole)
		
		if userRole == enum.PLAYER_X:
			self._autoPlayer._setRole('O')
			self.playerX = self._userPlayer
			self.playerO = self._autoPlayer
		else: 
			self._autoPlayer._setRole('X')
			self.playerO = self._userPlayer
			self.playerX = self._autoPlayer
				
	def _setQueue(self):
		"Establish player's game queue"
		self.queue = [self.playerX, self.playerO]
		
	def initialize(self, playerRole):
		"Initialize players. Should be called when game is started"
		self.gameEnabled = True
		# Set game's data proxy reference
		self._dataProxy = self.facade.retrieveProxy(GameBoardProxy.NAME)
		
		# Add two players to self.players list
		self._userPlayer = player.Player(enum.PLAYER_USER)
		self._autoPlayer = player.Player(enum.PLAYER_AUTO)
		self.players = [self._userPlayer, self._autoPlayer]	
		
		# Assign player roles
		self._assignRoles(playerRole)
		# Set player queue
		self._setQueue()	
		
	def stopGame(self):
		"Stop the game - disable further player's actions"
		self.gameEnabled = False
		
	def startGame(self):
		"Start the game - enable player's actions"
		self.gameEnabled = True
		
	def nextTurn(self):
		"Signal next player in the queue to take turn"
		if self.gameEnabled:
			# Get first player in the queue
			self.currPlayer = self.queue.pop(0)
			self.currPlayer.allowTurn(True)
			# Add player to the end of the queue
			self.queue.append(self.currPlayer)
	
			if self.currPlayer.isAuto():
				# Signal player to take turn
				(row, col) = self._dataProxy.suggestMove()
				# Send notification that auto-player made move
				self.sendNotification(tictactoe.AppFacade.AUTO_MOVE_MADE, (row, col, self.currPlayer.role))
			
	def disableCurrentPlayer(self):
		"Disable current player's actions"
		self.currPlayer.allowTurn(False)
			
class GameBoardProxy(puremvc.patterns.proxy.Proxy):
	"""GameBoardProxy - defines functionality responsible for "managing"
	game board and its underlying data. It also instantiates an assistant
	(instance of assistant.Assistant class) that suggests auto-player's moves 
	"""
	NAME = "GameBoardProxy"
	
	def __init__(self, gameBoard):
		super(GameBoardProxy, self).__init__(GameBoardProxy.NAME, [])		
		self.winner = None			# Who is current winner (if any)?
		self.assistant = None		# Assistent - an instance of assistant.Assistant class
		self.center = [1, 1]		# Center of the game board
		self.gameBoard = gameBoard	# Game board's GUI panel (wxPython controls)
		self.blankBoard = [
						[None, None, None],
						[None, None, None],
						[None, None, None],
					]
		self.data = copy.deepcopy(self.blankBoard)
		self.winCombos = [			# Winning combinations (this data does not change)
							[0, 1, 2],
							[3, 4, 5],
							[6, 7, 8],
							[0, 3, 6],
							[1, 4, 7],
							[2, 5, 8],
							[0, 4, 8],
							[2, 4, 6],							
						]
		
	def initialize(self, playerRole):
		"Initialize game's board data. initData() must be called each time new game starts"
		self.winner = None
		self.data = copy.deepcopy(self.blankBoard)
		self.assistant = assistant.Assistant(self, enum.opponent[playerRole])
				
	def isBlank(self):
		"Is board blank? Returns True or False"
		return self.data == self.blankBoard
		
	def cntForCombo(self, combo, value):
		"How many times given value appears in a given combo (a triplet of game board's positions)"
		cnt = 0
		for item in combo:
			row = item / 3
			col = item % 3
			if self.data[row][col] == value:
				cnt += 1		
		return cnt
	
	def getData(self):
		"Return copy of the private data"
		return self.data
		
	def getWinCombos(self):
		"Return game's winning combinations"
		return self.winCombos
	
	def updateData(self, row, col, value, updateBoard = True, sendNotifications = True):
		"""Update game board's item (row, col) with the given value. 
		Also updates game board's GUI and sends advisory notifications - based on the value
		of updateBoars and sendNotifications flags
		"""
		self.data[row][col] = value
		if updateBoard:
			self.gameBoard.updateCell(row, col, value)
		if sendNotifications:
			# Check if we have a winner
			if not self.gameOver():
				# Check if we have a draw
				if self.getValidMoves() == []:
					self.sendNotification(tictactoe.AppFacade.GAME_DRAW)
					
	def undoMove(self, row, col):
		"Undo a move. This method is used by the assistant to undo its 'simulation' moves"
		self.data[row][col] = None
		self.winner = None
		
	def gameOver(self, sendNotification = True):
		"Check if any player has won"

		for value in enum.RoleTypes:
			for combo in self.winCombos:
				cnt = 0
				for item in combo:
					row = item / 3
					col = item % 3
					if self.data[row][col] == value:
						cnt += 1
						
				if cnt == 3:
					self.winner = value
					if sendNotification:
						self.sendNotification(tictactoe.AppFacade.GAME_OVER, value)
					return True
			
	def getValidMoves(self):
		"Return a list of all available moves"
		return([(row, col) for row in range(len(self.data))
							for col in range(len(self.data[row]))
							if self.data[row][col] is None])
		
	def suggestMove(self):
		"Suggest auto-player's move. Uses assistant entity to compute best move"
		return self.assistant.suggestMove()
