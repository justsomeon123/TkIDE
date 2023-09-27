# Commands

## Basics
First, to start connecting to the api, import the api:

```py 
import extapi as api
```

Then make a subclass of the api.Api

```py
class ExtensionName(api.APIInstance)
    def event_func1(self):
        #code code code
    
    def event_func2(self):
        #code code code
```
Now, initialize the extension.

```py 
extension = ExtensionName("Test",{"001":["event_func1","event_func2"]})
```

The first argument is the name of the extension, which should be unique, and preferably lowercase, although this doesn't affect anything, because the server only recognizes the client by a generated sequence.

The second argument is the event functions. It is a dictionary of functions that run on a certain event code. In the above example, when a file is opened (code 001), functions event_func1 and event_func2 will run in that order.

## Registering for Events
 - Simply pass the second argument in the initializing function as a dict of format:
 - ``` py 
    {"event_code":["event_func","event_func1"...],"event_code2":["event2_func",...],...}
   ```

## Event Codes
 - ### 001:
    - On File Open
 - ### 002:
    - On File Content Change

## Read Commands
- ### GetEditorText
    - Gets the text of the currently open editor.
    - If no editor is open, returns "NO-TEXT" (home page, etc.)
- ### GetFileName
    - Gets the name of the currently opened file.
    - If no editor is open, returns "NO-FILE" (home page, etc.)
- ### TabCount
    - Gets the number of currently opened tabs.
