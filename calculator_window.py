import tkinter as tk

def init():
    root = tk.Tk()
    root.title("Program")
    root.geometry("500x500")

    label1 = tk.Label(text="Hello, world!");
    label1.pack()

    root.mainloop()