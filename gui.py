import tkinter.messagebox as tkmb
import tkinter
import database
from hashlib import shake_256
from win32api import GetSystemMetrics

# PostgreSQL database establoshed connection
database_psql = database.DatabaseInteractions()

# Save logged user under below variable (this commented variable)
logged_user = () # 1st = login = user name, 2nd = password = password shake_256 signature

# Create GUI with widgets and all functionalities (within class created instance)
class GUIComponents():
    def __init__(self) -> None:
        # initialize python gui "tkinter" library instance
        self.main = tkinter.Tk()
        self.chld = None

        # config window
        self._config()

        # spawn "user login panel"
        self.login_panel()

        # spawn default component for window
        # self._spawn_default_guicomponents()

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

    # Adding go back button to Frame GUI tkinter widget with each another tkinter widgets 
    def _go_back(self, row_id, colspan=1) -> None:
        go_back = tkinter.Button(self.chld, text="Go back", command=lambda: self._spawn_default_guicomponents())
        go_back.grid(column=0, row=row_id, pady=10, columnspan=colspan)

    # Login user to allow he/she to access, to another application GUI features
    def login_panel(self):
        # For mailfunctions handling: Destroy previous children widget of main window from GUI
        if self.chld:
            self.chld.destroy()
        
        # Main feature = creating login panel is performed under this comment = description
        self.chld = tkinter.Frame(self.main)
        self.chld.rowconfigure(0)
        self.chld.rowconfigure(1)
        self.chld.rowconfigure(2)
        self.chld.rowconfigure(3)
        self.chld.columnconfigure(0)
        self.chld.columnconfigure(1)
        self.chld.pack()

         # Create this menu action description (Label widget with text 'Login yourself first')
        d_login = tkinter.Label(self.chld, text="Login yourself first")
        d_login.grid(columnspan=2, row=0)

         # Create entry for login from user (capture user login)
        d_login = tkinter.Label(self.chld, text="Login")
        d_login.grid(column=0, row=1, pady=3)
        
        i_login = tkinter.Entry(self.chld)
        i_login.grid(column=1, row=1, pady=3, padx=3)

         # Create entry for user password (capture user password)
        d_password = tkinter.Label(self.chld, text="Password")
        d_password.grid(column=0, row=2, pady=3)
        
        i_password = tkinter.Entry(self.chld)
        i_password.grid(column=1, row=2, pady=3, padx=3)

         # Login user button (user must click it to login yourself using passed login and password to above input=Entry widgets fields)
          # Function performing when user click on button with "Login" text
        def perform_login_operation():
            user_login = i_login.get()
            user_password = i_password.get()
            print(user_login, user_password)

            if len(user_login) > 0 and len(user_password) > 0:
                user_password_db = database_psql.get_user_password(user_login)

                # When user doesn't exist "user_password_db" variable will be equal to empty string
                if len(user_password_db) == 0:
                    tkmb.showerror("Incorrect login", "You pass incorrect login")
                else:
                    # Login user
                     # Create shake_256 signature from entered by user password to compare it in equality site with password obtained from database
                    base = shake_256()
                    base.update(bytes(user_password, "utf-8"))
                    user_password_sign = base.hexdigest(64)

                    print(user_password_sign)

                     # Compare signature with signature password from database and when is equal login user
                    if user_password_sign == user_password_db:
                        # Login user when passwords are equal to each other
                        logged_user = (user_login, user_password_sign)

                        # Display alert that user has been successfully logged into application
                        tkmb.showinfo("Success", "You has been successfully logged!")
                        
                        # Display to user default user components
                        self._spawn_default_guicomponents()
                    else:
                        # Show that user pass incorrect passwor
                        tkmb.showerror("Error", "You pass incorrect password!")
            else:
                tkmb.showerror("Error", "'Your login' and 'Your password' fields cannot be empty'")
         
        b_login = tkinter.Button(self.chld, text="Login", command=perform_login_operation)
        b_login.grid(row=3, columnspan=2, pady=10)

    # Create menu with capabilities to add new items to shop inventory
    def menu_additions(self):
        # Destroy previous children widget of main window from GUI
        self.chld.destroy()

        # Create this specific menu widgets
        self.chld = tkinter.Frame(self.main, width=500, height=300)
        self.chld.rowconfigure(0)
        self.chld.rowconfigure(1)
        self.chld.rowconfigure(2)
        self.chld.rowconfigure(3)
        self.chld.columnconfigure(0)
        self.chld.columnconfigure(1)
        self.chld.pack()

         # Name for whole interface action (for which action this interface will be creating)
        i_nameL = tkinter.Label(self.chld, text="Adding new items to shop inventory:")
        i_nameL.grid(column=0, row=0, pady=20)

         # Name for Entry widget action
        i_nameL = tkinter.Label(self.chld, text="Item name")
        i_nameL.grid(column=0, row=1, pady=3)

         # Adding entry for widget (tkinter) for capture user input
        i_nameI = tkinter.Entry(self.chld)
        i_nameI.grid(column=1, row=1, padx=3, pady=3)

         # Button to add new items
        i_addB = tkinter.Button(self.chld, text="Add new item", command=lambda: database_psql.add_new_item(i_nameI.get()))
        i_addB.grid(row=2, columnspan=2, pady=2)
        
         # Go back button
        self._go_back(row_id=3, colspan=2)

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
             # Function which wraps identifier of clicked element
            def wrapper_delete_item(idx):
                # Obtain id of clicked element button
                element_id_to_delete: str = items_ids_list[idx]

                # Return to button command param function which deletes this specific element from database
                return lambda: delete_element(element_id_to_delete)
            
             # Function to delete elements from database with displaying changes within GUI 
            def delete_element(id: str):
                # Delete item from database
                database_psql.delete_item(id)

                # Show information box alert to user using GUI
                tkmb.showinfo("Success", "This element has been deleted from shop inventory items database!")

                # Refresh inventory items list by destroy it and re-create again
                self.menu_inventory()

            btn_delete = tkinter.Button(for_items_frame, text="DELETE", command=wrapper_delete_item(idx))
            btn_delete.grid(row=idx, column=1, padx=5, pady=5)

            # Increase iterated items counter
            idx+=1

        # Go back button
        self._go_back(idx+1)



if __name__ == "__main__":
    GUI = GUIComponents()
