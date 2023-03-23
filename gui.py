import tkinter
import database
from win32api import GetSystemMetrics

# PostgreSQL database establoshed connection
database_psql = database.DatabaseInteractions()

# Create GUI with widgets and all functionalities (within class created instance)
class GUIComponents():
    def __init__(self) -> None:
        # initialize python gui "tkinter" library instance
        self.main = tkinter.Tk()
        self.chld = None

        # config window
        self._config()

        # spawn default component for window
        self._spawn_default_guicomponents()

        # spawn tkinter GUI window
        self.main.mainloop()

    # Basic GUI spawned window configuration
    def _config(self):
        # add basic title to spawned GUI window 
        self.main.winfo_toplevel().title("Shop interactions program")
        
        # Setup default window size (half desktop width and half desktop height) = default gui window size after minimalize it
        windows_screen_width = int(GetSystemMetrics(0) / 2)
        windows_screen_height = int(GetSystemMetrics(1) / 2)
        width_x_height = f"{windows_screen_width}x{windows_screen_height}"
        self.main.geometry(width_x_height)
        
        # Run GUI window in full screen depth (maximize = zoomed)
        self.main.state("zoomed")

    # Spawn default components and attach options to them for default spawned GUI window 
    def _spawn_default_guicomponents(self):
        # Clear all widgets from main GUI frame
        if self.chld:
            self.chld.destroy()

        # Create child GUI frame
        self.chld = tkinter.Frame(self.main)

        # Add title to GUI
        title = tkinter.Label(self.chld, text="Choose what you'd like to perform")
        title.pack(pady=10)

        # Add buttons to GUI
            # Shop inventory menu button
        button_inv = tkinter.Button(master=self.chld, text="Display shop inventory", command=self.menu_inventory) # crete button object
        button_inv.pack(pady=4) # Add button to parent

            # Add inventory menu button
        button_menuadditions = tkinter.Button(master=self.chld, text="Shop inventory modifications", command=self.menu_additions) # crete button object
        button_menuadditions.pack() # Add button to parent

        self.chld.pack()

    # Create menu with capabilities to add new items to shop inventory
    def menu_additions(self):
        # Destroy previous children widget of main window from GUI
        self.chld.destroy()

        # Create this specific menu widgets
        self.chld = tkinter.Frame(self.main, width=500, height=300)

        i_nameL = tkinter.Label(self.chld, text="Item name")
        i_nameL.pack()

        i_nameI = tkinter.Entry(self.chld)
        i_nameI.pack()

        # Button to add new items
        i_addB = tkinter.Button(self.chld, text="Add new item", command=lambda: database_psql.add_new_item(i_nameI.get()))
        i_addB.pack()
        # Add frame widget to main window GUI
        self.chld.pack()

        # Go back button
        go_back = tkinter.Button(self.chld, text="Go back", command=lambda: self._spawn_default_guicomponents())
        go_back.pack()

    # Displaying items from shop inventory
    def menu_inventory(self):
        # Clear previous widgets from frame for widgets
        self.chld.destroy()

        # Get items names from database or obtain empty list (without any names => should be obtained when shop inventory database is empty)
        (items_names_list, items_ids_list) = database_psql.get_items()
        
        # Creating this menu widgets
        self.chld = tkinter.Frame(width=self.main.winfo_width(), height=self.main.winfo_height())
        self.chld.rowconfigure(0)
        self.chld.rowconfigure(1)
        self.chld.pack()

         # Title for spawning menu
        title = tkinter.Label(self.chld, text="Shop inventory items list:")
        title.grid(row=0, pady=10, sticky=tkinter.W, padx=10)

         # Frame for items
        for_items_frame = tkinter.Frame(master=self.chld)
        for_items_frame.columnconfigure(0, weight=2)
        for_items_frame.columnconfigure(1, weight=1)
        for_items_frame.grid(row=1)

         # Add items to list for items and ability to delete each subsequent item from shop inventory database
        idx = 0
        for item_name in items_names_list:
            # Add item name
            txt_itn = tkinter.Label(for_items_frame, text=item_name, pady=5)
            txt_itn.grid(column=0, row=idx)

            # Button to delete item with this item name
            delete_item = lambda: ""
            btn_delete = tkinter.Button(for_items_frame, text="DELETE", command=delete_item)
            btn_delete.grid(row=idx, column=1, padx=5, pady=5)

            # Increase iterated items counter
            idx+=1

        # Go back button
        go_back = tkinter.Button(self.chld, text="Go back", command=lambda: self._spawn_default_guicomponents())
        go_back.pack(pady=10)



if __name__ == "__main__":
    GUI = GUIComponents()
