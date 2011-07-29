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
import vo

class DialogMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
	
	NAME = 'DialogMediator'
	
	def __init__(self, viewComponent):
		super(DialogMediator, self).__init__(DialogMediator.NAME, viewComponent)

	def listNotificationInterests(self):
		return [
#		main.AppFacade.SHOW_DIALOG,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.SHOW_DIALOG:
			dlg = wx.MessageDialog(self.viewComponent, note.getBody(), 'Alert',style=wx.OK|wx.ICON_EXCLAMATION)
			result = dlg.ShowModal()
			dlg.Destroy()

class GameBoardMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
	
	NAME = 'GameBoardMediator'
	
	userProxy = None
	
	def __init__(self, viewComponent):
		super(GameBoardMediator, self).__init__(GameBoardMediator.NAME, viewComponent)
		self.playerProxy = self.facade.retrieveProxy(model.PlayerProxy.NAME)
		self.viewComponent._setPlayerProxy(self.playerProxy)	

	def listNotificationInterests(self):
		return [
#			main.AppFacade.START_GAME,
#			main.AppFacade.STOP_GAME,
		]

	def handleNotification(self, note): 
		noteName = note.getName()
		if noteName == main.AppFacade.START_GAME:
			self.viewComponent.resetBoard()
		
#	def onAdd(self, evt):
#		user = vo.UserVO(self.viewComponent.usernameInput.GetValue(), 
#			  		     self.viewComponent.firstInput.GetValue(), 
#					     self.viewComponent.lastInput.GetValue(), 
#					     self.viewComponent.emailInput.GetValue(), 
#					     self.viewComponent.passwordInput.GetValue(),
#					     self.viewComponent.departmentCombo.GetValue())
#		self.viewComponent.user = user
#		self.userProxy.addItem(user)
#		self.sendNotification(main.AppFacade.USER_ADDED, user)
#		self.clearForm()
#
#	def onUpdate(self, evt):
#		user = vo.UserVO(self.viewComponent.usernameInput.GetValue(), 
#			  		     self.viewComponent.firstInput.GetValue(), 
#					     self.viewComponent.lastInput.GetValue(), 
#					     self.viewComponent.emailInput.GetValue(), 
#					     self.viewComponent.passwordInput.GetValue(),
#					     self.viewComponent.departmentCombo.GetValue())
#		self.viewComponent.user = user
#		self.userProxy.updateItem(user)
#		self.sendNotification(main.AppFacade.USER_UPDATED, user)
#		self.clearForm()
#
#	def onCancel(self, evt):
#		self.sendNotification(main.AppFacade.CANCEL_SELECTED)
#		self.clearForm()

#class UserListMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
#
#	NAME = 'UserListMediator'
#	
#	userProxy = None
#
#	def __init__(self, viewComponent):
#		super(UserListMediator, self).__init__(UserListMediator.NAME, viewComponent)
#		
#		self.userProxy = self.facade.retrieveProxy(model.UserProxy.NAME)
#		self.viewComponent.updateUserGrid(self.userProxy.getUsers())
#		
#		self.viewComponent.Bind(self.viewComponent.EVT_USER_SELECTED,self.onSelect)
#		self.viewComponent.Bind(self.viewComponent.EVT_NEW,self.onNew)
#		self.viewComponent.Bind(self.viewComponent.EVT_DELETE,self.onDelete)
#
#	def listNotificationInterests(self):
#		return [
#		main.AppFacade.CANCEL_SELECTED,
#		main.AppFacade.USER_UPDATED,
#		main.AppFacade.USER_ADDED,
#		main.AppFacade.USER_DELETED
#		]
#
#	def handleNotification(self, note): 
#		noteName = note.getName()
#		if noteName == main.AppFacade.CANCEL_SELECTED:
#			self.viewComponent.deSelect()
#			self.viewComponent.updateUserGrid(self.userProxy.getUsers())
#		
#		elif noteName == main.AppFacade.USER_UPDATED:
#			self.viewComponent.deSelect()
#			self.viewComponent.updateUserGrid(self.userProxy.getUsers())
#		
#		elif noteName == main.AppFacade.USER_ADDED:
#			self.viewComponent.deSelect()
#			self.viewComponent.updateUserGrid(self.userProxy.getUsers())
#		
#		elif noteName == main.AppFacade.USER_DELETED:
#			self.viewComponent.deSelect()
#			self.viewComponent.updateUserGrid(self.userProxy.getUsers())
#			
#	def onSelect(self, evt):
#		self.sendNotification(main.AppFacade.USER_SELECTED,self.viewComponent.selectedUser)
#	
#	def onNew(self, evt):
#		user = vo.UserVO()
#		self.sendNotification(main.AppFacade.NEW_USER, user)
#
#	def onDelete(self, evt):
#		self.sendNotification(main.AppFacade.DELETE_USER,self.viewComponent.selectedUser)
#
#class RolePanelMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
#
#	NAME = 'RolePanelMediator'
#	
#	roleProxy = None
#
#	def __init__(self, viewComponent):
#		super(RolePanelMediator, self).__init__(RolePanelMediator.NAME, viewComponent)
#
#		self.roleProxy = self.facade.retrieveProxy(model.RoleProxy.NAME)
#		self.viewComponent.updateRoleCombo(enum.RoleList, enum.ROLE_NONE_SELECTED)
#		
#		self.viewComponent.Bind(self.viewComponent.EVT_ADD_ROLE,self.onAddRole)
#		self.viewComponent.Bind(self.viewComponent.EVT_REMOVE_ROLE,self.onRemoveRole)
#	
#	def getRolePanel(self):
#		return viewComponent
#	
#	def onAddRole(self,evt):
#		self.roleProxy.addRoleToUser(self.viewComponent.user, self.viewComponent.selectedRole)
#
#	def onRemoveRole(self,evt):
#		self.roleProxy.removeRoleFromUser(self.viewComponent.user, self.viewComponent.selectedRole)
#		self.viewComponent.updateRoleList(self.roleProxy.getUserRoles(self.viewComponent.user.username))
#
#	def listNotificationInterests(self):
#		return [
#		main.AppFacade.NEW_USER,
#		main.AppFacade.USER_ADDED,
#		main.AppFacade.USER_UPDATED,
#		main.AppFacade.USER_DELETED,
#		main.AppFacade.CANCEL_SELECTED,
#		main.AppFacade.USER_SELECTED,
#		main.AppFacade.ADD_ROLE_RESULT
#		]
#
#	def handleNotification(self, note): 
#		noteName = note.getName()	
#
#		if noteName ==	main.AppFacade.NEW_USER:
#			self.clearForm()
#
#		elif noteName ==  main.AppFacade.USER_ADDED:
#			self.viewComponent.user = note.getBody()
#			roleVO = vo.RoleVO(self.viewComponent.user.username)
#			self.roleProxy.addItem(roleVO)
#			self.clearForm()
#
#		elif noteName ==  main.AppFacade.USER_UPDATED:
#			self.clearForm()
#
#		elif noteName ==  main.AppFacade.USER_DELETED:
#			self.clearForm()
#
#		elif noteName ==  main.AppFacade.CANCEL_SELECTED:
#			self.clearForm()
#
#		elif noteName ==  main.AppFacade.USER_SELECTED:
#			self.viewComponent.user = note.getBody()
#			self.viewComponent.updateRoleList(self.roleProxy.getUserRoles(self.viewComponent.user.username))
#
#		elif noteName ==  main.AppFacade.ADD_ROLE_RESULT:
#			self.viewComponent.updateRoleList(self.roleProxy.getUserRoles(self.viewComponent.user.username))
#		
#	def clearForm(self):   
#		self.viewComponent.user = None
#		self.viewComponent.updateRoleList([])
#		self.viewComponent.roleCombo.SetStringSelection(enum.ROLE_NONE_SELECTED)