import puremvc.patterns.proxy

import main
import enum
import player
import assistant

class PlayerProxy(puremvc.patterns.proxy.Proxy):	
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
		
		if userRole == 'X':
			self._autoPlayer._setRole('O')
			self.playerX = self._userPlayer
			self.playerO = self._autoPlayer
		else: 
			self._autoPlayer._setRole('X')
			self.playerO = self._userPlayer
			self.playerX = self._autoPlayer
				
	def _setQueue(self):
		self.queue = [self.playerX, self.playerO]
		
	def initialize(self, playerRole):
		"Initialize players. Should be called when game is started"
		self.gameEnabled = True
		# Set game's data proxy reference
		self._dataProxy = self.facade.retrieveProxy(GameDataProxy.NAME)
		
		# Add two players to self.players list
		self._userPlayer = player.Player(enum.PLAYER_USER)
		self._autoPlayer = player.Player(enum.PLAYER_AUTO)
		self.players = [self._userPlayer, self._autoPlayer]	
		
		# Assign player roles
		self._assignRoles(playerRole)
		# Set player queue
		self._setQueue()
		
	def stopGame(self):
		self.gameEnabled = False
		
	def startGame(self):
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
				# Send notification that Auto player made move
				self.sendNotification(main.AppFacade.AUTO_MOVE_MADE, (row, col, self.currPlayer.role))
			
	def disableCurrentPlayer(self):
		self.currPlayer.allowTurn(False)
			
class GameDataProxy(puremvc.patterns.proxy.Proxy):
	NAME = "GameDataProxy"
	data = []
	moveAssistant = None
	
	def __init__(self, gameBoard):
		super(GameDataProxy, self).__init__(GameDataProxy.NAME, [])		
		self.winCombos = [	# Winning combinations (this data does not change)
							[0, 1, 2],
							[3, 4, 5],
							[6, 7, 8],
							[0, 3, 6],
							[1, 4, 7],
							[2, 5, 8],
							[0, 4, 8],
							[2, 4, 6],							
						]
		self.assistant = assistant.Assistant(self.winCombos)
		
	def initialize(self, playerRole):
		"Initialize game's board data. initData() must be called each time new game starts"
		role = None
		self.data = [
						[None, None, None],
						[None, None, None],
						[None, None, None],
					]
		if playerRole is enum.MARKER_O:
			role = enum.MARKER_X
		else:
			role = enum.MARKER_O
		
		self.assistant.setRoles(role)
				
	def getData(self):
		"Return copy of the private data"
		return self.data
		
	def updateData(self, row, col, value):
		self.data[row][col] = value
		# Send notification that game's data is updated
		self.sendNotification(main.AppFacade.DATA_UPDATED, (row, col, value))
		# Check if we have a winner
		if not self.checkWin():
			# Check if we have a draw
			if self.assistant._getAvail(self.data) == []:
				self.sendNotification(main.AppFacade.GAME_DRAW)
		
	def checkWin(self):
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
					self.sendNotification(main.AppFacade.GAME_OVER, value)
					return True
			
	def suggestMove(self):
		return self.assistant.suggestMove(self.data)
