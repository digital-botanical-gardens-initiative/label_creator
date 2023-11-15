import requests
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import process
import pandas as pd
import os
import Processing_site

def main():

    username = os.environ.get("username")
    password = os.environ.get("password")

    list_uni = requests.get("http://universities.hipolabs.com/search?")
    data = list_uni.json()

    dataf = pd.DataFrame(data=data, columns=['alpha_two_code', 'web_pages', 'country', 'state-province', 'name', 'domains'])

    unique_countries = dataf['country'].drop_duplicates().reset_index(drop=True)
    sorted_countries = pd.DataFrame(unique_countries).sort_values('country').reset_index(drop=True)

    # Global variables
    selected_country = None
    selected_university = None
    country_suggestions = []
    university_suggestions = []


    def update_country_suggestions():
        global selected_country, country_suggestions
        selected_item = combobox_country.get()
        if selected_item:
            # Use fuzzywuzzy to get the best matches for countries
            matches = process.extract(selected_item, sorted_countries['country'].tolist(), limit=3)
            country_suggestions = [match for match, _ in matches if _ >= 50]  # Adjust threshold as needed

            # Update the listbox with country suggestions
            listbox_country.delete(0, tk.END)
            for suggestion in country_suggestions:
                listbox_country.insert(tk.END, suggestion)

    def update_university_suggestions():
        global selected_country, selected_university, university_suggestions
        if selected_country:
            # Filter universities based on selected country
            country_filtered_universities = dataf[dataf['country'] == selected_country]
            os.environ['country'] = str(selected_country)
            selected_item = combobox_university.get()
            if selected_item:
                # Use fuzzywuzzy to get the best matches for universities in the selected country
                matches = process.extract(selected_item, country_filtered_universities['name'].tolist(), limit=7)
                university_suggestions = [match for match, _ in matches if _ >= 50]  # Adjust threshold as needed

                # Update the listbox with university suggestions
                listbox_university.delete(0, tk.END)
                for suggestion in university_suggestions:
                    listbox_university.insert(tk.END, suggestion)

    def on_country_select(event):
        global selected_country
        selected_index = listbox_country.curselection()
        if selected_index:
            selected_suggestion = listbox_country.get(selected_index)
            combobox_country.delete(0, tk.END)
            combobox_country.insert(tk.END, selected_suggestion)
            selected_country = selected_suggestion
            update_university_suggestions()  # Update university suggestions when country is selected

    def on_university_select(event):
        global selected_university
        selected_index = listbox_university.curselection()
        if selected_index:
            selected_suggestion = listbox_university.get(selected_index)
            combobox_university.delete(0, tk.END)
            combobox_university.insert(tk.END, selected_suggestion)
            selected_university = selected_suggestion
            # Perform actions when a university is selected, you can add more actions here if needed
            listbox_country.forget()
            listbox_university.forget()
            #lauch()
            os.environ['username'] = str(username)
            os.environ['password'] = str(password)
            os.environ['site'] = str(selected_university)
            root.destroy()
            Processing_site.main()
    
    #def lauch():
        

    # Main Tkinter window
    root = tk.Tk()
    root.title("Fuzzy Matching Suggestions")

    # Create a Country Combobox
    combobox_country = ttk.Combobox(root)
    combobox_country.pack()

    # Create a Listbox for country suggestions
    listbox_country = tk.Listbox(root, height=3, width=50, font=('Helvetica', 10))  # Adjust height and font size as needed
    listbox_country.pack()

    # Create a University Combobox
    combobox_university = ttk.Combobox(root)
    combobox_university.pack()

    # Create a Listbox for university suggestions
    listbox_university = tk.Listbox(root, height=7, width=50, font=('Helvetica', 10))  # Adjust height and font size as needed
    listbox_university.pack()

    # Bind the event handlers for country and university selection
    listbox_country.bind("<<ListboxSelect>>", on_country_select)
    listbox_university.bind("<<ListboxSelect>>", on_university_select)

    # Bind event handlers for updating suggestions
    combobox_country.bind("<KeyRelease>", lambda event: root.after(50, update_country_suggestions))
    combobox_university.bind("<KeyRelease>", lambda event: root.after(50, update_university_suggestions))

    root.mainloop()

if __name__ == "__main__":
    main()