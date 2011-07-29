import puremvc.patterns.proxy

import main
import enum
import player

class PlayerProxy(puremvc.patterns.proxy.Proxy):	
	NAME = "PlayerProxy"
	
	def __init__(self):
		super(PlayerProxy, self).__init__(PlayerProxy.NAME, [])
		self.queue = []
		self.playerX = None
		self.playerO = None
		self.user = player.PlayerUser()
		self.auto = player.PlayerAuto()
			
	def getPlayer(self):
		return self.user
	
	def setMarkers(self, userMarker):
		self.user.marker = userMarker
		if userMarker == 'X':
			self.auto._setMarker('O')
		else:
			self.auto._setMarker('X') 
	
	def setQueue(self):
		self.queue = [self.playerX, self.playerO]
		
	def nextPlayer(self):
		next = self.queue.pop(0)
		self.queue.append(next)
		return next
			
class GameBoardProxy(object):
	NAME = "GameBoardProxy"
	
	def __init__(self):
		super(GameBoardProxy, self).__init__(GameBoardProxy.NAME, [])
		self.data = [
						[None, None, None],
						[None, None, None],
						[None, None, None],
					]
		self.winCombos = [
							[0, 1, 2],
							[3, 4, 5],
							[6, 7, 8],
							[0, 3, 6],
							[1, 4, 7],
							[2, 5, 8],
							[0, 4, 8],
							[2, 4, 6],							
						]
		
	def updateItem(self, row, col, value):
		self.data[row][col] = value
		self.checkWin(value)
		
	def checkWin(self, value):
		for combo in self.winCombos:
			cnt = 0
			for item in combo:
				row = item / 3
				col = item % 3
				if self.data[row][col] == value:
					cnt += 1
					
			if cnt == 3:
				self.sendNotification(main.AppFacade.PLAYER_WIN, value)
				break
			
	