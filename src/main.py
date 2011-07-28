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
	
	STARTUP			= "startup"
	START_GAME		= "startGame"
	STOP_GAME		= "stopGame"
	END_GAME		= "endGame"
	ROLE_SELECTED	= "roleSelected"

	SELECTION_MADE	= "selectionMade"
	SHOW_DIALOG		= "showDialog"
	
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