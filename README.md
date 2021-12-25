# TkIDE  Version 1.6.1 :tada:
Merry Christmas! :christmas_tree: :tada:
# Disclaimers
- ## WARNING: TkIDE is a work in progress project. I am not responsible for any damage done to your computer.
## Included features


## Changes
- ## 1.6.1
- Fixed major saving and loading file bugs.
- Fixed bug where the file would not be saved.
- Fixed bug with no icon, removed splash screen.
- Better Performance and smaller size
- Working on extension api
- removed old extension api
- ## Version 1.6.0
- New folder view + shortcut to open folder
- Added new loading screen - ![Loading Screen](assets/LoadingEx.jpg)
- Performance improvements
- Improved extension system - new api for extensions
- Removed Run command aka disabled it.
<br>
## Included features
### All new syntax highlighting 
- Disabled by default - go to theme.json and copy values in "old" and put that into the main part json
- strings are less laggy and should now work properly
- soon to come - actual differentiating between file types for better highlighting

### KeyBinds for more functionalty with files.
- Ctrl+S : Save File 
- Ctrl+O : Open File
- Ctrl+N : New File
- Ctrl+D : Delete File
- Ctrl+R : Run a python file

### settings.json and theme.json
- choose the app icon
- choose the theme file (Disabled by default)
- choose the default font (NOT USED)
- add the syntax items (NOT USED)
- change syntax
<span style="color:red">c</span>
<span style="color:orange">o</span>
<span style="color:yellow">l</span> 
<span style="color:green">o</span>
<span style="color:blue">r</span>
<span style="color:purple">s</span>
in theme.json (Disabled by default)

<br>

## Issues
- 

## Important Things

### Disclaimer:TkIDE is <b><b>NOT</b></b> pure tkinter. There are custom classes amd in the future there may be some wxPython or PyQt
<br>

also it is not an ide its just a trash code editor with a few features. 

### Info

- Will try to work on load times (not happening lol)
    > On the previous note, numba might be used in the future.
    > On that note, I might now use pyjion as an attempt to speed it up.
- more features - maybe?
- Updated yearly for major updates.
-  Usually updated monthly for minor updates.
- The tab system is not perfect and will probably be improved in the future.
    > If too many tabs are open the close buttons will clump togther and not work. A solution that could be implemented is to have a scrollbar for the tab system and fixing the custom tab system.
- The syntax highlighting is not perfect and will probably be improved in the future.
    > I need more experience with regex before I will try to fix it, - expect delay of 3 - 5 months.
- I am working on an extension system that will allow for smaller builds.
- I am working on a system to run python files and output them to a tkinter terminal.
    > Note:I might  on adding the terminal as input and output for a more intergrated experience.
- Running extension commands has a simple basis for now.
  > You can now add your own commands to the extension system via the extensions folder and commands.json. To run a command type the sections of the command in the command box separated by / and press the run button. All console related code will not work.



## ***Beware***
- ### **TkIDE** could be closed at any time.