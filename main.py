import tkinter as tk #python graphical user interfaces
from tkinter import ttk #themed tkinter that is more modern
from tkinter import messagebox
from tkinter import filedialog #shows popup alert boxes
from tkcalendar import Calendar 
from datetime import datetime
from PIL import Image, ImageTk
import random
import json
import os


#Loading past user data
USER_FILE = "users.json"
SETTINGS_FILE = "users_settings.json"
ASSIGNMENTS_FILE = "assignments.json"

def load_users():
    # Loads the current user data in the users.json file
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def load_settings(): 
    # Loads the current user settings data in the users_settings.json file
    try: 
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return {}
    
def load_assignments():
    # Loads the current assignment data in the assignments.json file
    try: 
        with open(ASSIGNMENTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    # saves any user changes to the users.json file
    with open(USER_FILE, "w") as f: 
        json.dump(users, f, indent=4)

def save_settings(settings):
    # saves any setiings changes to the settings.json file
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def save_assignments(assignments):
    # saves any assignment changes to the assignments.json file
    try:
        with open(ASSIGNMENTS_FILE, "w") as f:
            json.dump(assignments, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save assignment: {e}")


users = load_users()
settings = load_settings()
assignments = load_assignments()


def is_admin(username):
    # checks the users role to see if they are an admin
    return users.get(username, {}).get("role").lower() == "admin" #looks up given username and if user exists checks if they are admin

# Assignment Dataclass
class Assignment:
    def __init__(self, title, due_date, class_name, assignment_type, completed=False, priority=False):
        # Defines the fields for the Assignment class
        self.title = title
        self.due_date = due_date 
        self.class_name = class_name
        self.assignment_type = assignment_type
        self.completed = completed
        self.priority = priority  # add priority to make it go 'to do' list 

    def add_to_user(self, username):
        # saves an assignment to the user's dictionary in the users.json file
        assignments = load_assignments()
        if username not in assignments:
            assignments[username] = {"assignments": {}}
        assignments[username]["assignments"][self.title] = self.__dict__
        save_assignments(assignments)
        messagebox.showinfo(f"Assignment '{self.title}' saved for user '{username}'.")

    def delete_assignments(username, title):
        # ensures that when an assignment is deleted, it is also deleted from the assignment.json file
        assignments = load_assignments()
        if username in assignments and title in assignments[username]["assignments"]:
            del assignments[username]["assignments"][title]
            save_assignments(assignments)
            return True
        return False
    



class AssignmentTrackerApp(tk.Tk):
    # main application controller
    def __init__(self):
        # intilizes the window for the Assignment Tracker
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("800x600")
        self.configure(bg="white")

        # initializes the current user and role for use on other pages
        self.current_user = None
        self.current_user_role = None
        self.assignments = []
        self.class_colors = {}

        self.nav_bar = tk.Frame(self, bg="#eee", height=50)
        self.nav_bar.pack(fill="x", side="top")
        
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for PageClass in (LoginPage, HomePage, TablePage, CalendarPage, ToDoPage, ProgressPage, SettingsPage, UsersPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        
        self.show_login() # When the application is first ran, the user is shown the login page

    def create_nav_bar(self):
            #creates the navigation bar based on the user's role
            for widget in self.nav_bar.winfo_children():
                widget.destroy() 
            buttons = [
                ("Home", self.show_home),
                ("Assignments", self.show_table),
                ("Calendar", self.show_calendar),
                ("To-Do", self.show_todo),
                ("Progress", self.show_progress),
                ("Settings", self.show_settings),
            ]

            if self.current_user_role.lower() == "admin":
                buttons.append(("Users", self.show_users))

            for name, command in buttons:
                tk.Button(self.nav_bar, text=name, command=command, bg="#ddd").pack(side='left', padx=5, pady=10)

            tk.Button(self.nav_bar, text="Logout", command=self.logout).pack(side="right", padx=10, pady=5)

    def load_user_assignments(self, username):
        # loads all of the assignments sotred under the user in the assignment's page to be populated
        all_assignments = load_assignments()
        user_assignments = all_assignments.get(username, {}).get("assignments", {})

        self.assignments = [
            Assignment(
                title=a["title"],
                due_date=a["due_date"],
                class_name=a["class_name"],
                assignment_type=a["assignment_type"],
                completed=a.get("completed", False),
                priority=a.get("priority", False)
            )
            for a in user_assignments.values()
        ]

    def logout(self):
        # logs the user out and shows the login page
        self.current_user = None
        self.current_user_role = None
        messagebox.showinfo("Logged Out", "You have been logged out")
        self.show_login()


    def show_nav_bar(self):
        # displays the navigation bar
        self.nav_bar.pack(fill='x')

    def hide_nav_bar(self):
        # hides the navigation bar
        self.nav_bar.pack_forget()

    def show_page(self, page_class):
        # used to show a specific page of the assignment tracker
        frame = self.frames[page_class.__name__]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    
    # The functions below are used to make navigating between the various pages of the tracker much easier
    def show_home(self): self.show_page(HomePage)
    def show_users(self): self.show_page(UsersPage)
    def show_table(self): self.show_page(TablePage)
    def show_calendar(self): self.show_page(CalendarPage)
    def show_todo(self): self.show_page(ToDoPage)
    def show_progress(self): self.show_page(ProgressPage)
    def show_settings(self): self.show_page(SettingsPage)
    def show_login(self):
        self.hide_nav_bar()
        self.show_page(LoginPage)

class LoginPage(tk.Frame):
    # Class that creates the LoginPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="Username: ", bg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Password: ", bg="white").grid(row=1, column=0, padx=10, pady=10)

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Sign In", command=self.signin).grid(row=2, column=0, pady=10, padx=10) # Sign In Button
        tk.Button(self, text="Sign Up", command=lambda: SignUpPage(self)).grid(row=2, column=1, pady=10, padx=10) # Sign Up Button
        tk.Button(self, text="Forgot Password?", command=self.forgot_password).grid(row=2, column=2, pady=10, padx=10) # Forgot Password Button
        

    def forgot_password(self):
        # Function that allows the user to reset their password
        reset_window = tk.Toplevel()
        reset_window.title("Reset Password")
        reset_window.geometry("300x300")

        tk.Label(reset_window, text="Enter Username:", bg="white").pack(pady=5)
        entry_username = tk.Entry(reset_window)
        entry_username.pack(pady=5)

        tk.Label(reset_window, text="Enter New Password:", bg="white").pack(pady=5)
        entry_new_password = tk.Entry(reset_window, show="*")
        entry_new_password.pack(pady=5)

        tk.Label(reset_window, text="Confirm New Password:", bg="white").pack(pady=5)
        entry_confirmation = tk.Entry(reset_window, show="*")
        entry_confirmation.pack(pady=5)

        def reset():
            # this funtion actually replaces the password in the user.json and the users.settings.json files
            username = entry_username.get()
            new_password = entry_new_password.get()
            confirm_password = entry_confirmation.get()
            users = load_users()
            settings = load_settings()

            if username in users:
                if new_password == confirm_password:
                    users[username]["password"] = new_password
                    settings[username]["password"] = new_password

                    save_users(users)
                    save_settings(settings)

                    messagebox.showinfo("Success", "Password updated successfully")
                    reset_window.destroy()

                else:
                    messagebox.showerror("Error", "Passwords do not match. Please try again")
            else:
                messagebox.showerror("Error", "Username not found.")

        tk.Button(reset_window, text="Reset", command=reset).pack(pady=10).grid(row=0, column=1)

   

    def signin(self):
        # responsible for signing the user in by checking the username and password stored in the user.json file
        username = self.entry_username.get()
        password = self.entry_password.get()
        users = load_users()

        if username in users and users[username]["password"] == password:
            self.controller.current_user = users[username]
            self.controller.current_user["username"] = username
            messagebox.showinfo("Success", "Login successful!")

            self.controller.load_user_assignments(username)

            self.controller.current_user_role = users[username]["role"]
            self.controller.create_nav_bar()
            self.controller.show_nav_bar()


            default_view = settings.get(username, {}).get("default_view", "Home")
            page_mapping = {
                "Home": HomePage, 
                "Table": TablePage,
                "Calendar": CalendarPage,
                "Todo": ToDoPage,
                "Progress": ProgressPage,
                
            }
            self.controller.show_page(page_mapping.get(default_view))

        else:
            messagebox.showerror("Error", "Invalid credentials.")


class SignUpPage(tk.Toplevel):
    # Class that creates the SignUpPage and houses all of the function related to the page
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sign Up")
        self.geometry("350x400")

        tk.Label(self, text="First Name:").pack(pady=5)
        self.entry_first_name = tk.Entry(self)
        self.entry_first_name.pack(pady=5)

        tk.Label(self, text="Last Name:").pack(pady=5)
        self.entry_last_name = tk.Entry(self)
        self.entry_last_name.pack(pady=5)

        tk.Label(self, text="Username:").pack(pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        tk.Label(self, text="Password").pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        tk.Label(self, text="Confirm Password").pack(pady=5)
        self.entry_confirm_password = tk.Entry(self, show="*")
        self.entry_confirm_password.pack(pady=5)

        tk.Label(self, text="Select Role:").pack(pady=5)
        self.role = tk.StringVar(value="student")
        role_options = ["student", "admin"]
        self.role_menu = ttk.Combobox(self, textvariable=self.role, values=role_options)
        self.role_menu.pack(pady=5)

        tk.Button(self, text="Register", command=self.signup).pack(pady=10)

    def signup(self):
        # responsible for adding the new user to the users.json file
        users = load_users()
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()
        role = self.role.get()

        if not all([first_name, last_name, username, password, confirm_password]):
            # ensures that new users fill out all of the required fields on the sign up page
            messagebox.showerror("Error", "All fields must be filled.")
            return
        if password != confirm_password: # ensures that the passwords match each other
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if username in users: # ensures that the username is not already in use
            messagebox.showerror("Error", "Username already exists.")
            return

        # adds the new user to the users.json file
        users[username] = {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": role
        }

        # adds the new user to the user_settings.json
        settings[username] = {
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "profile_picture": "",
            "default_view": ""
        }

        save_users(users)
        save_settings(users)
        messagebox.showinfo("Success", "Account created successfully!") # shows users a confirmation that their user profile was created
        self.destroy() # closes the sign up window

class HomePage(tk.Frame):
    # Class that creates the HomePage 
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Welcome to the Assignment Tracker!", font=("Helvetica", 20), bg="white").pack(pady=50)

class UsersPage(tk.Frame):
    # Class that creates the UsersPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="User Management", font=("Helvetica", 16), bg="white").pack(pady=10) # page title

        # creates a dropdown menu and populates it with the list of current users
        tk.Label(self, text="Select a User to Delete:", bg="white").pack(pady=10)
        self.user_dropdown = ttk.Combobox(self)
        self.user_dropdown.pack(pady=10)
        self.load_users_for_dropdown()

        tk.Button(self, text="Delete User", command=self.delete_user_prompt, bg="red").pack(pady=10) # delete user button


        if not self.controller.current_user_role == "admin":
            messagebox.showerror("Access Denied", "Admins Only")
            return
        

        
    def load_users_for_dropdown(self):
        # Populates the dropdown with the users' usernames
        users = load_users()
        self.user_dropdown["values"] = list(users.keys())
        if users:
            self.user_dropdown.current(0)

    def delete_user_prompt(self):
        # Confirm and delete selected user
        username = self.user_dropdown.get()

        if not username: 
            messagebox.showerror("Error", "No user selected.")
            return
            
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{username}'? This action cannot be undone.")
        if confirm:
            users = load_users()

            # deletes users from users.json file
            if username in users:
                del users[username]
                save_users(users)

            # deletes users from assignments.json file
            assignments = load_assignments()
            if username in assignments:
                del assignments[username]
                save_assignments(assignments)

            # deletes users from users_settings.json file
            settings = load_settings()
            if username in settings:
                del settings[username]
                save_settings(settings)

                

            messagebox.showinfo("Success", f"User '{username}' has been deleted successfully.")
            self.load_users_for_dropdown()

        else:
            messagebox.showinfo("Cancelled", "User deletion cancelled.")

        # Add a "Delete" button that runs delete_user when clicked
        tk.Button(self, text="Delete", command=self.delete_user_prompt).pack(pady=10)

        


class TablePage(tk.Frame):
    # Class that creates the TablePage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Top toolbar
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="x", pady=(20, 0))

        label = tk.Label(top_frame, text="Assignment Table", font=("Helvetica", 20), bg="white")
        label.pack(side="left", padx=20)

        # Creates Edit Button
        edit_button = tk.Button(top_frame, text="Edit Selected", bg="#f0ad4e", fg="black", command=self.edit_selected)
        edit_button.pack(side="right", padx=10)

        # Creates the delete button
        delete_button = tk.Button(top_frame, text="Delete Selected", bg="red", fg="black", command=self.delete_selected)
        delete_button.pack(side="right", padx=10)

        # Creates the plus button
        plus_button = tk.Button(top_frame, text="+", font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="green",
                                command=self.open_add_assignment_popup)
        plus_button.pack(side="right", padx=10)

        # Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("Priority", "Title", "Due Date", "Class", "Type", "Completed"),
            show="headings"
        )
        self.tree.heading("Priority", text="★")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Class", text="Class Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Completed", text="Completed")

        self.tree.pack(fill="both", expand=True, pady=10)

    def refresh(self):
        # updates the table page
        self.tree.delete(*self.tree.get_children())

        for a in self.controller.assignments:
            # Assign color if new class
            if a.class_name not in self.controller.class_colors:
                self.controller.class_colors[a.class_name] = self.generate_random_color()

            row_color = self.controller.class_colors[a.class_name]

        # populates the table with assignments that were previously added from the assignments.json file
        for a in self.controller.assignments:
            self.tree.insert("", "end", values=(
                "★" if a.priority else "",
            a.title,
            a.due_date,
            a.class_name,
            a.assignment_type,
            "Yes" if a.completed else "No"
            ))


            self.tree.tag_configure(a.class_name, background=row_color)

    def generate_random_color(self):
        # generates a random color to color code the different classes
        return "#{:06x}".format(random.randint(0x444444, 0xDDDDDD))

    def open_add_assignment_popup(self):
        # creates the popup window that shows when a user wants to add an assignment
        popup = tk.Toplevel(self)
        popup.title("Add Assignment")
        popup.geometry("300x350")
        popup.grab_set()

        fields = ["Title", "Due Date", "Class Name", "Type"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(popup, text=field).pack(pady=(10 if i == 0 else 5, 0))
            entry = tk.Entry(popup)
            entry.pack()
            entries[field] = entry

        completed_var = tk.BooleanVar()
        priority_var = tk.BooleanVar()
        tk.Checkbutton(popup, text="Completed", variable=completed_var).pack(pady=5)
        tk.Checkbutton(popup, text="Mark as Priority (★)", variable=priority_var).pack(pady=5)

        def save():
            # adds the assignement to both the user dictionary in the assignment file and to the ongoing list of assignments
            username = self.controller.current_user["username"]
            new_assignment = Assignment(
                entries["Title"].get(),
                entries["Due Date"].get(),
                entries["Class Name"].get(),
                entries["Type"].get(),
                completed=completed_var.get(),
                priority=priority_var.get()
            )
            self.controller.assignments.append(new_assignment)
            new_assignment.add_to_user(username)
            self.refresh()
            popup.destroy()

        tk.Button(popup, text="Add", command=save, bg="#4CAF50", fg="black").pack(pady=10) # creates the add button that users click to run the above functionality

    def delete_selected(self):
        # allows users to deleted the selected assignments from both the table view and the assignments.json
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an assignment to delete.")
            return
        
        assignments = load_assignments()

        for item in selected_items:
            values = self.tree.item(item, "values")
            title, due_date = values[1], values[2]

            self.controller.assignments = [
                a for a in self.controller.assignments
                if not (a.title == title and a.due_date == due_date)
            ]

            for username, user_data in assignments.items():
                user_assignments = user_data.get("assignments", {})
                for assignment_title, details in list(user_assignments.items()):
                    if details.get("title") == title and details.get("due_date") == due_date:
                        del user_assignments[assignment_title]
                        save_assignments(assignments)

            self.tree.delete(item)


        messagebox.showinfo("Deleted", "Selected assignment(s) deleted.")

    def edit_selected(self):
        # edits the assignments in the table only
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an assignment to edit.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        title, due_date = values[1], values[2]

        popup = tk.Toplevel(self)
        popup.title("Edit Assignment")
        popup.geometry("300x350")
        popup.grab_set()

        fields = ["Title", "Due Date", "Class Name", "Type"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(popup, text=field).pack(pady=(10 if i == 0 else 5, 0))
            entry = tk.Entry(popup)
            entry.insert(0, values[i + 1])  # skip priority
            entry.pack()
            entries[field] = entry

        completed_var = tk.BooleanVar(value=(values[5] == "Yes"))
        priority_var = tk.BooleanVar(value=(values[0] == "★"))
        tk.Checkbutton(popup, text="Completed", variable=completed_var).pack(pady=5)
        tk.Checkbutton(popup, text="Mark as Priority (★)", variable=priority_var).pack(pady=5)

        def save():
            # saves the assignments to the controller list, not to the assignments.json file
            self.controller.assignments = [
                a for a in self.controller.assignments
                if not (a.title == title and a.due_date == due_date)
            ]

            updated = Assignment(
                entries["Title"].get(),
                entries["Due Date"].get(),
                entries["Class Name"].get(),
                entries["Type"].get(),
                completed=completed_var.get(),
                priority=priority_var.get()
            )

            self.controller.assignments.append(updated)
            self.refresh()
            popup.destroy()

        tk.Button(popup, text="Save", command=save, bg="#f0ad4e", fg="white").pack(pady=10)


class CalendarPage(tk.Frame):
    # Class that creates the CalendarPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Title
        tk.Label(self, text="Assignment Calendar", font=("Courier New", 20), bg="white").pack(pady=10)

        # Outer horizontal frame
        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: Calendar
        self.calendar = Calendar(
            content_frame,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            showweeknumbers=False,
            firstweekday="sunday",
            background="white",
            foreground="black",
            headersbackground="#eeeeee",
            headersforeground="black",
            weekendbackground="#f9f9f9",
            weekendforeground="gray",
            selectbackground="#4CAF50",
            selectforeground="white"
        )
        self.calendar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 20))

        # Right column with two vertical sections
        top_right = tk.Frame(content_frame, bg="white", height=100)
        bottom_right = tk.Frame(content_frame, bg="white")
        
        top_right.grid(row=0, column=1, sticky="nsew")
        bottom_right.grid(row=1, column=1, sticky="nsew")

        # Label + Listbox in the bottom-right quadrant
        tk.Label(bottom_right, text="Assignments for Selected Date:", font=("Helvetica", 14), bg="white").pack(anchor="w")

        self.assignment_listbox = tk.Listbox(bottom_right, width=50)
        self.assignment_listbox.pack(fill="both", expand=True, pady=5)

        # Grid weight configuration
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

        # Event binding?
        self.calendar.bind("<<CalendarSelected>>", self.show_assignments_for_selected_date)

    def refresh(self):
        # updates the calendar upon reload
        self.assignment_listbox.delete(0, tk.END)
        self.calendar.calevent_remove('all')

        for a in self.controller.assignments:

            
            try:
                due_date = datetime.strptime(a.due_date, "%Y-%m-%d")
                self.calendar.calevent_create(due_date, f"{a.title}", 'due')
            except ValueError:
                continue

        self.calendar.tag_config('due', background='red', foreground='white')

    def show_assignments_for_selected_date(self, event):
        # filters the assignments so that only the ones due on a given date are shown
        selected_date = self.calendar.get_date()
        self.assignment_listbox.delete(0, tk.END)
        found = False

        for a in self.controller.assignments:
            if a.due_date == selected_date:
                self.assignment_listbox.insert(tk.END, f"{a.title} - {a.class_name} - {a.assignment_type}")
                found = True

        if not found:
            self.assignment_listbox.insert(tk.END, "No assignments due on this date.")

class ToDoPage(tk.Frame):
    # Class that creates the ToDoPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="To-Do List", font=("Helvetica", 20), bg="white").pack(pady=10)

        self.todo_listbox = tk.Listbox(self, width=80, height=20)
        self.todo_listbox.pack(padx=20, pady=10)

        self.refresh()

    def refresh(self):
        self.todo_listbox.delete(0, tk.END)

        # Separate starred and non-starred assignments
        starred = []
        regular = []

        for a in self.controller.assignments:
            item_str = f"★ {a.title}" if getattr(a, "starred", False) else a.title
            display = f"{item_str} - {a.class_name} - {a.due_date}"
            if getattr(a, "starred", False):
                starred.append(display)
            else:
                regular.append(display)

        for item in starred + regular:
            self.todo_listbox.insert(tk.END, item)

class ProgressPage(tk.Frame):
    # Class that creates the ProgressPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="Progress Tracker", font=("Helvetica", 20), bg="white").pack(pady=10)

        self.progress_label = tk.Label(self, text="", font=("Helvetica", 14), bg="white")
        self.progress_label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.refresh()

    def refresh(self):
        # updates the progress bar if needed upon reload
        total = len(self.controller.assignments)
        completed = sum(1 for a in self.controller.assignments if a.completed)

        if total == 0:
            percent = 0
        else:
            percent = (completed / total) * 100

        self.progress_label.config(text=f"Completed {completed} out of {total} assignments ({percent:.1f}%)")
        self.progress_bar["value"] = percent


class SettingsPage(tk.Frame):
    # Class that creates the SettingsPage and houses all of the function related to the page
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Settings Page", font=("Helvetica", 20), bg="white").pack(pady=20)

        # User Profile Section
        tk.Label(self, text="First Name:", bg="white").pack(pady=5)
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack(pady=5)

        tk.Label(self, text="Last Name:", bg="white").pack(pady=5)
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack(pady=5)

        tk.Label(self, text="Profile Picture:", bg="white").pack(pady=5)
        self.image_label = tk.Label(self, bg="white")
        self.image_label.pack(pady=5)
        tk.Button(self, text="Upload Image", command=self.upload_image).pack(pady=5)

        # Default View Selection
        tk.Label(self, text="Default View:", bg="white").pack(pady=5)
        self.default_view = tk.StringVar()
        self.default_view.set("Home")
        self.view_options = ["Table", "Calendar",  "Todo", "Progress"]
        self.view_menu = ttk.Combobox(self, textvariable=self.default_view, values=self.view_options)
        self.view_menu.pack(pady=5)


        tk.Button(self, text="Save Settings", command=self.save_settings).pack(pady=10) # creates the button used to save the settings

    def upload_image(self):
        # allows the user to select a file on the computer as their profile page
        file_path = filedialog.askopenfilename()
        
        if not file_path:
            return
        
        self.image_label.config(text=f"Selected: {os.path.basename(file_path)}")
        self.profile_picture = file_path

        img = Image.open(file_path)
        img = img.resize((100,100))
        img_tk = ImageTk.PhotoImage(img)

        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def save_settings(self):
        # saves the settings preferences to the settings.json file
        settings = {
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "profile_picture": getattr(self, "profile_picture", ""),
            "default_view": self.default_view.get()
        }

        with open("user_settings.json", "w") as file:
            json.dump(settings, file)
        
        messagebox.showinfo("Success", "Settings have been saved succesfully.")

    def load_settings(self):
        # preloads the setttings for each user when they login
        if os.path.exists("user_settings.json"):
            with open("user_settings.json", "r") as file:
                settings = json.load(file)
                self.first_name_entry.insert(0, settings.get("first_name", ""))
                self.last_name_entry.insert(0, settings.get("last_name", ""))
                self.default_view.set(settings.get("default_view", "Home"))

                if settings.get("profile_picture"):
                    self.image_label.config(text=f"Selected: {os.path.basename(settings['profile_picture'])}")
    

if __name__ == "__main__":
    app = AssignmentTrackerApp()
    app.mainloop()