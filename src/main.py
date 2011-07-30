"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""
import wx
import puremvc.patterns.facade
import components
import controller

class AppFacade(puremvc.patterns.facade.Facade):
	
	STARTUP			= "startup"			# Application startup
	GAME_ON			= "gameOn"			# Player clicked "Start Game"
	GAME_OVER		= "gameOver"		# Signals end of game (one player wins)
	GAME_STOPPED	= "gameStopped"		# Signals end of game (player clicked "Stop Game")
	DATA_UPDATED	= "dataUpdated"		# Game board's data updated
	
	UPDATE_GAME_BOARD	= "updateBoard"	# Update game board (grid)
	UPDATE_GAME_DATA	= "updateData"	# Update game's data
	SHOW_DIALOG       	= "showDialog"	# Show dialog
	

	def __init__(self):
		self.initializeFacade()
		
	@staticmethod
	def getInstance():
		return AppFacade()
		
	def initializeFacade(self):
		super(AppFacade, self).initializeFacade()
		self.initializeController()

	def initializeController(self):
		super(AppFacade, self).initializeController()		
		super(AppFacade, self).registerCommand(AppFacade.STARTUP, controller.StartupCommand)

if __name__ == '__main__':
	
	app = AppFacade.getInstance()
	wxApp = components.WxApp()
	app.sendNotification(AppFacade.STARTUP, wxApp.appFrame)
	wxApp.MainLoop()