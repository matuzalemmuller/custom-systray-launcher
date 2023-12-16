from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import psutil
import subprocess

APP_NAME='ladder'
ICON_ACTIVE='icons/icon_active.png'
ICON_INACTIVE='icons/icon_inactive.png'
PROCESS=['/home/matuzalem/dev/ladder-systray/bin/ladder', '-r', 'https://t.ly/14PSf']

# Kill app if already running
def kill_app(systray, icon_inactive, systray_option):
    for p in psutil.process_iter():
        if APP_NAME in p.name() or APP_NAME in ' '.join(p.cmdline()):
            p.terminate()
            p.wait()
            return True
    return False

# Start/stop app
def start_stop_app(systray, icon_inactive, icon_active, systray_option):
    if kill_app(systray, icon_inactive, systray_option):
        systray_option.setText('Start')
        systray.setIcon(icon_inactive)
    else:
        result = subprocess.Popen(PROCESS)
        systray_option.setText('Stop')
        systray.setIcon(icon_active)

# Quit app
def quit_app(app, systray, icon_inactive, systray_option):
    kill_app(systray, icon_inactive, systray_option)
    app.quit()

# Create Qt app 
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Add an icon 
icon_active = QIcon(ICON_ACTIVE) 
icon_inactive = QIcon(ICON_INACTIVE) 

# Add item on the menu bar 
systray = QSystemTrayIcon() 
systray.setIcon(icon_inactive) 
systray.setVisible(True)

# Create the options 
menu = QMenu() 
systray_option = QAction("Start")
menu.addAction(systray_option)
systray_option.triggered.connect(lambda: start_stop_app(systray, icon_inactive, icon_active, systray_option))

quit_option = QAction("Quit")
menu.addAction(quit_option)
quit_option.triggered.connect(lambda: quit_app(app, systray, icon_inactive, systray_option))
systray.activated.connect(lambda: start_stop_app(systray, icon_inactive, icon_active, systray_option))

# Add options to the System Tray
systray.setContextMenu(menu)

# Kill all instances of the app before starting the system tray
while kill_app(systray, icon_inactive, systray_option):
    pass

app.exec_()
