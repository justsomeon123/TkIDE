# Commands

## Basics
First, to start connecting to the api, import the api:

<code>import extapi as api</code>

Then, run the intiate function with the name of your program.

<code>api.InitiateConnection("programname")</code>

This name should be unique, and preferably lowercase.

Once you're done with what your extension/app wanted to do, use the following command to close the connection.

<code>api.ExitConnection()</code>

## Read Commands
- ### GetEditorText
    - Gets the text of the currently open editor.
    - If no editor is open, returns "NO-TEXT" (home page, etc.)
- ### GetFileName
    - Gets the name of the currently opened file.
    - If no editor is open, returns "NO-FILE" (home page, etc.)
- ### TabCount
    - Gets the number of currently opened tabs.