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
	GAME_OVER		= "gameOver"		# Signals a WIN
	GAME_DRAW		= "gameDraw"		# Signals a DRAW
	DATA_UPDATED	= "dataUpdated"		# Game board's data updated	
	AUTO_MOVE_MADE	= "autoMoveMade"	# Auto player made his move
	SHOW_GAME_OVER	= "dialodGameOver"	# Show GAME OVER dialog
	SHOW_GAME_DRAW	= "dialodGameDraw"	# Show DRAW dialog
	
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