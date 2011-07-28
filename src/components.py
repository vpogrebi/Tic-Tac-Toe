import wx
import wx.grid
import enum

class WxApp(wx.App):
	
	appFrame = None
	
	def OnInit(self):
		self.appFrame = AppFrame()
		self.appFrame.Show()
		#self.SetTopWindow(self.frame)
		
		return True

class AppFrame(wx.Frame):
	
	gameBoard = None
#	selectionList = None
#	statusText = None
	
	def __init__(self):
		wx.Frame.__init__(self, parent = None, id = -1, title = "Tic-Tac-Toe", size = (400, 400))
		self.gameBoard = GameBoard(self)
#		self.userList = UserList(self)
#		self.userForm = UserForm(self)
	
class GameBoard(wx.Panel):
	
	evt_CLICK = wx.NewEventType()
	EVT_CLICK = wx.PyEventBinder(evt_CLICK, 1)
	
	boardGrid = None
	
	def __init__(self,parent):
		wx.Panel.__init__(self, parent, id = 2, size = (330, 330))
		#self.SetBackgroundColour('Blue')
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		hboxBottom = wx.BoxSizer(wx.HORIZONTAL)
		
		self.boardGrid = wx.grid.Grid(self, -1, )
		self.boardGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.onClick)
		self.boardGrid.CreateGrid(3, 3)
		self.boardGrid.SetDefaultCellAlignment(wx.ALIGN_CENTER_HORIZONTAL, wx.ALIGN_CENTER_VERTICAL)
		
		
#		hboxBottom.Add(self.newBtn, 0, wx.RIGHT,10)
#		hboxBottom.Add(self.deleteBtn, 0, wx.RIGHT,10)
		vbox.Add(self.boardGrid, 0, wx.ALL|wx.ALIGN_CENTER, 10)
#		vbox.Add(hboxBottom, 0, wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT,10)

		self.SetAutoLayout(True)
		self.SetSizer(vbox)
		self.Layout()
	
	def resetBoard(self):
		self.boardGrid.ClearGrid()
	
	def updateCell(self, row, col):
		self.boardGrid.SetCellValue(row, col, "X")
#		self.boardGrid.SetAttr(row, col, wx.grid.GridCellAttr())
		
	def onClick(self, evt):
		try:
			self.updateCell(evt.GetRow(), evt.GetCol())
			self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_CLICK, self.GetId()))
		except IndexError:
			pass
	
#class RolePanel(wx.Panel):
#	
#	evt_ADD_ROLE = wx.NewEventType()
#	EVT_ADD_ROLE = wx.PyEventBinder(evt_ADD_ROLE, 1)
#	
#	evt_REMOVE_ROLE = wx.NewEventType()
#	EVT_REMOVE_ROLE = wx.PyEventBinder(evt_REMOVE_ROLE, 2)
#
#	user = None
#	selectedRole = None
#	
#	roleList = None
#	roleCombo = None
#	addBtn = None
#	removeBtn = None
#	
#	def __init__(self,parent):
#		wx.Panel.__init__(self,parent,id=1,pos=(330,220),size=(330,300))
#		#self.SetBackgroundColour('Red')
#		
#		vbox = wx.BoxSizer(wx.VERTICAL)
#		hboxBottom = wx.BoxSizer(wx.HORIZONTAL)
#		
#		self.roleList = wx.ListBox(self,-1,size=(300,200))
#		self.roleList.Bind(wx.EVT_LISTBOX, self.onListClick)
#		self.roleCombo = wx.ComboBox(self, -1, size=wx.DefaultSize)
#		self.roleCombo.Bind(wx.EVT_COMBOBOX, self.onComboClick)
#		self.addBtn = wx.Button(self, -1, "Add")
#		self.addBtn.Disable()
#		self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
#		self.removeBtn = wx.Button(self, -1, "Remove")
#		self.removeBtn.Disable()
#		self.removeBtn.Bind(wx.EVT_BUTTON, self.onRemove)
#		
#		hboxBottom.Add(self.roleCombo, 0, wx.RIGHT,10)
#		hboxBottom.Add(self.addBtn, 0, wx.RIGHT,10)
#		hboxBottom.Add(self.removeBtn, 0, wx.RIGHT,10)
#		vbox.Add(self.roleList, 1, wx.TOP|wx.CENTER,10)
#		vbox.Add(hboxBottom, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT,10)
#
#		self.SetAutoLayout(True)
#		self.SetSizer(vbox)
#		self.Layout()
#	
#	def updateRoleList(self,items):
#		self.roleList.Clear()
#		self.roleList.AppendItems(items)
#	
#	def updateRoleCombo(self,choices, default):
#		self.roleCombo.Clear()
#		self.roleCombo.AppendItems(choices)
#		self.roleCombo.SetValue(default)
#	
#	def onComboClick(self, evt):
#		if not self.roleCombo.GetValue() == enum.ROLE_NONE_SELECTED:
#			self.addBtn.Enable()
#		else:
#			self.addBtn.Disable()
#		self.roleList.SetSelection(-1)
#		self.selectedRole=self.roleCombo.GetValue()
#	
#	def onListClick(self, evt):
#		if not self.roleList.GetSelection() == enum.ROLE_NONE_SELECTED:
#			self.removeBtn.Enable()
#		else:
#			self.removeBtn.Disable()
#		self.roleCombo.SetValue(enum.ROLE_NONE_SELECTED)
#		self.selectedRole=self.roleList.GetStringSelection()
#	
#	def onAdd(self, evt):
#		self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_ADD_ROLE, self.GetId()))
#	
#	def onRemove(self,evt):
#		self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_REMOVE_ROLE, self.GetId()))

