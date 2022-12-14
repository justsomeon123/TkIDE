# TkIDE  Version 1.7.2


# Disclaimers
- ## **WARNING**: TkIDE is a work in progress project. I am not responsible for any damage done to your computer.

- ## **Beware!**
  - ### **TkIDE** could be closed at any time.

- ## TkIDE is not an actual IDE. It is a code editor with limited functionality.


- ### TkIDE's raw code only works with Python 3.9 and above.


## Changes  

- ## 1.7.2
- Worked more on syntax highlighting with [Pygments](https://pygments.org/).
- Fixed deprecation issues with Pillow NEAREST, and imgdhr.
- Removed extensions. They were too much of a hassle, and were too hard for me to get to work. So, as of now, there will be no extensions. In the future there may be extension support, but for now, it will not exist.
- Removed tree file view. It was hard too work on, and there were too many problems with it.

- ## Version 1.7.0
- Finally added decent extension support!
- mp3loader now functions as an extension, and plays music!
- Huge changes in the back end


- ## Version 1.6.2
- Removed venv folder 
- All extensions have to be bundled/packages with required dependncies
- removed clunk in exe
- Pushed extension api back for a while,probably will arrive Feb ~ May
- > ## mp3loader (Formerly mp4loader) 
- Renamed to mp3loader (extension functions/commands renamed appropriately)
- adding mp3 functionality
- ## Version 1.6.1
- Reenabled run function - NO functionality
- Fixed major saving and loading bug
- Optimized code
- Working on extension api - old one removed.
- Removed loading screen.
- ## Version 1.6.0
- New folder view + shortcut to open folder
- Added new loading screen - ![Loading Screen](assets/LoadingEx.jpg)
- Performance improvements
- Improved extension system - new api for extensions
- Removed Run command aka disabled it.
<br>
## Included features
### All new syntax highlighting (Pygments)
- Faster than the older regex-based syntax highlighting

### KeyBinds for more functionalty with files.
- Ctrl+S : Save File 
- Ctrl+O : Open File
- Ctrl+N : New File
- Ctrl+D : Delete File
- Ctrl+R : Run a python file (Doesn't do anything)
### settings.json
- choose the app and file icon
- Select image scaling size

<br>

## Issues
- Highlighting is not working properly. 

## Important Things

### Disclaimer:TkIDE is <b><b>NOT</b></b> pure tkinter. There are custom classes and in the future there may be some wxPython or PyQt
<br>

- ### Non standard library things used:
  - Pillow
  - Custom tkinter based widgets
  - Pygments
  

### Info

- Will try to work on load times (not happening lol)
    - Working with pyinstaller not onefile mode and venvs
    - Works, well - up to 2 times faster than the old version
- more features - maybe?

- The tab system ~~is not perfect~~ trash and will probably be improved in the future.

    - If too many tabs are open the close buttons will clump togther and not work. A solution that could be implemented is to have a scrollbar for the tab system and fixing the custom tab system.

- I am working on a system to run python files and output them to a tkinter terminal.

  - Note:I might add the terminal as part of the ide, instead of a new window 