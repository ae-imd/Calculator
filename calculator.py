import tkinter as tk
import re
import POLIZ

class calculator:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Program")
        self.__root.geometry("500x600")
        self.__root.configure(bg="black")

        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=1)
        self.__root.rowconfigure(0, weight=1)

        self.__initialize_icon(self.__root)

        self.__main_frame = tk.Frame(master=self.__root)
        self.__main_frame.grid(row=0, column=1, padx=50, sticky='w')

        self.__ns_frame = tk.Frame(master=self.__root, bg='black')
        self.__ns_frame.grid(row=0, column=0, sticky='e')

        self.__buttons_frame = tk.Frame(master=self.__root, bg='black')
        self.__buttons_frame.grid(row=1, column=1)

        self.__current_panel = None
        self.__root_panel = None
        self.__log_panel = None
        self.__pow_panel = None
        self.__syntax_panel = None
        self.__bitwise_panel = None

        self.__initialize_field(self.__main_frame)
        self.__initialize_number_systems(self.__ns_frame)
        self.__initialize_buttons(self.__buttons_frame)

        self.__current_text = ""
        self.__result = None

    def __initialize_buttons(self, frame):
        grid = [['<--', '-->', 'B', 'C', '='],
                ['7', '8', '9', '/', 'SYNTAX'],
                ['6', '5', '4', '*', 'ROOT'],
                ['3', '2', '1', '+', 'LOG'],
                ['0', '+/-', 'SKIP', '-', 'POW'],
                ['E', 'PI', 'PHI', 'BITWISE']]
        
        number_style = {"bg": "#333333", "fg": "white", "font": ("Arial", 12)}
        operation_style = {"bg": "#ff0000", "fg": "white", "font": ("Arial", 12)}
        special_style = {"bg": "#00ff2f", "fg": "black", "font": ("Arial", 10)}
        function_style = {"bg": "#ff9500", "fg": "white", "font": ("Arial", 10)}

        for row_idx, row in enumerate(grid):
            for col_idx, button_text in enumerate(row):
                if button_text in ['=', '+', '-', '*', '/', '+/-', ',']:
                    style = operation_style
                elif button_text in ['<--', '-->', 'B', 'C']:
                    style = special_style
                elif button_text in ['ROOT', 'LOG', 'POW', 'SYNTAX', 'BITWISE']:
                    style = function_style
                else:
                    style = number_style
                
                button = tk.Button(master=frame, text=button_text,
                                   width=6, height=2, **style, relief="flat")
                
                if button_text in ['ROOT', 'LOG', 'POW', 'SYNTAX', 'BITWISE']:
                    button.config(command=lambda text=button_text: self.__on_function_button_click(text))
                else:
                    button.config(command=lambda text=button_text: self.__on_button_click(text))

                button.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")
    
        for i in range(6):
            frame.rowconfigure(i, weight=1)
        for i in range(5):
            frame.columnconfigure(i, weight=1)

    def __create_function_panels(self):
        self.__root_panel = tk.Frame(self.__buttons_frame, bg="#444444", relief="raised", bd=2)
        root_functions = ["SQRT", "CBRT", "ROOT"]
        for i, func in enumerate(root_functions):
            btn = tk.Button(self.__root_panel, text=func, width=8, height=1,
                           bg="#ff9500", fg="white", font=("Arial", 9),
                           command=lambda f=func: self.__insert_function(f))
            btn.pack(padx=2, pady=1, fill="x")

        self.__log_panel = tk.Frame(self.__buttons_frame, bg="#444444", relief="raised", bd=2)
        log_functions = ["LOG", "LN", "LOG2"]
        for i, func in enumerate(log_functions):
            btn = tk.Button(self.__log_panel, text=func, width=8, height=1,
                           bg="#ff9500", fg="white", font=("Arial", 9),
                           command=lambda f=func: self.__insert_function(f))
            btn.pack(padx=2, pady=1, fill="x")

        self.__pow_panel = tk.Frame(self.__buttons_frame, bg="#444444", relief="raised", bd=2)
        pow_functions = ["^", "SQR", "CBR", "EXP"]
        for i, func in enumerate(pow_functions):
            btn = tk.Button(self.__pow_panel, text=func, width=8, height=1,
                           bg="#ff9500", fg="white", font=("Arial", 9),
                           command=lambda f=func: self.__insert_function(f))
            btn.pack(padx=2, pady=1, fill="x")

        self.__syntax_panel = tk.Frame(self.__buttons_frame, bg="#444444", relief="raised", bd=2)
        syntax_functions = ['(', ')', '.', ',']
        for i, func in enumerate(syntax_functions):
            btn = tk.Button(self.__syntax_panel, text=func, width=4, height=1,
                        bg="#9b59b6", fg="white", font=("Arial", 9),
                        command=lambda f=func: self.__insert_function(f))
            btn.pack(padx=1, pady=1)

        self.__bitwise_panel = tk.Frame(self.__buttons_frame, bg="#444444", relief="raised", bd=2)
        bitwise_functions = ["DIV", "MOD", "LSH", "RSH", "ROL", "ROR", "AND", "XOR", "OR"]
        for i, func in enumerate(bitwise_functions):
            btn = tk.Button(self.__bitwise_panel, text=func, width=6, height=1,
                           bg="#ff9500", fg="white", font=("Arial", 9),
                           command=lambda f=func: self.__insert_function(f))
            btn.pack(padx=1, pady=1)

    def __show_function_panel(self, function_type):
        self.__hide_function_panel()
        
        if function_type == "ROOT":
            self.__current_panel = self.__root_panel
        elif function_type == "LOG":
            self.__current_panel = self.__log_panel
        elif function_type == "POW":
            self.__current_panel = self.__pow_panel
        elif function_type == "SYNTAX":
            self.__current_panel = self.__syntax_panel
        elif function_type == "BITWISE":
            self.__current_panel = self.__bitwise_panel

        if self.__current_panel:
            self.__current_panel.place(x=200, y=100)
            self.__current_panel.lift()

    def __hide_function_panel(self):
        if self.__current_panel:
            self.__current_panel.place_forget()
            self.__current_panel = None

    def __on_function_button_click(self, func_type):
        if self.__current_panel is not None:
            current_panel_type = None
            if self.__current_panel == self.__root_panel:
                current_panel_type = "ROOT"
            elif self.__current_panel == self.__log_panel:
                current_panel_type = "LOG"
            elif self.__current_panel == self.__pow_panel:
                current_panel_type = "POW"
            elif self.__current_panel == self.__syntax_panel:
                current_panel_type = "SYNTAX"
            elif self.__current_panel == self.__bitwise_panel:
                current_panel_type = "BITWISE"

            if current_panel_type == func_type:
                self.__hide_function_panel()
                return

        self.__show_function_panel(func_type)

    def __insert_function(self, func: str) -> None:
        if func in ["SQRT", "CBRT", "LN", "LOG2", "SIN", "COS", "TAN", "COT", 
                   "ASIN", "ACOS", "ATAN", "ACOT", "FLOOR", "CEILING", "SQR",
                   "CBR", "EXP", "ROOT", "LOG", "DIV", "MOD", "LSH", "RSH", "ROL",
                   "ROR", "AND", "XOR", "OR"]:
            self.__current_text += f"{func}("
        elif func == "^":
            self.__current_text += "^"
        elif func in ['E', 'PI', 'PHI']:
            self.__current_text += func
        elif func in ['(', ')', ',', '.']:
            self.__current_text += func
        
        self.__update_field(self.__current_text)
        self.__hide_function_panel()

    def __initialize_field(self, frame):
        self.__field = tk.Label(master=frame, text="_____________",
                         bg="#000000", fg="#00ff00", width=15, height=5)
        self.__field.pack(expand=True)

    def __initialize_number_systems(self, frame):
        titles = ["BIN", "OCT", "DEC", "HEX"]
        header = tk.Label(frame, text="Number systems", 
                         font=("Arial", 12, "bold"),
                         bg="black", fg="white")
        header.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        self.__value_labels = []

        for i, title in enumerate(titles):
            title_label = tk.Label(master=frame, text=title, width=6,
                                 font=("Arial", 10, "bold"),
                                 bg="black", fg="#00e1ff")
            value_label = tk.Label(master=frame, text="", width=12,
                                 font=("Courier", 10),
                                 bg="#333333", fg="#00e1ff", relief="sunken")
            
            title_label.grid(row=i+1, column=0, padx=5, pady=8, sticky='w')
            value_label.grid(row=i+1, column=1, padx=5, pady=8, sticky='w')
            self.__value_labels.append(value_label)

    def __initialize_icon(self, root):
        try:
            icon = tk.PhotoImage(file='icons/logotype.png')
            root.iconphoto(False, icon)
        except:
            pass

    def run(self):
        self.__create_function_panels()
        self.__root.mainloop()

    def __on_button_click(self, text: str):
        if text == 'C':
            self.__current_text = ""
            self.__result = None
        elif text == 'B':
            self.__current_text = self.__current_text[:-1]
        elif text == '=':
            self.__calculate()
        elif text == '+/-':
            if self.__current_text and self.__current_text[0] == '-':
                self.__current_text = self.__current_text[1:]
            elif self.__current_text:
                self.__current_text = '-' + self.__current_text
        elif text in ['E', 'PI', 'PHI']:
            self.__current_text += text
        else:
            self.__current_text += text

        self.__update_field(self.__current_text)

    def __calculate(self):
        try:
            if self.__current_text:
                self.__result = POLIZ.calculate_infix_expression(self.__current_text)
                is_integer = self.__result == int(self.__result)

                self.__current_text = str(self.__result) if not is_integer else str(int(self.__result))
        except:
            self.__current_text = "Error"
            self.__result = None
        finally:
            self.__update_field(self.__current_text)
            self.__update_number_systems()

    def __update_field(self, text: str):
        self.__field.config(text=text)
    
    def __update_number_systems(self):
        try:
            if self.__current_text and self.__current_text not in ["", "Error"] and self.__result is not None:
                is_integer = self.__result == int(self.__result)

                if self.__result < 0 or not is_integer:
                    values = ["ND", "ND",  "ND", "ND"]
                else:
                    values = [bin(int(self.__result))[2:],
                        oct(int(self.__result))[2:],
                        str(int(self.__result)),
                        hex(int(self.__result))[2:].upper()]
                for i, value_label in enumerate(self.__value_labels):
                        value_label.config(text=values[i])
            else:
                for value_label in self.__value_labels:
                    value_label.config(text="")
        except:
            for value_label in self.__value_labels:
                value_label.config(text="")