#class CtrlButton(wx.Panel):
#	
#	evt_START = wx.NewEventType()
#	EVT_START = wx.PyEventBinder(evt_START, 1)
#
#	evt_STOP = wx.NewEventType()
#	EVT_STOP = wx.PyEventBinder(evt_STOP, 1)
#
#	ctrlBtn = None
#
#	def __init__(self,parent):
#		wx.Panel.__init__(self,parent,id=3,pos=(0,220),size=(330,300))
#		#self.SetBackgroundColour('Green')
#		
#		vbox = wx.BoxSizer(wx.VERTICAL)
#		hboxBottom = wx.BoxSizer(wx.HORIZONTAL)
#		
#		self.ctrlBtn = wx.Button(self, -1, "Start")
#		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStart)
#		self.stopBtn.Bind(wx.EVT_BUTTON, self.onDelete)
#		
#		
##		grid = wx.GridSizer(7,2,6,0)
##		st1 = wx.StaticText(self, -1, 'First Name')
##		self.firstInput = wx.TextCtrl(self, -1)
##		self.firstInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st1, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.firstInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st2 = wx.StaticText(self, -1, 'Last Name')
##		self.lastInput = wx.TextCtrl(self, -1)
##		self.lastInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st2, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.lastInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st3 = wx.StaticText(self, -1, 'Email')
##		self.emailInput = wx.TextCtrl(self, -1)
##		self.emailInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.emailInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st4 = wx.StaticText(self, -1, 'Username')
##		self.usernameInput = wx.TextCtrl(self, -1)
##		self.usernameInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st4, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.usernameInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st5 = wx.StaticText(self, -1, 'Password')
##		self.passwordInput = wx.TextCtrl(self, -1, style = wx.TE_PASSWORD)
##		self.passwordInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st5, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.passwordInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st6 = wx.StaticText(self, -1, 'Confirm')
##		self.confirmInput = wx.TextCtrl(self, -1, style = wx.TE_PASSWORD)
##		self.confirmInput.Bind(wx.EVT_KEY_UP, self.checkValid)
##		grid.Add(st6, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.confirmInput, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		st7 = wx.StaticText(self, -1, 'Department')
##		self.departmentCombo = wx.ComboBox(self, -1)
##		self.firstInput.Bind(wx.EVT_COMBOBOX, self.checkValid)
##		grid.Add(st7, 0, wx.ALIGN_CENTER_VERTICAL)
##		grid.Add(self.departmentCombo, 0, wx.ALIGN_RIGHT | wx.EXPAND)
##		
##		self.addBtn = wx.Button(self, -1, "Add User", size=(100,-1))
##		self.addBtn.Disable()
##		self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
##		self.cancelBtn = wx.Button(self, -1, "Cancel")
##		self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
##		
##		vbox.Add(grid, 0, wx.ALL | wx.EXPAND, 10)
##		
##		hboxBottom.Add(self.addBtn, 0, wx.RIGHT,10)
##		hboxBottom.Add(self.cancelBtn, 0, wx.RIGHT,10)
##		vbox.Add(hboxBottom, 0, wx.BOTTOM|wx.ALIGN_RIGHT,10)
#
#		self.SetAutoLayout(True)
#		self.SetSizer(vbox)
#		self.Layout()
#	
#	def updateUser(self, user):
#		self.user = user
#		self.usernameInput.SetValue(self.user.username)
#		self.firstInput.SetValue(self.user.fname)
#		self.lastInput.SetValue(self.user.lname)
#		self.emailInput.SetValue(self.user.email)
#		self.passwordInput.SetValue(self.user.password)
#		self.confirmInput.SetValue(self.user.password)
#		self.departmentCombo.SetValue(self.user.department)
#		self.checkValid()
#
#	def updateDepartmentCombo(self,choices, default):
#		self.departmentCombo.Clear()
#		self.departmentCombo.AppendItems(choices)
#		self.departmentCombo.SetValue(default)
#	
#	def updateMode(self, mode):
#		self.mode = mode
#		if self.mode == self.MODE_ADD:
#			self.addBtn.SetLabel("Add User")
#		else:
#			self.addBtn.SetLabel("Update User")
#		
#	def onAdd(self, evt):		
#		if self.mode == self.MODE_ADD:
#			self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_ADD, self.GetId()))
#		else:
#			self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_UPDATE, self.GetId()))
#		self.checkValid()
#	
#	def onCancel(self, evt):
#		self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_CANCEL, self.GetId()))
#		
#	def checkValid(self, evt=None):
#		if self.enableSubmit(self.usernameInput.GetValue(),self.passwordInput.GetValue(),self.confirmInput.GetValue(),self.departmentCombo.GetValue()):
#			self.addBtn.Enable()
#		else:
#			self.addBtn.Disable()
#	
#	def enableSubmit(self, u, p, c, d):
#		return (len(u) > 0 and len(p) >0 and p == c and not d == enum.DEPT_NONE_SELECTED)