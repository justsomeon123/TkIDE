# Info on Origin.

Before becoming an actual project with more than just notepad-features, TkIDE was a small ~100 line text editor. However, as I tried expanding it to make it bigger, I didn't try to modularize or get rid of the legacy code. For example, there was a "filename" variable in the code that just represented the most recent filename, and was completely redundant. There was also no removal of repetitive code. All of this and more caused TkIDE to become very unintuitive, and caused a lot of problems while trying to make extensions, or modify the source code.

In an effort to undo some of this, I have decided to start taking some action. For example, tabs are now classes, and seperate from the main code at [tabs.py](source/tabs.py). This is one in many steps I'll have to take to fix TkIDE.

![image](assets/disease.png)