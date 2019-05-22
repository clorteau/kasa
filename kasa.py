#!/usr/bin/env python3
#
#Turn TP-Link Kasa lights and plugs on and off
#Clem Lorteau - 2019-05-21

import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox
from PySide2.QtCore import QFile, Qt
from functools import partial
from tplink import Core
from config import devices

path = os.path.dirname(os.path.realpath(__file__))

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
    uifile = QFile(os.path.join(path, 'mainwindow.ui'))
    uifile.open(QFile.ReadOnly)
    loader = QUiLoader()
    mainWindow = loader.load(uifile)

    mainWindow.setWindowFlags(mainWindow.windowFlags() | Qt.MSWindowsFixedSizeDialogHint \
                              & ~Qt.WindowMaximizeButtonHint)
    mainWindow.AllOnButton.clicked.connect(partial(action, 'all', 'on'))
    mainWindow.AllOffButton.clicked.connect(partial(action, 'all', 'off'))
    
    row = 1
    for name, ip in devices.items():
        layout = QHBoxLayout()
        layout.setSpacing(10)
        label = QLabel(name)
        onButton = QPushButton('On')
        offButton = QPushButton('Off')
        
        layout.addWidget(onButton)
        layout.addWidget(offButton)
        mainWindow.gridLayout.addWidget(label, row, 0)
        mainWindow.gridLayout.addLayout(layout, row, 1)
        row += 1
        
        onButton.clicked.connect(partial(action, name, 'on'))
        offButton.clicked.connect(partial(action, name, 'off'))

    mainWindow.show()
    mainWindow.resize(mainWindow.gridLayout.totalSizeHint())
    sys.exit(app.exec_())
