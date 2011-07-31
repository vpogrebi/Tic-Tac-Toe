"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import wx
import puremvc.interfaces
import puremvc.patterns.mediator

import main
import model
import enum
import vo

class DialogMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
	
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
	
	NAME = 'GameBoardMediator'
	
	playerProxy = None
	
	def __init__(self, viewComponent):
		super(GameBoardMediator, self).__init__(GameBoardMediator.NAME, viewComponent)
		# Get PlayerProxy and GameDataProxy references (handlers)
		self.playerProxy = self.facade.retrieveProxy(model.PlayerProxy.NAME)
		self.gameDataProxy = self.facade.retrieveProxy(model.GameDataProxy.NAME)

		self.viewComponent.Bind(self.viewComponent.EVT_GAME_START, self.onGameStart)
		self.viewComponent.Bind(self.viewComponent.EVT_GAME_STOP, self.onGameStop)
		self.viewComponent.Bind(self.viewComponent.EVT_MOVE_MADE, self.onPlayerMoved)

	def listNotificationInterests(self):
		return [
			main.AppFacade.GAME_OVER,
			main.AppFacade.GAME_DRAW,
			main.AppFacade.DATA_UPDATED,
			main.AppFacade.AUTO_MOVE_MADE,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.DATA_UPDATED:
			(row, col, value) = note.getBody()
			self.viewComponent.updateCell(row, col, value)
		elif noteName == main.AppFacade.AUTO_MOVE_MADE:
			(row, col, value) = note.getBody()
			self.gameDataProxy.updateData(row, col, value)
			self.onPlayerMoved(None)
		elif noteName == main.AppFacade.GAME_OVER:
			winner = note.getBody()
			self.onGameOver(winner)	
		elif noteName == main.AppFacade.GAME_DRAW:
			self.onGameDraw()	
			
	def onGameStart(self, evt):
		# Signal GameDataProxy to initialize game's data
		playerRole = self.viewComponent.getRole()
		self.gameDataProxy.initialize(playerRole)   
		# Signal PlayerProxy to initialize players
		self.playerProxy.initialize(playerRole)
		# Signal GameBoard (GUI) to initialize game bord controls
		self.viewComponent.initialize(playerRole)
		# Signal PlayerProxy to have next player take turn
		self.playerProxy.nextTurn()
	
	def onGameStop(self, evt):
		self.viewComponent.onStopGame(None)
	
	def onGameOver(self, winner):
		self.playerProxy.stopGame()
		self.sendNotification(main.AppFacade.SHOW_GAME_OVER, "'%s' IS A WINNER" % winner)
		self.onGameStop(None)
	
	def onGameDraw(self):
		self.playerProxy.stopGame()
		self.sendNotification(main.AppFacade.SHOW_GAME_DRAW, "WE HAVE A DRAW")
		self.onGameStop(None)
	
	def onPlayerMoved(self, evt):
		if evt:
			(row, col, value) = self.viewComponent._lastSelection
			self.gameDataProxy.updateData(row, col, value)
		elif self.playerProxy.gameEnabled:
			self.viewComponent.boardGrid.Enable()

		self.playerProxy.disableCurrentPlayer()
		# Signal next player to take turn
		self.playerProxy.nextTurn()		
		
