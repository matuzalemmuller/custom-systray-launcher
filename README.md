# Description

A simple script to create custom launchers in the system tray. Confirmed to work on Linux under Debian XFCE, may require some small tweaks to run in other DEs/macOS/Windows.

## What this is not

This is not a complex way to manage applications. Although there is a very basic check to see if a launched process is still running, the intent of this project is not to manage application state or perform complex operations.

No CLI/GUI support is provided out of the box for multiple reasons, with the main one being that I do not need these features myself.

# Installation

Download the repository/[script](./systray.py) and install the requirements.
```
pip3 install -r requirements.txt
```

# Run

Simply change the variables in the script and run it.

## Variables

|Option|Description|
| ------------- | ------------- |
|`LAUNCH_ONLY` (use with caution)|If the command provided will only be launched or if it will be treated as a standalone application that can be started/stopped|
|`ICON_ACTIVE`|Path to icon to be displayed when app has been launched|
|`ICON_INACTIVE`|Path to icon to be displayed when the app is not running. Optional if `LAUNCH_ONLY` is set to `True`|
|`ICON_WARNING`|Path to icon to be displayed when a process is identified to have crashed/stopped running unexpectedly. Optional if `LAUNCH_ONLY` is set to `True`|
|`PROCESS`|Process to launch - note the [subprocess.Popen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen) syntax|
|`STOP_PROCESS` (untested/experimental)|Command to stop process. If not provided, the process PID will be killed. Note the [subprocess.Popen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen) syntax|

# TODO

Nothing to do so far. I put this script together to solve a need I had, and decided to make it open source. There are many places where it can be improved but it works well enough for me.
