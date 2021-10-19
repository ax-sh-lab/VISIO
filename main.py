
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMainWindow
from PyQt5.QtCore import Qt, QPoint 
from PyQt5 import QtGui, QtCore
from PIL import ImageGrab
from pathlib import Path
from time import time 

# from PyQt5.QtWidgets import * 
# from PyQt5.QtGui import *

path = Path(__file__).parent

class SnipBase(QMainWindow):
    def __init__(self, screen) -> None:
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
        self.setWindowOpacity(.3)
        self.setGeometry(screen)
        self.begin = QPoint()
        self.end = QPoint()

        self.border_color = QtGui.QColor('black')
        self.background_color = QtGui.QColor(128, 128, 255, 128)

        print('Capture the screen...')

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(self.border_color, 2))
        qp.setBrush(self.background_color)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        self.select_region((
            min(self.begin.x(), self.end.x()),# x1
            min(self.begin.y(), self.end.y()),# y1
            max(self.begin.x(), self.end.x()),# x2,
            max(self.begin.y(), self.end.y()) # y2
        ))

class Snip(SnipBase):
    def validate(self, img):
        pass
    def select_region(self, geometry):
        img = ImageGrab.grab(bbox=geometry)
        self.validate(img)
        folder = path / 'shots'
        folder.mkdir(exist_ok=True)
        date = int(time())
        name = f'visio-{date}.png'
        name = folder / name 
        img.save(name)
        print("Saved as", name)





class TrayIcon(QSystemTrayIcon):
    def __init__(self, app) -> None:
        QSystemTrayIcon.__init__(self)
        icon = QIcon("assets/icon.svg")
        self.setIcon(icon)

        self.setVisible(True)
        self.activated.connect(self.systemIcon)
        self.screen = app.desktop().screenGeometry()
        self.snip = Snip(self.screen)
        self.toggleState = False
        
    def systemIcon(self, reason):
        # QSystemTrayIcon.Unknown	    0	Unknown reason
        # QSystemTrayIcon.Context	    1	The context menu for the system tray entry was requested
        # QSystemTrayIcon.DoubleClick	2	The system tray entry was double clicked. # Note: On macOS, a double click will only be emitted if no context menu is set, since the menu opens on mouse press

        # Constant	Value	Description
        # QSystemTrayIcon.Trigger	    3	The system tray entry was clicked
        # QSystemTrayIcon.MiddleClick	4	The system tray entry was clicked with the middle mouse button
        if reason == QSystemTrayIcon.Trigger:
            self.toggle()
            return 
        if reason == QSystemTrayIcon.Context:
            print("Right clicked")
    
    def toggle(self):
        
        if self.toggleState:
            self.snip.show()
        else:
            self.snip.hide()
        self.toggleState = not self.toggleState


class App(QApplication):
    def __init__(self, *args) -> None:
        QApplication.__init__(self, *args)
        self.setQuitOnLastWindowClosed(False)

  

def main():
    app = App([])
    tray = TrayIcon(app)
    # # Create the menu
    # menu = QMenu()
    # action = QAction("A menu item")
    # menu.addAction(action)

    # # Add a Quit option to the menu.
    # quit = QAction("Quit")
    # quit.triggered.connect(app.quit)
    # menu.addAction(quit)

    # Add the menu to the tray
    # tray.setContextMenu(menu)
    app.exec_()
   


if __name__ == '__main__':
    main()