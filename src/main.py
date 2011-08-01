"""
MAIN module of the TIC-TAC-TOE application, an application's 
"entry" point. Defines AppFacade class required by 'pureMVC' 
framework
"""

import components
import controller
import puremvc.patterns.facade

class AppFacade(puremvc.patterns.facade.Facade):
	
	STARTUP			= "startup"			# Application startup
	GAME_OVER		= "gameOver"		# Signals a WIN
	GAME_DRAW		= "gameDraw"		# Signals a DRAW
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