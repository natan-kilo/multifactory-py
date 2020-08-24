# Multifactory
### Create Semi-Dedicated Satisfactory Servers

## Requirements:
- The only requirement is Python 3.x (No libraries required)

#### Server Owners:
To use it, simply put `server.py` and `common.py` into a folder on your Server you want to save the World Saves in, and run `server.py` with Python 3.x.
- To change the IP and Port where your Server will listen for incoming connections, you will also have to change `server.py:113` to the desired IP and Port before running it

#### Users:
To use it, simply put `client.py` and `common.py` into the World's Save Folder and run `client.py` with Python 3.x.
- To find your World's Save Folder, Press the Windows Key and type _(or Paste)_ _`%LOCALAPPDATA%\FactoryGame\Saved\SaveGames`_, where the Latest changed Folder will be the World you saved changes last.
- For simplicity's sake, you can create `start.bat` following the steps listed below in the same folder and create a Desktop Shortcut for it for simple access once you closed the Folder

##### Creating `start.bat`
1. Press the Windows Key, type `cmd` and Press `Enter`
2. Type: `py`, `python`, or `python3`, and notice if any of them say `Python 3.X.X` and `>>>` a few lines later
3. If one of the commands works, remember it and go to the next step. If None of the commands work, make sure to [install Python](https://www.python.org/ "Python Homepage") and add it to PATH first, before retrying the last step 
4. In the Folder, go to `View` and enable `File Extensions`
5. In the folder, rightclick and create a new Text File.
6. Rename the File to `start.bat` and Press `Yes`
7. Rightclick `start.bat` and Press `Edit`
8. Copy this into the file
```batch
@echo off
python client.py
REM replace 'python' with the command that worked for you
pause
```
9. Press `Ctrl+S` to Save the File
10. Close the Editor, rightclick the File -> `Send To` -> `Desktop (Create Shortcut)`
11. To run the Program in the Future, simply doubleclick the Shortcut on your Desktop
