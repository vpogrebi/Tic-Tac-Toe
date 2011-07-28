"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import main
import model
#import view

import puremvc.patterns.command
import puremvc.interfaces

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
	def execute(self, note):
		self.facade.registerProxy(model.UserProxy())
		self.facade.registerProxy(model.RoleProxy())
		
		mainPanel = note.getBody()
		
#		self.facade.registerMediator(view.DialogMediator(mainPanel))
#		self.facade.registerMediator(view.UserFormMediator(mainPanel.userForm))
#		self.facade.registerMediator(view.UserListMediator(mainPanel.userList))
#		self.facade.registerMediator(view.RolePanelMediator(mainPanel.rolePanel))

class AddCellTakenCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
	def execute(self, note):
		result = note.getBody()
		if not result:
			self.facade.sendNotification(main.AppFacade.SHOW_DIALOG, "Cell already taken")

