from contextlib import contextmanager
import os,importlib

@contextmanager
def changedir(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

