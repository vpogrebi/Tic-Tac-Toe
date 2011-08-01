import wx
import puremvc.interfaces
import puremvc.patterns.mediator

import main
import model

class DialogMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
	"Defines 'GAME OVER' and 'DRAW' MessageDialog notification handlers"
	
	NAME = 'DialogMediator'
	
	def __init__(self, viewComponent):
		super(DialogMediator, self).__init__(DialogMediator.NAME, viewComponent)

	def listNotificationInterests(self):
		return [
			main.AppFacade.SHOW_GAME_OVER,
			main.AppFacade.SHOW_GAME_DRAW,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.SHOW_GAME_OVER:
			dlg = wx.MessageDialog(self.viewComponent, note.getBody(), 'GAME OVER', style = wx.OK)
			result = dlg.ShowModal()
			dlg.Destroy()
		if noteName == main.AppFacade.SHOW_GAME_DRAW:
			dlg = wx.MessageDialog(self.viewComponent, note.getBody(), 'DRAW', style = wx.OK)
			result = dlg.ShowModal()
			dlg.Destroy()

class GameBoardMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
	"""Main application's 'view' mediator. Provides a link and controls interaction 
	between between application's proxies	(PlayerProxy and GameBoardProxy) and its
	view component (GUI). Also handles AppFacade's notifications.
	"""
	NAME = 'GameBoardMediator'
	
	playerProxy = None
	
	def __init__(self, viewComponent):
		"Obtain handlers to view components (proxies), and register events"
		super(GameBoardMediator, self).__init__(GameBoardMediator.NAME, viewComponent)
		# Get PlayerProxy and GameBoardProxy references (handlers)
		self.playerProxy = self.facade.retrieveProxy(model.PlayerProxy.NAME)
		self.gameDataProxy = self.facade.retrieveProxy(model.GameBoardProxy.NAME)

		self.viewComponent.Bind(self.viewComponent.EVT_GAME_START, self.onGameStart)
		self.viewComponent.Bind(self.viewComponent.EVT_GAME_STOP, self.onGameStop)
		self.viewComponent.Bind(self.viewComponent.EVT_MOVE_MADE, self.onPlayerMoved)

	def listNotificationInterests(self):
		"Subscribe to notifications"
		return [
			main.AppFacade.GAME_OVER,
			main.AppFacade.GAME_DRAW,
			main.AppFacade.AUTO_MOVE_MADE,
		]

	def handleNotification(self, note):
		"Notification handler. Handles GAME_OVER, GAME_DRAW and AUTO_MOVE_MADE notifications"
		noteName = note.getName()
		if noteName == main.AppFacade.AUTO_MOVE_MADE:
			(row, col, value) = note.getBody()
			self.gameDataProxy.updateData(row, col, value)
			self.onPlayerMoved(None)
		if noteName == main.AppFacade.GAME_OVER:
			winner = note.getBody()
			self.onGameOver(winner)	
		elif noteName == main.AppFacade.GAME_DRAW:
			self.onGameDraw()	
			
	def onGameStart(self, evt):
		"Initialize view controls and proxies for the new game"
		# Signal GameBoardProxy to initialize game's data
		playerRole = self.viewComponent.getRole()
		self.gameDataProxy.initialize(playerRole)   
		# Signal PlayerProxy to initialize players
		self.playerProxy.initialize(playerRole)
		# Signal GameBoard (GUI) to initialize game bord controls
		self.viewComponent.initialize(playerRole)
		# Signal PlayerProxy to have next player take turn
		self.playerProxy.nextTurn()
	
	def onGameStop(self, evt):
		"Signal view component to stop the game"
		self.viewComponent.onStopGame(None)
	
	def onGameOver(self, winner):
		"Game is over - someone won"
		self.playerProxy.stopGame()
		self.sendNotification(main.AppFacade.SHOW_GAME_OVER, "'%s' IS A WINNER" % winner)
		self.onGameStop(None)
	
	def onGameDraw(self):
		"Game is over - there is a DRAW"
		self.playerProxy.stopGame()
		self.sendNotification(main.AppFacade.SHOW_GAME_DRAW, "WE HAVE A DRAW")
		self.onGameStop(None)
	
	def onPlayerMoved(self, evt):
		"Actions to take upon either player's move"
		if evt:
			# Interactive player made his move - signal game board proxy to update its data
			(row, col, value) = self.viewComponent._lastSelection
			self.gameDataProxy.updateData(row, col, value, updateBoard = False)
		elif self.playerProxy.gameEnabled:
			# Auto player made his move - enable game board so interactive player can take his turn
			self.viewComponent.boardGrid.Enable()

		# Disable current player - so same player can not take turn again
		self.playerProxy.disableCurrentPlayer()
		# Signal next player to take turn
		self.playerProxy.nextTurn()		
		
