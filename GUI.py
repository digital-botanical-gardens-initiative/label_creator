import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

class MainPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create widgets for the main page
        label = tk.Label(self, text="Create labels")
        label.pack()

        button1 = tk.Button(self, text="Generate labels from scratch", command=self.open_window1)
        button1.pack()

        button2 = tk.Button(self, text="Print already existing labels from a table", command=self.open_window2)
        button2.pack()

    def open_window1(self):
        # Hide the main page and open Window 1
        self.pack_forget()
        window1 = Window1(self.master)
        window1.pack()

    def open_window2(self):
        # Hide the main page and open Window 2
        self.pack_forget()
        window2 = Window2(self.master)
        window2.pack()

class Window1(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.number = tk.IntVar()
        self.location = tk.StringVar()
        self.parambig = tk.IntVar(value=1)
        self.paramsmall1 = tk.IntVar(value=1)
        self.paramsmall2 = tk.IntVar(value=1)

        # Create widgets for the main page
        label = tk.Label(self, text="Generate labels from scratch")
        label.pack()

        # Create text entry fields
        label_username = tk.Label(self, text="Your directus username:")
        label_username.pack()
        entry_username = tk.Entry(self, textvariable=self.username)
        entry_username.pack()

        label_password = tk.Label(self, text="Your directus password:")
        label_password.pack()
        entry_password = tk.Entry(self, textvariable=self.password, show="*")
        entry_password.pack()

        #Number of labels
        number_label = tk.Label(self, text="Number of labels you want:")
        number_label.pack()
        number_entry = tk.Entry(self, textvariable=self.number)
        number_entry.pack()

        #Where the labels will be used
        location_label = tk.Label(self, text="Sampling location:")
        location_label.pack()
        locations = ["JBUF", "JBN", "EMI"]
        dropdown_location = tk.OptionMenu(self, self.location, *locations)
        dropdown_location.pack()

        #Choose big labels
        check_big = tk.Checkbutton(self, text="big labels (dbgi_123456)", variable=self.parambig)
        check_big.pack()

        #Choose small labels extraction
        check_small1 = tk.Checkbutton(self, text="small labels for extraction (dbgi_123456_01)", variable=self.paramsmall1)
        check_small1.pack()

        #Choose small labels for injection
        check_small2 = tk.Checkbutton(self, text="small labels for injection (dbgi_123456_01_01)", variable=self.paramsmall2)
        check_small2.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def show_values(self):
        # Retrieve the entered values
        username = self.username.get()
        os.environ["username"] = username
        password = self.password.get()
        os.environ["password"] = password
        number = self.number.get()
        os.environ["number"] = number
        location = self.location.get()
        os.environ["location"] = location
        parambig1 = self.parambig.get()
        os.environ["parambig1"] = parambig1
        paramsmall11 = self.paramsmall1.get()
        os.environ["paramsmall11"] = paramsmall11
        paramsmall21 = self.paramsmall2.get()
        os.environ["paramsmall12"] = paramsmall21



class Window2(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a variable to store the entered text
        self.number_ext = tk.StringVar()
        self.number_inj = tk.StringVar()
        self.parambig = tk.IntVar()
        self.paramsmall1 = tk.IntVar(value=1)
        self.paramsmall2 = tk.IntVar(value=1)

        # Create widgets for the main page
        label = tk.Label(self, text="Print already existing labels using a table")
        label.pack()

        import_label = tk.Label(self, text="CSV is expected to have a unique column containing codes in format dbgi_123456, without header")
        import_label.pack()
        import_button = tk.Button(self, text="Import your CSV", command=self.import_csv)
        import_button.pack()

        # Create text entry fields
        number_ext_label = tk.Label(self, text="Number of the extraction (let empty if you want big labels):")
        number_ext_label.pack()
        numbers_ext = [str(num).zfill(2) for num in range(1, 100)]
        dropdown_number_ext = tk.OptionMenu(self, self.number_ext, *numbers_ext)
        dropdown_number_ext.pack()

        number_inj_label = tk.Label(self, text="Number of the injection (let empty if you want big labels or extraction labels):")
        number_inj_label.pack()
        numbers_inj = [str(num).zfill(2) for num in range(1, 100)]
        dropdown_number_inj = tk.OptionMenu(self, self.number_inj, *numbers_inj)
        dropdown_number_inj.pack()

        #Choose big labels
        check_big = tk.Checkbutton(self, text="big labels (dbgi_123456)", variable=self.parambig)
        check_big.pack()

        #Choose small labels extraction
        check_small1 = tk.Checkbutton(self, text="small labels for extraction (dbgi_123456_01)", variable=self.paramsmall1)
        check_small1.pack()

        #Choose small labels for injection
        check_small2 = tk.Checkbutton(self, text="small labels for injection (dbgi_123456_01_01)", variable=self.paramsmall2)
        check_small2.pack()

        button_submit = tk.Button(self, text="Submit", command=self.show_values)
        button_submit.pack()

        button_back = tk.Button(self, text="Back to Main Page", command=self.back_to_main)
        button_back.pack()

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            os.environ["VARIABLE_NAME"] = df
    
    def back_to_main(self):
        # Destroy Window 2 and show the main page
        self.destroy()
        main_page.pack()

    def show_values(self):
        # Retrieve the entered values
        number_ext = self.number_ext.get()
        os.environ["VARIABLE_NAME"] = number_ext
        number_inj = self.number_inj.get()
        os.environ["VARIABLE_NAME"] = number_inj
        parambig2 = self.parambig.get()
        os.environ["VARIABLE_NAME"] = parambig2
        paramsmall12 = self.paramsmall1.get()
        os.environ["VARIABLE_NAME"] = paramsmall12
        paramsmall22 = self.paramsmall2.get()
        os.environ["VARIABLE_NAME"] = paramsmall22

# Create the main window
window = tk.Tk()
window.title("DBGI labels creator")
window.minsize(500, 300)
window.iconbitmap("./icon.ico")

# Create the main page
main_page = MainPage(window)
main_page.pack()

window.mainloop()