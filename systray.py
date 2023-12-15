from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import psutil
import subprocess

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Adding an icon 
icon_active = QIcon("icons/icon_active.png") 
icon_inactive = QIcon("icons/icon_inactive.png") 

# Adding item on the menu bar 
tray = QSystemTrayIcon() 
tray.setIcon(icon_inactive) 
tray.setVisible(True) 

# Creating the options 
menu = QMenu() 
option = QAction("Start")
menu.addAction(option)

# Kills ladder if running
def kill_ladder():
    for p in psutil.process_iter():
        if 'ladder' in p.name() or 'ladder' in ' '.join(p.cmdline()):
            p.terminate()
            p.wait()
            tray.setIcon(icon_inactive)
            option.setText('Start')
            return True
    return False

# Start/stop ladder
def start_stop_ladder():
    if not kill_ladder():
        result = subprocess.Popen(['/home/matuzalem/dev/ladder-systray/bin/ladder', '-r', 'https://t.ly/14PSf'])
        tray.setIcon(icon_active)
        option.setText('Stop')

# Quit app
def quit_app():
    kill_ladder()
    app.quit()

# Linking QAction with function above
option.triggered.connect(start_stop_ladder)

# To quit the app
quit_option = QAction("Quit")
menu.addAction(quit_option)
quit_option.triggered.connect(quit_app)

# Open when left-clicking the icon
tray.activated.connect(start_stop_ladder)

# Adding options to the System Tray
tray.setContextMenu(menu)

# Kills all instances of ladder before starting the system tray
while kill_ladder():
    pass

app.exec_()
