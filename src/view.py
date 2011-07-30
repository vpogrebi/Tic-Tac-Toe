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
			main.AppFacade.SHOW_DIALOG,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.SHOW_DIALOG:
			dlg = wx.MessageDialog(self.viewComponent, note.getBody(), 'Alert',style=wx.OK|wx.ICON_EXCLAMATION)
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
#			main.AppFacade.GAME_ON,
			main.AppFacade.GAME_OVER,
#			main.AppFacade.GAME_STOPPED,
			main.AppFacade.DATA_UPDATED,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.DATA_UPDATED:
			(row, col, value) = note.getBody()
			self.gameDataProxy.updateData(row, col, value)
			self.viewComponent.updateCell(row, col, value)
			self.onPlayerMoved(None)
		elif noteName == main.AppFacade.GAME_OVER:
			winner = note.getBody()
			self.onGameOver(winner)
			
			
	def onGameStart(self, evt):
		# Signal GameDataProxy to initialize game's data
		self.gameDataProxy.initialize()
		self.playerProxy.initialize(self.viewComponent.getRole(), self.gameDataProxy.getData())
		self.viewComponent.initialize(self.playerProxy.getUser(), self.gameDataProxy.getData())
#		self.viewComponent._setData(self.gameDataProxy.getData())
#		self.viewComponent._setPlayer(self.playerProxy.getUser())
		# Signal PlayerProxy to have next player take turn
		self.playerProxy.nextTurn()
	
	def onGameStop(self, evt):
		self.viewComponent.onStopGame(None)
	
	def onGameOver(self, winner):
		self.sendNotification(main.AppFacade.SHOW_DIALOG, "GAME OVER!\n'%s' IS A WINNER" % winner)
		self.onGameStop(None)
	
	def onPlayerMoved(self, evt):
		# Check if player that made this move - is a winner
		self.gameDataProxy.checkWin(self.playerProxy.currPlayer.role)
		# Signal next player to take turn
		self.playerProxy.nextTurn()		
		
