#!/usr/bin/env python3
# coding: utf-8
# Version 1.1

import os
import sys
import numpy as np
import pandas as pd
import tkinter as tk
from neo.io import AxonIO
from tkinter import filedialog, messagebox


class getparams(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
        self.wm_title("Export Parameters")

        self.button = tk.Button(self, text="Initialize", command=self.on_button)

        self.lab0 = tk.Label(self,text="Format:")
        self.form = tk.StringVar()
        self.form.set('TSV')
        self.form0 = tk.Radiobutton(self, text="TSV", variable=self.form, value='TSV')
        self.form1 = tk.Radiobutton(self, text="CSV", variable=self.form, value='CSV')
        self.form0.select()

        self.lab1 = tk.Label(self,text="Compression:")
        self.comp = tk.IntVar()
        self.comp.set(0)
        self.comp0 = tk.Radiobutton(self, text="None", variable=self.comp, value=0)
        self.comp1 = tk.Radiobutton(self, text="GZIP", variable=self.comp, value=1)
        self.comp0.select()
 
        self.lab2 = tk.Label(self,text="Decimal Separator:")
        self.sep = tk.Entry(self,width=5)
        self.sep.insert(0,".")

        self.dvar = tk.StringVar()
        self.lab3 = tk.Label(self,text="Decimals:")
        self.decims = tk.Spinbox(self, values=(0,1,2,3,4,5,6,'All'), textvariable=self.dvar,width=4)
        self.decims.insert('end','All')
        self.dvar.set(6)

        self.lab0.grid(row=0,column=0, sticky='W')
        self.form0.grid(row=0,column=1)
        self.form1.grid(row=0,column=2)

        self.lab1.grid(row=1,column=0, sticky='W')
        self.comp0.grid(row=1,column=1)
        self.comp1.grid(row=1,column=2)

        self.lab2.grid(row=2,column=0, sticky='W')
        self.sep.grid(row=2,column=1,columnspan=2)

        self.lab3.grid(row=3,column=0, sticky='W')
        self.decims.grid(row=3,column=1,columnspan=2)

        self.button.grid(row=4,column=0, columnspan=3)

        self.lift()

    def on_button(self):
        global decims, form, comp, dsep
        decims = self.decims.get()
        form = self.form.get().lower()
        comp = self.comp.get()
        dsep = self.sep.get()
        if form=="csv" and dsep==",":
            messagebox.showwarning("Warning", "Using comma as a separator in a Comma Separated Values file generates ambiguity.")
        else:
            self.destroy()


root = tk.Tk()
root.withdraw()
file_paths=filedialog.askopenfilenames(title="Files to Convert",
           filetypes =(("ABF Files", "*.abf"),("All Files","*.*")))
root.destroy()

file_names=[".".join(file_path.split(".")[:-1]) for file_path in file_paths]

getparams().mainloop()

try:
    sep = '\t' if form=="tsv" else ','
except NameError: #window closed without a selection
    sys.exit()

for f in range(len(file_paths)):
    fileout = file_names[f] + '.' + form
    reader = AxonIO(filename = file_paths[f])
    blks = reader.read(cascade=True,lazy=False)
    seg = blks[0].segments
    f=np.transpose(np.array([seg[0].analogsignals])[0])[0]
    df=pd.DataFrame(f)

    if decims=="All":
        if comp==0:
            df.to_csv(fileout,sep=sep,decimal=dsep)
        else:
            df.to_csv(fileout,sep=sep,decimal=dsep,compression='gzip')

    else:
        dformat = '%.'+decims+'f'
        if comp==0:
            df.to_csv(fileout,float_format=dformat,sep=sep,decimal=dsep)
        else:
            df.to_csv(fileout,float_format=dformat,sep=sep,decimal=dsep,compression='gzip')

    if comp:
        os.rename(fileout,fileout + '.gzip')

fini = tk.Tk()
fini.withdraw()
messagebox.showinfo("ABF Convert", "Finished Converting files.")
