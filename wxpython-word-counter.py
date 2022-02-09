import wx
from collections import Counter 
import os
import re

class windowClass(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs)
        
        self.my_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        btn = wx.Button(self, label='Open File (.txt)')
        btn.Bind(wx.EVT_BUTTON, self.onOpen)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.my_text, 1, wx.ALL|wx.EXPAND)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(sizer)
        self.Centre()
        self.basicGUI()
        
    def onOpen(self, event):
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fobj:
                for line in fobj:
                    count = Counter(word for line in fobj for word in line.split())
        top_words = count.most_common(3)
        self.my_text.WriteText('\n-------------------------------------------\n')
        self.my_text.WriteText('The three most used words in the file are: \n')
        self.my_text.WriteText(str(top_words))

    def basicGUI(self):

        panel = wx.Panel(self)

        menuBar = wx.MenuBar()

        fileButton = wx.Menu()
        editButton = wx.Menu()
        importItem = wx.Menu()
        viewItem   = wx.Menu()
        
#       Build a menu entry - text only
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit', 'Exit sample ...')
#        ID_HOST = wx.NewId()
        viewHostItem  = fileButton.Append(wx.ID_ANY, 'Host', 'Retrieve Host ...')
        captureItem  = fileButton.Append(wx.ID_ANY, 'Capture', 'Start Capture Mode ...')
        monitorItem  = fileButton.Append(wx.ID_ANY, 'Monitor', 'Start Monitor Mode ...')

        menuBar.Append(fileButton, 'File')
        menuBar.Append(editButton, 'Edit')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_MENU, self.ViewHost, viewHostItem)
        self.Bind(wx.EVT_MENU, self.CaptureMode, captureItem)
        self.Bind(wx.EVT_MENU, self.MonitorMode, monitorItem)

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Waiting To Start')

        self.SetTitle('Word Counter')
        self.Show(True)

    def Quit(self, e):
        yesNoBox = wx.MessageDialog(None, 'Are you sure you want to Quit?', 'Question', wx.YES_NO)
        yesNoAnswer = yesNoBox.ShowModal()
        yesNoBox.Destroy()
        if yesNoAnswer == wx.ID_YES:
            self.Close()

    def ViewHost(self, e):
        self.Close()

    def CaptureMode(self, e):
        self.statusbar.SetStatusText('Data Capture Mode')

        self.statusbar.SetStatusText('Exit Capture Mode')

    def MonitorMode(self,e):
        self.statusbar.SetStatusText('Data Monitor Mode')
        self.statusbar.SetStatusText('Exit Monitor Mode')

def main():
    app = wx.App()
    windowClass(None, 0, size=(500,400))
    app.MainLoop()

main()