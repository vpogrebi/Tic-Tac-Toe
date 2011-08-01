import wx
import wx.grid as gridlib

"""
This module defines application's main GUI components - which are 'enwrapped'
in GameBoard panel. wxPython framework is used for implementing GUI controls
"""

class WxApp(wx.App):
	
	appFrame = None
	
	def OnInit(self):
		self.appFrame = AppFrame()
		self.appFrame.Show()
		return True

class AppFrame(wx.Frame):
	
	gameBoard = None
	
	def __init__(self):
		wx.Frame.__init__(self, parent = None, id = -1, title = "Tic-Tac-Toe", size = (400, 400))
		self.gameBoard = GameBoard(self)
#		self.userList = UserList(self)
#		self.userForm = UserForm(self)
	
class GameBoard(wx.Panel):
	"""Application's main control - game board itself (GUI)"""
	
	# Game started - player clicked 'Start Game'
	evt_GAME_START	= wx.NewEventType()		
	EVT_GAME_START = wx.PyEventBinder(evt_GAME_START, 1)
		
	# Game stopped - player clicked 'Stop Game'
	evt_GAME_STOP	= wx.NewEventType()		
	EVT_GAME_STOP = wx.PyEventBinder(evt_GAME_STOP, 1)

	# Game over - one player wins
	evt_GAME_OVER = wx.NewEventType()
	EVT_GAME_OVER = wx.PyEventBinder(evt_GAME_OVER, 1)
		
	# Player made a move
	evt_MOVE_MADE = wx.NewEventType()
	EVT_MOVE_MADE = wx.PyEventBinder(evt_MOVE_MADE, 1)

	boardGrid = None
	ctrlBtn = None
	radioRoles = None
	
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, id = 2, size = (330, 330))
		self._roleList = ['X', 'O']
		self._data = None	# Underlying representation data - is set by the view (GameBoardMediator)
		self._playerRole = None	# Interactive player's role ('X' or 'O')
		self._lastSelection = None	# This private attribute will contain a (row, col, value) trio - last player's selection
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		hboxBottom = wx.BoxSizer(wx.HORIZONTAL)
		
		self.boardGrid = gridlib.Grid(self, -1, )
		self.boardGrid.CreateGrid(3, 3)

		self.boardGrid.SetColSize(0, 50)
		self.boardGrid.SetColSize(1, 50)
		self.boardGrid.SetColSize(2, 50)
		self.boardGrid.SetRowSize(0, 50)
		self.boardGrid.SetRowSize(1, 50)
		self.boardGrid.SetRowSize(2, 50)

		self.boardGrid.SetColLabelSize(0)
		self.boardGrid.SetRowLabelSize(0)
				
		for row in range(self.boardGrid.GetNumberRows()):
			for col in range(self.boardGrid.GetNumberCols()):
				self.boardGrid.SetCellAlignment(row, col, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
				self.boardGrid.SetCellBackgroundColour(row, col, wx.CYAN)
				self.boardGrid.SetCellFont(row, col, wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD))
		
		self.boardGrid.Disable()
		self.boardGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.onCellSelect)		
		
		self.ctrlBtn = wx.Button(self, -1, "Start Game", size=(100,-1))
		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStartGame)
		
		self.radioRoles = wx.RadioBox(self, -1, "Role Selection", wx.DefaultPosition, 
									wx.DefaultSize, self._roleList, 2, wx.RA_SPECIFY_COLS)
		self.radioRoles.SetToolTip(wx.ToolTip("Select 'X' or 'O'"))

		hboxBottom.Add(self.ctrlBtn, 0, wx.RIGHT,10)

		vbox.Add(self.radioRoles, 0, wx.ALL|wx.ALIGN_CENTER, 10)
		vbox.Add(self.boardGrid, 0, wx.ALL|wx.ALIGN_CENTER, 10)
		vbox.Add(hboxBottom, 0, wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT,10)

		self.SetAutoLayout(True)
		self.SetSizer(vbox)
		self.Layout()
		
	def initialize(self, role):
		"Initialize private data"
		self._playerRole = role
		
	def getRole(self):
		"Obtain current role selection"
		role = self._roleList[self.radioRoles.GetSelection()]
		return role
		
	def onStartGame(self, evt):
		"Initialize game panel for a new game"
		# Prepare (clear) game board (grid only - not the data!)
		self.boardGrid.ClearGrid()
		# Assume that player picked the role - disable radio box 
		self.radioRoles.Disable()
		# Enable board grid
		self.boardGrid.Enable()
		# Update ctrlBtn to say 'Stop Game'
		self.ctrlBtn.SetLabel("Stop Game")
		# Reassign event binding associated with the ctrlBtn
		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStopGame)
		# Notify the view that game has started
		self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_GAME_START, self.GetId()))
		
	def onStopGame(self, evt):
		"End the game - prepare GUI controls for the next game"
		self.boardGrid.Disable()
		self.radioRoles.Enable()
		self.ctrlBtn.SetLabel("Start Game")
		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStartGame)
		if evt:
			# Notify the view that game has been stopped
			self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_GAME_STOP, self.GetId()))
	
	def updateCell(self, row, col, value):
		"Update game board's cell"
		self.boardGrid.SetCellValue(row, col, value)
		
	def onCellSelect(self, evt):
		"What to do upon interactive player's move"		
		row = evt.GetRow()
		col = evt.GetCol()
		if not self.boardGrid.GetCellValue(row, col):
			self._lastSelection = (row, col, self._playerRole)
			# Update grid cell
			self.boardGrid.SetCellValue(row, col, self._playerRole)
			# Disable game board so interactive player can not take turn until auto player completes his turn
			self.boardGrid.Disable()
			# Notify the view that the player made move
			self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.evt_MOVE_MADE, self.GetId()))
			
		evt.Skip()
			
		
