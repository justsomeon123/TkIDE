import tkinter as tk
from tkterminal import Terminal

root = tk.Tk()
terminal = Terminal(pady=5, padx=5)
terminal.shell = True
terminal.pack(expand=True, fill='both')
b1 = tk.Button(
    root, text="Uninstall tkterminal", fg="Black",
    command=lambda: terminal.run_command('pip uninstall tkterminal', 'y'))
b1.pack()
root.mainloop()