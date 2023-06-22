import tkinter as tk

#Main page
window = tk.Tk()
window.title("Directus connection")
window.iconbitmap("./icon.ico")

#Username field
label = tk.Label(window, text="username:")
label.pack()

window.mainloop()
