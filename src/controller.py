import model
import view

import puremvc.interfaces
import puremvc.patterns.command

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
	"Application's STARTUP command - application's initialization"
	def execute(self, note):
		mainPanel = note.getBody()
		self.facade.registerProxy(model.PlayerProxy())	
		self.facade.registerProxy(model.GameBoardProxy(mainPanel.gameBoard))
		self.facade.registerMediator(view.DialogMediator(mainPanel))
		self.facade.registerMediator(view.GameBoardMediator(mainPanel.gameBoard))

