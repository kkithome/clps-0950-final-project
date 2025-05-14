import tkinter as tk #python graphical user interfaces
from tkinter import ttk #themed tkinter that is more modern
from tkinter import messagebox
from tkinter import filedialog #shows popup alert boxes
from tkcalendar import Calendar 
from datetime import datetime
from PIL import Image, ImageTk
import json
import os


#Loading past user data
USER_FILE = "users.json"
SETTINGS_FILE = "users_settings.json"
ASSIGNMENTS_FILE = "assignments.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def load_settings():
    try: 
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return {}
    
def load_assignments():
    try: 
        with open(ASSIGNMENTS_FILE, "r") as f:
            return json.load(f)
    except FileExistsError:
        with open(ASSIGNMENTS_FILE, "w") as f: 
            json.dump({}, f)
        return {}
    except json.JSONDecodeError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f: 
        json.dump(users, f, indent=4)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def save_assignments(assignments):
    with open(ASSIGNMENTS_FILE, "w") as f:
        json.dump(assignments, f, indent=4)


users = load_users()
settings = load_settings()
assignments = load_assignments()

#Creates an Admin page -> we need to add page for this
def is_admin(username):
    return users.get(username, {}).get("role") == "admin" #looks up given username and if user exists checks if they are admin
    
def admin_login():
    #create pop up for admin login
    login_window = tk.Toplevel()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

#add a label and in put field for the admin udername
    tk.Label(login_window, text="Admin Username").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

#add a label and password field (hides input with *)
    tk.Label(login_window, text="admin Password").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

#Verifying admin's credentials
    def verify_admin():
        username = entry_username.get()
        password = entry_password.get()

        if username in users and users[username]["password"] == password and is_admin(username):
            messagebox.showinfo("Success", "Admin verification successful!")
            login_window.destroy()
            delete_user_prompt()
        else:
            messagebox.showerror("Error", "Invalid Admin credentials")
     #Adds a login button that runs the verify_admin function when clicked       
    tk.Button(login_window, text="Login", command=verify_admin).pack(pady=10)

def delete_user_prompt():
        #create a popup window for deleting a user
        delete_window = tk.Toplevel()
        delete_window.title("Delete User")
        delete_window.geometry("300x200")

        #add label and input for username to delete
        tk.Label(delete_window, text="Enter Username to Delete").pack(pady=5)
        entry_username = tk.Entry(delete_window)
        entry_username.pack(pady=5)

        def delete_user():
            global users
            username = entry_username.get()
            if username in users:
                confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{username}'? This action cannot be undone.")
                if confirm:
                    del users[username]
                    save_users(users)
                    messagebox.showinfo("Success", f"User '{username}' has been deleted successfully.")
                    delete_window.destroy()
                else:
                    messagebox.showinfo("Cancelled", "User deletion cancelled.")
            else:
                messagebox.showerror("Error", "Username not found.")
            
        # Add a "Delete" button that runs delete_user when clicked
        tk.Button(delete_window, text="Delete", command=delete_user).pack(pady=10)

# Assignment data model
class Assignment:
    def __init__(self, title, due_date, class_name, assignment_type, completed=False, priority=False):
        self.title = title
        self.due_date = due_date 
        self.class_name = class_name
        self.assignment_type = assignment_type
        self.completed = completed
        self.priority = priority  # add priority to make it go 'to do' list 

    def add_to_user(self, username):
        assignments = load_assignments()
        if username not in assignments:
            assignments[username] = {"assignments": {}}
        assignments[username]["assignments"][self.title] = self.__dict__
        save_assignments(assignments)

    def delete_assignments(username, title):
        assignments = load_assignments()
        if username in assignments and title in assignments[username]["assignments"]:
            del assignments[username]["assignments"][title]
            save_assignments(assignments)
            return True
        return False
    
    def update_assignments(username, title, updated_data):
        assignments = load_assignments()
        if username in assignments and title in assignments[username]["assignments"]:
            assignments[username]["assignments"][title].update(updated_data)
            save_assignments(assignments)
            return True
        return False



class AssignmentTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("800x600")
        self.configure(bg="white")

        self.current_user = None
        self.assignments = []

        self.nav_bar = tk.Frame(self, bg="#eee", height=50)

        buttons = [
            ("Home", self.show_home),
            ("Assignments", self.show_table),
            ("Calendar", self.show_calendar),
            ("To-Do", self.show_todo),
            ("Progress", self.show_progress),
            ("Settings", self.show_settings),
        ]

        for name, command in buttons:
            tk.Button(self.nav_bar, text=name, command=command, bg="#ddd").pack(side='left', padx=5, pady=10)

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for PageClass in (LoginPage, HomePage, TablePage, CalendarPage, ToDoPage, ProgressPage, SettingsPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_login()

        tk.Button(self.nav_bar, text="Logout", command=self.logout).pack(side="right", padx=10, pady=5)

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logged Out", "You have been logged out")
        self.show_login()


    def show_nav_bar(self):
        self.nav_bar.pack(fill='x')

    def hide_nav_bar(self):
        self.nav_bar.pack_forget()

    def show_page(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def show_home(self): self.show_page(HomePage)
    def show_table(self): self.show_page(TablePage)
    def show_calendar(self): self.show_page(CalendarPage)
    def show_todo(self): self.show_page(ToDoPage)
    def show_progress(self): self.show_page(ProgressPage)
    def show_settings(self): self.show_page(SettingsPage)
    def show_login(self):
        self.hide_nav_bar()
        self.show_page(LoginPage)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="Username: ", bg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Password: ", bg="white").grid(row=1, column=0, padx=10, pady=10)

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Sign In", command=self.signin).grid(row=2, column=0, pady=10, padx=10)
        tk.Button(self, text="Sign Up", command=lambda: SignUpPage(self)).grid(row=2, column=1, pady=10, padx=10)
        tk.Button(self, text="Forgot Password?", command=self.forgot_password).grid(row=2, column=2, pady=10, padx=10)
        

    def forgot_password(self):
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
        username = self.entry_username.get()
        password = self.entry_password.get()
        users = load_users()

        if username in users and users[username]["password"] == password:
            self.controller.current_user = users[username]
            self.controller.current_user["username"] = username
            messagebox.showinfo("Success", "Login successful!")
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

        tk.Button(self, text="Register", command=self.signup).pack(pady=10)

    def signup(self):
        users = load_users()
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not all([first_name, last_name, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields must be filled.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        users[username] = {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }

        settings[username] = {
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "profile_picture": "",
            "default_view": ""
        }


        save_users(users)
        messagebox.showinfo("Success", "Account created successfully!")
        self.destroy()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Welcome to the Assignment Tracker!", font=("Helvetica", 20), bg="white").pack(pady=50)

class TablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Top toolbar
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="x", pady=(20, 0))

        label = tk.Label(top_frame, text="Assignment Table", font=("Helvetica", 20), bg="white")
        label.pack(side="left", padx=20)

        edit_button = tk.Button(top_frame, text="Edit Selected", bg="#f0ad4e", fg="black", command=self.edit_selected)
        edit_button.pack(side="right", padx=10)

        delete_button = tk.Button(top_frame, text="Delete Selected", bg="red", fg="black", command=self.delete_selected)
        delete_button.pack(side="right", padx=10)

        plus_button = tk.Button(top_frame, text="+", font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="green",
                                command=self.open_add_assignment_popup)
        plus_button.pack(side="right", padx=10)

        # Assignment Review
        self.tree = ttk.Treeview(
            self,
            columns=("Priority", "Title", "Due Date in YYYY-MM-DD format", "Class", "Type", "Completed"),
            show="headings"
        )
        self.tree.heading("Priority", text="★")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due Date in YYYY-MM-DD format", text="Due Date")
        self.tree.heading("Class", text="Class Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Completed", text="Completed")

        self.tree.pack(fill="both", expand=True, pady=10)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for a in self.controller.assignments:
            self.tree.insert("", "end", values=(
                "★" if a.priority else "",
                a.title,
                a.due_date,
                a.class_name,
                a.assignment_type,
                "Yes" if a.completed else "No"
            ))

    def open_add_assignment_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Assignment")
        popup.geometry("300x350")
        popup.grab_set()

        fields = ["Title", "Due Date in YYYY-MM-DD format", "Class Name", "Type"]
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
            username = self.controller.current_user["username"]
            new_assignment = Assignment(
                entries["Title"].get(),
                entries["Due Date in YYYY-MM-DD format"].get(),
                entries["Class Name"].get(),
                entries["Type"].get(),
                completed=completed_var.get(),
                priority=priority_var.get()
            )
            due_date = entries["Due Date in YYYY-MM-DD format"].get()

            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter Due date in YYYY-MM-DD format.")
                return
            
            new_assignment.add_to_user(username)
            self.refresh()
            popup.destroy()

        tk.Button(popup, text="Add", command=save, bg="#4CAF50", fg="black").pack(pady=10)

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an assignment to delete.")
            return

        for item in selected_items:
            values = self.tree.item(item, "values")
            title = values[1]

            if Assignment.delete_assignments(self.controller.current_user["username"], title):
                self.tree.delete(item)
            #due_date = values[2]
            #self.controller.assignments = [
            #    a for a in self.controller.assignments
            #    if not (a.title == title and a.due_date == due_date)
            #]
            #self.tree.delete(item)

        messagebox.showinfo("Deleted", "Selected assignment(s) deleted.")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an assignment to edit.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        title = values[1]
        due_date = values[2]

        popup = tk.Toplevel(self)
        popup.title("Edit Assignment")
        popup.geometry("300x350")
        popup.grab_set()

        fields = ["Title", "Due Date in YYYY-MM-DD format", "Class Name", "Type"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(popup, text=field).pack(pady=(10 if i == 0 else 5, 0))
            entry = tk.Entry(popup)
            entry.insert(0, values[i + 1])  # shift index: skip priority
            entry.pack()
            entries[field] = entry

        completed_var = tk.BooleanVar(value=(values[5] == "Yes"))
        priority_var = tk.BooleanVar(value=(values[0] == "★"))
        tk.Checkbutton(popup, text="Completed", variable=completed_var).pack(pady=5)
        tk.Checkbutton(popup, text="Mark as Priority (★)", variable=priority_var).pack(pady=5)

        def save():
            # Remove old
            self.controller.assignments = [
                a for a in self.controller.assignments
                if not (a.title == title and a.due_date == due_date)
            ]

            updated = Assignment(
                entries["Title"].get(),
                entries["Due Date in YYYY-MM-DD format"].get(),
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

        # Event binding
        self.calendar.bind("<<CalendarSelected>>", self.show_assignments_for_selected_date)

    def refresh(self):
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
        total = len(self.controller.assignments)
        completed = sum(1 for a in self.controller.assignments if a.completed)

        if total == 0:
            percent = 0
        else:
            percent = (completed / total) * 100

        self.progress_label.config(text=f"Completed {completed} out of {total} assignments ({percent:.1f}%)")
        self.progress_bar["value"] = percent


class SettingsPage(tk.Frame):
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

        tk.Button(self, text="Save Settings", command=self.save_settings).pack(pady=10)

    def upload_image(self):
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