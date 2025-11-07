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

        self.__buttons_frame= tk.Frame(master=self.__root, bg='black')
        self.__buttons_frame.grid(row=1, column=1)

        self.__initialize_field(self.__main_frame)
        self.__initialize_number_systems(self.__ns_frame)
        self.__initialize_buttons(self.__buttons_frame)

        self.__current_text = ""
        self.__result = None

    def __initialize_buttons(self, frame):
        grid = [['<--', '-->', 'B', 'C', '='],
                ['7', '8', '9', '/'],
                ['6', '5', '4', '*'],
                ['3', '2', '1', '+'],
                ['0', '+/-', '.', '-']]
        
        number_style = {"bg": "#333333", "fg": "white", "font": ("Arial", 12)}
        operation_style = {"bg": "#ff0000", "fg": "white", "font": ("Arial", 12)}
        special_style = {"bg": "#00ff2f", "fg": "black", "font": ("Arial", 10)}

        for row_idx, row in enumerate(grid):
            for col_idx, button_text in enumerate(row):
                if button_text in ['=', '+', '-', '*', '/', '+/-', '.']:
                    style = operation_style
                elif button_text in ['<--', '-->', 'B', 'C']:
                    style = special_style
                else:
                    style = number_style
                
                button = tk.Button(master=frame, text=button_text,
                                   width=6, height=2, **style, relief="flat",
                                   command=lambda text=button_text: self.__on_button_click(text))
                button.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")
    
        for i in range(5):
            frame.columnconfigure(i, weight=1)
        for i in range(5):
            frame.rowconfigure(i, weight=1)
    
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
        icon = tk.PhotoImage(file='icons/logotype.png')
        root.iconphoto(False, icon)

    def run(self):
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
        else:
            self.__current_text += text

        self.__update_field(self.__current_text)

    def __calculate(self):
        try:
            if self.__current_text:
                self.__result = POLIZ.calculate_infix_expression(self.__current_text)
                is_integer = self.__result == int(self.__result) # Checking for an integer value

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
                is_integer = self.__result == int(self.__result) # Checking for an integer value

                if self.__result < 0 or not is_integer:
                    values = [
                        "ND",
                        "ND", 
                        str(int(self.__result)),
                        "ND"
                    ]
                else:
                    values = [
                        bin(int(self.__result))[2:], # BIN
                        oct(int(self.__result))[2:], # OCT  
                        str(int(self.__result)), # DEC
                        hex(int(self.__result))[2:].upper() # HEX
                    ]
                for i, value_label in enumerate(self.__value_labels):
                        value_label.config(text=values[i])
            else:
                for value_label in self.__value_labels:
                    value_label.config(text="")
        except:
            for value_label in self.__value_labels:
                value_label.config(text="")