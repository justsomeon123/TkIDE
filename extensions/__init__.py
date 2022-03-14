from os.path import dirname, basename, join
import glob,json,importlib

def LoadExtensionPt(sections:list,command:bool=False):
    if command:
        print("mp3Loader.py initizalized and working")
        sections.insert(0,"command")
    else:pass
    
    if len(sections) == 0:
        return
    if len(sections) == 1:
        section = sections[0]
        exec("exec(commands[section])")
    if len(sections) == 2:
        section = sections[0]
        subsection = sections[1]
        exec("exec(commands[section][subsection])")
    if len(sections) == 3:
        section = sections[0]
        subsection = sections[1]
        subsection1 = sections[2]
        exec("exec(commands[section][subsection][subsection1])")
    if len(sections) == 4:
        section = sections[0]
        subsection = sections[1]
        subsection1 = sections[2]
        subsection2 = sections[3]
        exec("exec(commands[section][subsection][subsection1][subsection2])")
    else:return
    
modules = glob.glob(join(dirname(__file__), "**/*.py"),recursive=True)
__all__ = []
for module in modules:
    
    if basename(module) == "__init__.py":
        continue
    module = module.removeprefix(dirname(__file__)).replace("\\",".").removeprefix(".").removesuffix(".py")
    __all__.append(module)
    x = "extensions."+module
    importlib.__import__(x)

print(__all__)
commands = json.load(open("extensions/commands.json"))
#print(commands)


