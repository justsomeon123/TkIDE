import extapi as api
ext = api.APIInstance("test")  # Initialize the connection before calling GetEditorText()
print(ext.GetEditorText())
print(ext.GetFileName())
ext.ExitConnection()
del ext