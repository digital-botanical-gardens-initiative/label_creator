import requests
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import process
import pandas as pd

list_uni = requests.get("http://universities.hipolabs.com/search?")
data = list_uni.json()

dataf = pd.DataFrame(data=data, columns=['alpha_two_code', 'web_pages', 'country', 'state-province', 'name', 'domains'])

unique_countries = dataf['country'].drop_duplicates().reset_index(drop=True)
sorted_countries = pd.DataFrame(unique_countries).sort_values('country').reset_index(drop=True)
sorted_countries

# Global variables
suggestions = []

def update_suggestions():
    global suggestions
    selected_item = combobox.get()
    if selected_item:
        # Use fuzzywuzzy to get the best matches
        matches = process.extract(selected_item, sorted_countries['country'].tolist(), limit=7)
        suggestions = [match for match, _ in matches if _ >= 50]  # Adjust threshold as needed

        # Update the listbox with suggestions
        listbox.delete(0, tk.END)
        for suggestion in suggestions:
            listbox.insert(tk.END, suggestion)

def on_key_release(event):
    # Start or restart the suggestion update
    root.after_cancel(update_suggestions)  # Cancel previous update_suggestions call
    root.after(50, update_suggestions)  # Start update_suggestions

def on_listbox_select(event):
    # Set the selected suggestion in the combobox
    selected_index = listbox.curselection()
    if selected_index:
        selected_suggestion = listbox.get(selected_index)
        combobox.set(selected_suggestion)
        combobox.icursor(tk.END)
        print(selected_suggestion)
        listbox.forget()  # Hide the listbox when an element is selected

def on_combobox_selected(event):
    # Perform actions when an item is selected
    print(f"Selected: {combobox.get()}")
    listbox.forget()  # Hide the listbox when an element is selected
    # You can add more actions here if needed

# Main Tkinter window
root = tk.Tk()
root.title("Fuzzy Matching Suggestions")

# Create a Combobox
combobox = ttk.Combobox(root)
combobox.pack()

# Create a Listbox for suggestions
listbox = tk.Listbox(root, height=7, width=50, font=('Helvetica', 10))  # Adjust height and font size as needed
listbox.pack()


# Bind the event handlers
combobox.bind("<KeyRelease>", on_key_release)
combobox.bind("<<ComboboxSelected>>", on_combobox_selected)
listbox.bind("<<ListboxSelect>>", on_listbox_select)

root.mainloop()
