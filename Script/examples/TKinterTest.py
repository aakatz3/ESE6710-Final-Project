import tkinter.messagebox as mb
import tkinter as tk
from tkinter import ttk

# Make sure to include these globals
LOADS = ['50Ω Load', 'RB058LAM100TF', 'STPS360AF']
FETS = ['IGB070S10S1', 'IGB110S101', 'BSC065N06LS5', 'BSC096N10LS5', 'BSC160N15NS5']
# slice list to include only ones actually soldered
FETS = [FETS[1], FETS[3]]

# Provided by ChatGPT. Not proud of that, but it was the simplest option.
# Modified by me
def get_configuration():
    root = tk.Tk()
    root.withdraw()

    result = None

    dialog = tk.Toplevel(root)
    dialog.title("Select an option")
    dialog.resizable(False, False)

    tk.Label(dialog, text='FET Selection').pack(padx=10, pady=5)

    combo = ttk.Combobox(dialog, values=FETS, state="readonly")
    combo.pack(padx=10, pady=5)

    tk.Label(dialog, text='Load Selection').pack(padx=10, pady=5)

    combo2 = ttk.Combobox(dialog, values=LOADS, state="readonly")
    combo2.pack(padx=10, pady=5)

    def submit():
        if (combo.get() != '') & (combo2.get() != ''):
            nonlocal result
            result = (combo.get(), combo2.get())
            dialog.destroy()
        else:
            mb.showerror(
                message='Please select a value for the FET and the load',
                parent=dialog)

    ttk.Button(dialog, text="OK", command=submit).pack(pady=10)

    dialog.grab_set()
    dialog.wait_window()

    root.destroy()
    if result == None:
        raise ValueError('No selection made in configuration dialog')
    return result

print(get_configuration())
