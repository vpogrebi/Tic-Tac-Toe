"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

#import main
import model
import view

import puremvc.patterns.command
import puremvc.interfaces

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
	def execute(self, note):
		mainPanel = note.getBody()
		self.facade.registerProxy(model.PlayerProxy())	
		self.facade.registerProxy(model.GameDataProxy(mainPanel.gameBoard))
		self.facade.registerMediator(view.DialogMediator(mainPanel))
		self.facade.registerMediator(view.GameBoardMediator(mainPanel.gameBoard))

