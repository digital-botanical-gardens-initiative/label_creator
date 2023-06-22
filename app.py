import tkinter as tk

def store_credentials():
    username = username_entry.get()
    password = password_entry.get()
    number = number_entry.get()
    label_big = parambig.get()
    label_small_1 = paramsmall1.get()
    label_small_2 = paramsmall2.get()
    print(username)
    print(password)
    print(number)
    print(label_big)
    print(label_small_1)
    print(label_small_2)

#Main window
window = tk.Tk()
window.title("Create labels")

#window icon
window.iconbitmap("./icon.ico")

#window minimal size
window.minsize(500, 300)

#Username field
username_label = tk.Label(window, text="Your directus username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

#Password field
password_label = tk.Label(window, text="Your directus password:")
password_label.pack()
password_entry = tk.Entry(window)
password_entry.pack()

#Number of labels
number_label = tk.Label(window, text="Number of labels you want:")
number_label.pack()
number_entry = tk.Entry(window)
number_entry.pack()

#Choose big labels
parambig = tk.IntVar(value=1)
check_big = tk.Checkbutton(window, text="big labels (dbgi_123456)", variable=parambig)
check_big.pack()

#Choose small labels extraction
paramsmall1 = tk.IntVar(value=1)
check_small1 = tk.Checkbutton(window, text="small labels for extraction (dbgi_123456_01)", variable=paramsmall1)
check_small1.pack()

#Choose small labels for injection
paramsmall2 = tk.IntVar(value=1)
check_small2 = tk.Checkbutton(window, text="small labels for injection (dbgi_123456_01_01)", variable=paramsmall2)
check_small2.pack()

#confirm button
confirm_button = tk.Button(window, text = "Confirm", command=store_credentials)
confirm_button.pack()

#Start the window
window.mainloop()