#!/usr/bin/env python3
#
#Turn TP-Link Kasa lights and plugs on and off
#Clem Lorteau - 2019-05-21

import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox, QMainWindow
from PySide2.QtCore import QFile, Qt, QSettings
from functools import partial
from tplink import Core
from config import devices

path = os.path.dirname(os.path.realpath(__file__))

class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        uifile = QFile(os.path.join(path, 'mainwindow.ui'))
        uifile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(uifile)
        uifile.close()
        self.setCentralWidget(self.ui)
        self.setWindowTitle(self.ui.windowTitle())
        self.setWindowIcon(self.ui.windowIcon())
        
        self.setWindowFlags(self.windowFlags() \
                            & ~Qt.WindowMaximizeButtonHint)
        self.ui.AllOnButton.clicked.connect(partial(action, 'all', 'on'))
        self.ui.AllOffButton.clicked.connect(partial(action, 'all', 'off'))
        
    def closeEvent(self, event):
        settings = QSettings('Clem Lorteau', 'Kasa')
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        event.accept()

    def readSettings(self):
        settings = QSettings('Clem Lorteau', 'Kasa')
        self.restoreGeometry(settings.value('geometry'))
        self.restoreState(settings.value('windowState'))
        

def action(target, command):
    """Swith lamp/switch on/off
    target: string
       Name of the lamp/switch to act on: must be either 'all' or a name defined the 'devices' dict

    action: string
       Either 'on' or 'off'
    """
    try:
        if (target == 'all'):
            for name, ip in devices.items():
                Core().sendCommand(ip, command)
        else:
            Core().sendCommand(devices[target], command)
    except Exception as e:
        QMessageBox.critical(None, 'Error', str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    
    row = 1
    for name, ip in devices.items():
        layout = QHBoxLayout()
        layout.setSpacing(10)
        label = QLabel(name)
        onButton = QPushButton('On')
        offButton = QPushButton('Off')
        
        layout.addWidget(onButton)
        layout.addWidget(offButton)
        mainWindow.ui.gridLayout.addWidget(label, row, 0)
        mainWindow.ui.gridLayout.addLayout(layout, row, 1)
        row += 1
        
        onButton.clicked.connect(partial(action, name, 'on'))
        offButton.clicked.connect(partial(action, name, 'off'))
        

    mainWindow.show()
    mainWindow.readSettings()
    sys.exit(app.exec_())
