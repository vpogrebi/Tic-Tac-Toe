"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import puremvc.patterns.proxy

import vo
import enum
#import main

class PlayerProxy(puremvc.patterns.proxy.Proxy):
	
	NAME = "PlayerProxy"
	def __init__(self, userMarker):
		super(PlayerProxy, self).__init__(PlayerProxy.NAME, [])
		self.players = []
		self.addPlayer(vo.PlayerVO(enum.PLAYER_USER, userMarker))
		for marker in enum.MarkerTypes:
			if marker is not userMarker:
				self.addPlayer(vo.PlayerVO(enum.PLAYER_AUTO, marker))
				break
			
	def addPlayer(self, player):
		self.players.append(player)

	def nextPlayer(self, player):
		for member in self.players:
			if member is not player:
				return member
			
		

class RoleProxy(puremvc.patterns.proxy.Proxy):

	NAME = "RoleProxy"
	def __init__(self):
		super(RoleProxy, self).__init__(RoleProxy.NAME, [])
		self.data = []
#		self.addItem(vo.RoleVO('lstooge', [enum.ROLE_PAYROLL,enum.ROLE_EMP_BENEFITS]))
#		self.addItem(vo.RoleVO('cstooge', [enum.ROLE_ACCT_PAY,enum.ROLE_ACCT_RCV,enum.ROLE_GEN_LEDGER]))
#		self.addItem(vo.RoleVO('mstooge', [enum.ROLE_INVENTORY,enum.ROLE_PRODUCTION,enum.ROLE_SALES,enum.ROLE_SHIPPING]))
#
#	def getRoles(self):
#		print self.data
#		return self.data
#
#	def addItem(self, item):
#		self.data.append(item)
#
#	def deleteItem(self, item):
#		for i in range(len(self.data)):
#			if self.data[i].username == item.username:
#				del self.data[i]
#				break
#
#	def doesUserHaveRole(self, user, role):
#		hasRole = False;
#		for i in range(len(self.data)):
#			if self.data[i].username == user.username:
#				userRoles = self.data[i].roles
#				for j in range(len(userRoles)):
#					if userRoles[j] == role:
#						hasRole = True
#						break
#		return hasRole
#
#	def addRoleToUser(self, user, role):
#		result = False;
#		if not self.doesUserHaveRole(user, role):
#			for i in range(0,len(self.data)):
#				if self.data[i].username == user.username:
#					userRoles = self.data[i].roles
#					userRoles.append(role)
#					result = True;
#					break
#		self.sendNotification(main.AppFacade.ADD_ROLE_RESULT, result)
#
#	def removeRoleFromUser(self, user, role):
#		if self.doesUserHaveRole(user, role):
#			for i in range(0,len(self.data)):
#				if self.data[i].username == user.username:
#					userRoles = self.data[i].roles
#					for j in range(0,len(userRoles)):
#						if userRoles[j] == role:
#							del userRoles[i]
#							break
#
#	def getUserRoles(self, username):
#		userRoles = []
#		for i in range(0,len(self.data)):
#			if self.data[i].username == username:
#				userRoles = self.data[i].roles
#				break
#		return userRoles