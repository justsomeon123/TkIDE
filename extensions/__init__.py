from os.path import dirname, basename, isfile, join
import glob,json
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
print(__all__)
bootstrap = json.load(open(glob.glob(join(dirname(__file__), "bootstrap.json"))[0]))
print(bootstrap)
def LoadExtensionPt(section,subsection):
    exec("exec(bootstrap[section][subsection])")

