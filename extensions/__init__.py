from os.path import dirname, basename, isfile, join
import glob,json
def LoadExtensionPt(sections:list):
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
    
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
print(__all__)
commands = json.load(open("extensions/commands.json"))
print(commands)


