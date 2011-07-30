import puremvc.patterns.proxy

import main
import enum
import player

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
		self._data = None		# Game data (maintained by GameDataProxy)
		
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
		
	def initialize(self, userRole, gameData):
		"Initialize players. Should be called when game is started"
		# Set private game data
		self._data = gameData
		
		# Add two players to self.players list
		self._userPlayer = player.PlayerUser()
		self._autoPlayer = player.PlayerAuto()
		self.players = [self._userPlayer, self._autoPlayer]	
		
		# Assign player roles
		self._assignRoles(userRole)
		# Set player queue
		self._setQueue()
		
	def getUser(self):
		user = None
		for pl in self.players:
			if pl.type == 'user':
				user = pl
				break
			
		return user
	
	def nextTurn(self):
		"Signal next player in the queue to take turn"
		# Get first player in the queue
		self.currPlayer = self.queue.pop(0)
		self.currPlayer.allowTurn()
		if self.currPlayer.isAuto():
			# Signal player to take turn
			(row, col) = self.currPlayer.takeTurn(self._data)
			# Send notification that game's data is updated
			self.sendNotification(main.AppFacade.DATA_UPDATED, (row, col, self.currPlayer.role))
		# Add player to the end of the queue
		self.queue.append(self.currPlayer)
			
class GameDataProxy(puremvc.patterns.proxy.Proxy):
	NAME = "GameDataProxy"
	data = []
	gameBoard = None
	
	def __init__(self, gameBoard):
		super(GameDataProxy, self).__init__(GameDataProxy.NAME, [])		
		self.gameBoard = gameBoard	# GameBoardGrid - GUI panel
		self.initialize()	# Initialize game's board data
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
		
	def initialize(self):
		"Initialize game's board data. initData() must be called each time new game starts"
		self.data = [
						[None, None, None],
						[None, None, None],
						[None, None, None],
					]
		
	def getData(self):
		return self.data
		
	def updateData(self, row, col, value):
		self.data[row][col] = value
		
	def checkWin(self, role):
		for combo in self.winCombos:
			cnt = 0
			for item in combo:
				row = item / 3
				col = item % 3
				if self.data[row][col] == role:
					cnt += 1
					
			if cnt == 3:
				self.sendNotification(main.AppFacade.GAME_OVER, role)
				break
			
