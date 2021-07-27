import cx_Freeze
import sys
import os

base = None
if sys.platform == 'win32':
    base="Win32GUI"

# search python -> open file location -> Again open file location -> tcl -> select tcl8.6 and tk8.6 one by one -> copy path
os.environ["TCL_LIBRARY"] = r"C:\Users\sudha\AppData\Local\Programs\Python\Python38-32\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\sudha\AppData\Local\Programs\Python\Python38-32\tcl\tk8.6"

executables = [cx_Freeze.Executable("login.py", base=base, icon="billing.ico")]

cx_Freeze.setup(
    name = "Billing System",
    options = {"build_exe": {"packages":["tkinter","os","sys"], "include_files":["tcl86t.dll","tk86t.dll","billing.ico","bills"]}},
    version = "1.00",
    description = "Billing System for managing small businesses | Developed by Sudhansu Dwivedi",
    executables = executables

)