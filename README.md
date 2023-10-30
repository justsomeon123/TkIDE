# TkIDE  Version 2.3.2

## August goes. School comes. Coding goes down.

<br>

# Disclaimers

- ## **WARNING**: TkIDE is a work in progress project. I am not responsible for any damage done to your computer by extensions, or by bugged code.

- ## **Beware!**

- ### **TkIDE** could be closed at any time

- ## TkIDE is not an actual IDE. It is a code editor with limited functionality

- ### TkIDE's raw code only works with Python 3.9 and above (as to my knowledge)
- ### Tested on 3.10/3.11

## Changelog

- ## 2.2.1
  - Added more commands, read at [commands.md](extensions/commands.md)
- ## 2.2 
  - File explorer disabled (it didn't work that well)
  - Added support for extensions again baby!!!!!!!!
    -  Based on an api, with socket and thread communication in the ide, allowing for multiple extensions, without lag/freezing.
    - This also at the same time prevents misuse of the ide, because only supported commands will work.
    - Currently there are 3 commands. 2 are necessary (init and close connection) and one allows for access of currently opened text.
    - Will expand, tutorial, more commands, documentation etc in next update.
    - **NOT TESTED ON EXE VERSION**
  - No executable this version.
  - Search from right click menu.



- ## 2.1

  - Added file explorer! (hopefully works?)
  - more readme errors

- ## 2.0

  - Fixed readme errors.
  - New Icon.

- ## 1.8.2

  - Finished right click menu, added paste, cut, delete.

- ## 1.8

  - Finally actually added the syntax highlighting, tested with Python. Problem is it doesn't work fully, as I haven't added all the color rules.
  - Added Image Icon, and actually fixed the deprecation issues, which i left untouched last version.
  - Optimized the syntax highlighting.

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
  - mp3loader (Formerly mp4loader)
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
  - Added new loading screen - ![Loading Screen](assets/LoadingEx.jpg) (removed)
  - Performance improvements
  - Improved extension system - new api for extensions
  - Removed Run command aka disabled it.
<br>

## Included features

### All new syntax highlighting (Pygments)

- Faster than the older regex-based syntax highlighting

### KeyBinds for more functionalty with files

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

### Disclaimer:TkIDE is <b><b>NOT</b></b> pure, untouched tkinter. There are custom classes and in the future there may be some other additions

<br>

- ### Non standard library objects used

  - Pillow
  - Custom tkinter based widgets
  - Pygments
  
### Notes/Goals

- Will try to work on load times (not happening lol)
  - Working with pyinstaller not onefile mode and venvs
  - Works, well - up to 2 times faster than the old version

- More features - maybe?

- The tab system ~~is not perfect~~ trash and will probably be improved in the future.

  - If too many tabs are open the close buttons will clump togther and not work. A solution that could be implemented is to have a scrollbar for the tab system and fixing the custom tab system.

- I am working on a system to run python files and output them to a terminal.

  - I might add the terminal as part of the ide, instead of a new window
