
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

class TrayIcon(QSystemTrayIcon):
    def __init__(self) -> None:
        QSystemTrayIcon.__init__(self)
        icon = QIcon("assets/icon.svg")
        self.setIcon(icon)

        self.setVisible(True)
        self.activated.connect(self.systemIcon)
        
    def systemIcon(self, reason):
        # QSystemTrayIcon.Unknown	    0	Unknown reason
        # QSystemTrayIcon.Context	    1	The context menu for the system tray entry was requested
        # QSystemTrayIcon.DoubleClick	2	The system tray entry was double clicked. # Note: On macOS, a double click will only be emitted if no context menu is set, since the menu opens on mouse press

        # Constant	Value	Description
        # QSystemTrayIcon.Trigger	    3	The system tray entry was clicked
        # QSystemTrayIcon.MiddleClick	4	The system tray entry was clicked with the middle mouse button
        if reason == QSystemTrayIcon.Trigger:
            print('Clicked')
            return 
        if reason == QSystemTrayIcon.Context:
            print("Right clicked")


class App(QApplication):
    def __init__(self, *args) -> None:
        QApplication.__init__(self, *args)
        self.setQuitOnLastWindowClosed(False)

  

def main():
    app = App([])
    tray = TrayIcon()
    # Create the menu
    menu = QMenu()
    action = QAction("A menu item")
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    app.exec_()
   


if __name__ == '__main__':
    main()