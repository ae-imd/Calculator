import tkinter as tk
import re
import number_systems as ns

class calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Program")
        self.root.geometry("500x500")

        icon = tk.PhotoImage(file='icons/logotype.png')
        self.root.iconphoto(False, icon)

        self.text1 = tk.Text(height=1, width=50, state="disabled")
        self.text1.pack(pady=20)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        # ns - number systems
        ns_frame = tk.Frame(main_frame)
        ns_frame.pack(side=tk.LEFT, padx=10)

        ns_label = tk.Label(ns_frame, text="Number Systems", font=("Arial", 10, "bold"))
        ns_label.grid(row=0, column=0)

        self.ns_text = tk.Text(ns_frame, height=6, width=15, 
                                        state="disabled", font=("Consolas", 9))
        self.ns_text.grid(row=1, column=0)

        # ao = aritmetic operations
        ao_frame = tk.Frame(main_frame)
        ao_frame.pack(side=tk.RIGHT, padx=10)

        ao_label = tk.Label(ao_frame, text="Arithmetic operations", font=("Arial", 10, "bold"))
        ao_label.grid(row=0, column=0, columnspan=4)

        symbols = ["7", "8", "9", "+", 
                   "4", "5", "6", "-", 
                   "1", "2", "3", "*", 
                   "0", "C", " ", "/"]
        
        for i, s in enumerate(symbols):
            row = i // 4 + 1
            col = i % 4
            
            if s == "C":
                btn = tk.Button(ao_frame, text=s, width=6, height=2, command=self.clear_text)
            else:
                btn = tk.Button(ao_frame, text=s, width=6, height=2,
                              command=lambda ss = s: self.press_button(ss))
            btn.grid(row=row, column=col, padx=2, pady=2)
            
        self.root.bind('<Return>', self.calculate)

        self.last_result = None
    def run(self):
        self.root.mainloop()

    def press_button(self, text: str):
        self.text1.config(state='normal')
        self.text1.insert(tk.END, text)
        self.text1.config(state='disabled')
    def clear_text(self):
        self.text1.config(state='normal')
        self.text1.delete("1.0", tk.END)
        self.text1.config(state='disabled')

        self.ns_text.config(state='normal')
        self.ns_text.delete("1.0", tk.END)
        self.ns_text.config(state='disabled')

        self.last_result = None

    def calculate(self, event=None):
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
            self.last_result = res

            self.show_all_systems()
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
    
    def show_all_systems(self):
        """Показывает представление числа во всех системах счисления"""
        if self.last_result is not None:
            try:
                decimal = str(self.last_result)
                binary = ns.dec_to_bin(int(self.last_result))
                octal = ns.dec_to_oct(int(self.last_result))
                hexadecimal = ns.dec_to_hex(int(self.last_result))
                
                display_text = f"DEC: {decimal}\nBIN: {binary}\nOCT: {octal}\nHEX: {hexadecimal}"
                self.update_ns_text(display_text)
                
            except ValueError as e:
                self.update_ns_text(f"Error:\n{str(e)}")
        else:
            self.update_ns_text("No result\nCalculate first!")

    def clear_ns_text(self):
        """Очищает поле систем счисления"""
        self.update_ns_text("")

    def update_ns_text(self, text: str):
        self.ns_text.config(state='normal')
        self.ns_text.delete("1.0", tk.END)
        self.ns_text.insert("1.0", text)
        self.ns_text.config(state='disabled')
    