#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import sleep
import logging
import os
import psutil
import signal
import subprocess
import sys
import threading

###############################  CONFIGURE HERE ###############################
LAUNCH_ONLY = False   # (required) If the program will only be launched of started+stopped
PROCESS = [""]        # (required) Command to start the process
STOP_PROCESS = [""]   # Command to stop the process (if not provided, pid from PROCESS will be killed if LAUNCH_ONLY is False)
ICON_ACTIVE = ""      # (required) Systray icon
ICON_INACTIVE = ""    # (required if LAUNCH_ONLY is True) Icon for inactive in case behavior is start/stop
ICON_WARNING = ""     # (required if LAUNCH_ONLY is True) Icon for pid died while running in case behavior is start/stop
###############################################################################
PID = 0

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] - %(levelname)s - %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
    stream=sys.stdout,
)

# Check PID status and change systray icon if process was terminated
class CheckPIDStatus(threading.Thread):
    def __init__(self, systray, systray_option, icon_warning):
        super(CheckPIDStatus, self).__init__()
        self.stop = False
        self.systray = systray
        self.systray_option = systray_option
        self.icon_warning = icon_warning

    def run(self):
        while not (self.stop):
            global PID
            if PID != 0:
                proc = psutil.Process(PID)
                if not psutil.pid_exists(PID) or proc.status() == psutil.STATUS_ZOMBIE:
                    self.systray_option.setText("Warning/Error")
                    self.systray.setIcon(self.icon_warning)
            sleep(5)


def check_variables():
    if any(var not in globals() for var in ('LAUNCH_ONLY','PROCESS','ICON_ACTIVE')):
        logging.error("Missing one or more required variables: LAUNCH_ONLY, PROCESS, ICON_ACTIVE")
        sys.exit(1)
    if not LAUNCH_ONLY and any(var not in globals() for var in ('ICON_INACTIVE','ICON_WARNING')):
        logging.error("Missing one or more required variables: ICON_INACTIVE, ICON_WARNING (LAUNCH_ONLY is False)")
        sys.exit(1)
    else:
        if 'STOP_PROCESS' in globals():
            logging.info("STOP_PROCESS is provided but LAUNCH_ONLY is True")


# Kill app if already running
def kill_running_process():
    global PID
    if PID != 0:
        try:
            logging.info(f"Attempting to kill process with PID {PID}")
            os.kill(PID, signal.SIGTERM)
            logging.info(f"Killed process with PID {PID}")
            PID = 0
        except OSError as err:
            logging.error(f"Error killing process: {err}")
            PID = 0
            return False
    return True


# Start/stop app
def start_stop_app(systray, icon_inactive, icon_active, icon_warning, systray_option):
    global PID
    if not LAUNCH_ONLY:
        if systray_option.text() == "Stop":
            if 'STOP_PROCESS' in globals() and STOP_PROCESS[0] != "":
                result = subprocess.Popen(STOP_PROCESS, shell=False, preexec_fn=os.setsid)
                PID = 0
                logging.info(f"Stopped process gracefully")
                systray_option.setText("Start")
                systray.setIcon(icon_inactive)
            elif kill_running_process():
                systray_option.setText("Start")
                systray.setIcon(icon_inactive)
            else:
                systray_option.setText("Warning/Error")
                systray.setIcon(icon_warning)
            return
        elif systray_option.text() == "Warning/Error":
            logging.warning(
                "Not launching process because there was an error with the previous instance"
            )
            return
        else:
            systray_option.setText("Stop")
            systray.setIcon(icon_active)
    result = subprocess.Popen(PROCESS, shell=False, preexec_fn=os.setsid)
    PID = result.pid
    logging.info(f"Launched process {PROCESS} with PID {PID}")


# Quit app
def quit_app(app, systray, icon_inactive, systray_option, thread):
    thread.stop = True
    app.quit()


def main():
    check_variables()

    # Create Qt app
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Add an icon
    if not LAUNCH_ONLY:
        icon_inactive = QIcon(ICON_INACTIVE)
        icon_warning = QIcon(ICON_WARNING)
    else:
        icon_inactive = ""
        icon_warning = ""
    icon_active = QIcon(ICON_ACTIVE)

    # Add item on the menu bar
    systray = QSystemTrayIcon()
    if LAUNCH_ONLY:
        systray.setIcon(icon_active)
    else:
        systray.setIcon(icon_inactive)
    systray.setVisible(True)
    systray.activated.connect(
        lambda: start_stop_app(
            systray, icon_inactive, icon_active, icon_warning, systray_option
        )
    )

    # Create the options
    menu = QMenu()
    systray.setContextMenu(menu)
    systray_option = QAction("Start")
    menu.addAction(systray_option)
    systray_option.triggered.connect(
        lambda: start_stop_app(
            systray, icon_inactive, icon_active, icon_warning, systray_option
        )
    )

    # Thread to check if PIDs are still running
    thread_pid_status = CheckPIDStatus(systray, systray_option, icon_warning)
    if not LAUNCH_ONLY:
        thread_pid_status.start()

    quit_option = QAction("Quit")
    menu.addAction(quit_option)
    quit_option.triggered.connect(
        lambda: quit_app(app, systray, icon_inactive, systray_option, thread_pid_status)
    )

    app.exec_()


if __name__ == "__main__":
    main()
