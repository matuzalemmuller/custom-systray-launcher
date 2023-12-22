#!/usr/bin/env python3

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import logging
import os
import signal
import subprocess
import sys

###############################  CONFIGURE HERE ###############################  
ICON_ACTIVE='icons/icon_active.png'
ICON_INACTIVE='icons/icon_inactive.png'
ICON_WARNING='icons/warning.png'
PROCESS=['/home/matuzalem/dev/ladder-systray/bin/ladder', '-r', 'https://t.ly/14PSf']
LAUNCH_ONLY=False
PID=0
###############################################################################

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] - %(levelname)s - %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    stream=sys.stdout)

# Kill app if already running
def kill_running_process():
    global PID
    if PID != 0:
        try:
            logging.info(f'Attempting to kill process with PID {PID}')
            os.kill(PID+1000, signal.SIGTERM)
            logging.info(f'Killed process with PID {PID}')
            PID = 0
        except OSError as err:
            logging.error(f'Error killing process: {err}')
            PID = 0
            return False
    return True

# Start/stop app
def start_stop_app(systray, icon_inactive, icon_active, icon_warning, systray_option):
    global PID
    if not LAUNCH_ONLY:
        if systray_option.text() == 'Stop':
            if kill_running_process():
                systray_option.setText('Start')
                systray.setIcon(icon_inactive)
            else:
                systray_option.setText('Warning/Error')
                systray.setIcon(icon_warning)
            return
        elif systray_option.text() == 'Warning/Error':
            logging.warning('Not launching process because there was an error killing the previous instance')
            return
        else:
            systray_option.setText('Stop')
            systray.setIcon(icon_active)
    result = subprocess.Popen(PROCESS, shell=False, preexec_fn=os.setsid)
    PID = result.pid
    logging.info(f'Launched process {PROCESS} with PID {PID}')

# Quit app
def quit_app(app, systray, icon_inactive, systray_option):
    kill_running_process()
    app.quit()

def main():
    # Create Qt app 
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Add an icon 
    icon_active = QIcon(ICON_ACTIVE) 
    icon_inactive = QIcon(ICON_INACTIVE) 
    icon_warning = QIcon(ICON_WARNING)

    # Add item on the menu bar 
    systray = QSystemTrayIcon()
    if LAUNCH_ONLY:
        systray.setIcon(icon_active)
    else: 
        systray.setIcon(icon_inactive) 
    systray.setVisible(True)
    systray.activated.connect(lambda: start_stop_app(systray, icon_inactive, icon_active, icon_warning, systray_option))

    # Create the options 
    menu = QMenu() 
    systray_option = QAction("Start")
    menu.addAction(systray_option)
    systray_option.triggered.connect(lambda: start_stop_app(systray, icon_inactive, icon_active, icon_warning, systray_option))

    quit_option = QAction("Quit")
    menu.addAction(quit_option)
    quit_option.triggered.connect(lambda: quit_app(app, systray, icon_inactive, systray_option))

    # Add options to the System Tray
    systray.setContextMenu(menu)

    app.exec_()

if __name__ == "__main__":
    main()
