import tkinter as tk
import re

class calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Program")
        self.root.geometry("500x500")

        self.icon = tk.PhotoImage(file='icons/logotype.png')
        self.root.iconphoto(False, self.icon)

        self.text1 = tk.Text(height=1, width=50, state="disabled")
        self.text1.pack(pady=20)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        symbols = ["7", "8", "9", "+", 
                   "4", "5", "6", "-", 
                   "1", "2", "3", "*", 
                   "0", "C", "/"]
        
        for i, s in enumerate(symbols):
            row = i // 4
            col = i % 4
            
            if s == "C":
                btn = tk.Button(buttons_frame, text=s, width=6, height=2, command=self.clear_text)
            else:
                btn = tk.Button(buttons_frame, text=s, width=6, height=2,
                              command=lambda ss = s: self.press_button(ss))
            btn.grid(row=row, column=col, padx=2, pady=2)
            
        self.root.bind('<Return>', self.result)

        self.root.mainloop()

    def press_button(self, text: str):
        self.text1.config(state='normal')
        self.text1.insert(tk.END, text)
        self.text1.config(state='disabled')
    def clear_text(self):
        self.text1.config(state='normal')
        self.text1.delete("1.0", tk.END)
        self.text1.config(state='disabled')
    def result(self, event=None):
        try:
            expr = self.text1.get("1.0", tk.END).strip()
            self.clear_text()
            self.text1.config(state='normal')
            
            if not expr:
                self.text1.insert(tk.END, "Insert an expression")
                return
            if not self.is_safe_expression(expr):
                self.text1.insert(tk.END, "It's the wrong expression")
                return
            
            res = eval(expr)
            self.text1.insert(tk.END, res)
        except ZeroDivisionError:
            self.text1.insert(tk.END, "Divide by zero")
        except SyntaxError:
            self.text1.insert(tk.END, "Syntax error")
        except NameError:
            self.text1.insert(tk.END, "Wrong symbols")
        except Exception as e:
            self.text1.insert(tk.END, "Error")
        finally:
            self.text1.config(state='disabled')
    
    def is_safe_expression(self, expr: str):
        pattern: str = r'^-?\d+([\+\-\*\\]\d+)*$' # The special pattern for math expressions
        return bool(re.match(pattern, expr))