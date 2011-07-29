import wx
import wx.grid as gridlib

import main
import model
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
	
	def __init__(self):
		wx.Frame.__init__(self, parent = None, id = -1, title = "Tic-Tac-Toe", size = (400, 400))
		self.gameBoard = GameBoard(self)
#		self.userList = UserList(self)
#		self.userForm = UserForm(self)
	
class GameBoard(wx.Panel):
	
	evt_START_GAME = wx.NewEventType()
	EVT_START_GAME = wx.PyEventBinder(evt_START_GAME, 1)
	
	evt_STOP_GAME = wx.NewEventType()
	EVT_STOP_GAME = wx.PyEventBinder(evt_STOP_GAME, 1)

	boardGrid = None
	ctrlBtn = None
	makerRbox = None
	
	playerProxy = None

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, id = 2, size = (330, 330))
		self.markerSelectionList = ['X', 'O']
		self.markersSet = False

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
		
		self.markerSelectionRbox = wx.RadioBox(self, -1, "Marker Selection", wx.DefaultPosition, 
									wx.DefaultSize, self.markerSelectionList, 2, wx.RA_SPECIFY_COLS)
		self.markerSelectionRbox.Bind(wx.EVT_RADIOBOX, self.onMarkerSelection)
		self.markerSelectionRbox.SetToolTip(wx.ToolTip("Select 'X' or 'O'"))

		hboxBottom.Add(self.ctrlBtn, 0, wx.RIGHT,10)

		vbox.Add(self.markerSelectionRbox, 0, wx.ALL|wx.ALIGN_CENTER, 10)
		vbox.Add(self.boardGrid, 0, wx.ALL|wx.ALIGN_CENTER, 10)
		vbox.Add(hboxBottom, 0, wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT,10)

		self.SetAutoLayout(True)
		self.SetSizer(vbox)
		self.Layout()
		
	def _setPlayerProxy(self, playerProxy):
		self.playerProxy = playerProxy
		
	def onMarkerSelection(self, evt = None):
		if evt:
			self.playerProxy.setMarkers(self.markerSelectionList[evt.GetInt()])
		else:
			self.playerProxy.setMarkers(self.markerSelectionList[self.markerSelectionRbox.Selection])
			
		self.markersSet = True
		
	def onStartGame(self, evt):
		if not self.markersSet:
			self.onMarkerSelection()
			
		self.boardGrid.ClearGrid()
		self.markerSelectionRbox.Disable()
		self.boardGrid.Enable()
		self.ctrlBtn.SetLabel("Stop Game")
		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStopGame)
	
	def onStopGame(self, evt):
		self.boardGrid.Disable()
		self.markerSelectionRbox.Enable()
		self.ctrlBtn.SetLabel("Start Game")
		self.ctrlBtn.Bind(wx.EVT_BUTTON, self.onStartGame)
	
	def updateBoard(self, data):
		for row in data:
			for col in data[row]:
				self.boardGrid.SetCellValue(row, col, data[row][col])
		
	def onCellSelect(self, evt):		
		try:
			self.boardGrid.SetCellValue(evt.GetRow(), evt.GetCol(), self.playerProxy.getPlayer().marker)
			evt.Skip()
		except IndexError:
			pass
	
