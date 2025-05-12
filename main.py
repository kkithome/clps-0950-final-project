import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
import os

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

class Assignment:
    def __init__(self, title, due_date, class_name, assignment_type, completed=False):
        self.title = title
        self.due_date = due_date
        self.class_name = class_name
        self.assignment_type = assignment_type
        self.completed = completed

class AssignmentTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("800x600")
        self.configure(bg="white")

        self.current_user = None
        self.assignments = []

        # Create nav_bar but do not pack
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

    def show_nav_bar(self):
        self.nav_bar.pack(fill='x')

    def hide_nav_bar(self):
        self.nav_bar.pack_forget()

    def show_page(self, page_class):
        frame = self.frames[page_class.__name__]
        if hasattr(frame, 'refresh'):
            frame.refresh()
        frame.tkraise()

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

    def signin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        users = load_users()

        if username in users and users[username]["password"] == password:
            self.controller.current_user = users[username]
            self.controller.current_user["username"] = username
            messagebox.showinfo("Success", "Login successful!")
            self.controller.show_nav_bar()
            self.controller.show_home()
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
        tk.Label(self, text="Assignment Table", font=("Helvetica", 20), bg="white").pack(pady=20)

class CalendarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Calendar Page", font=("Helvetica", 20), bg="white").pack(pady=20)

class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="To-Do Page", font=("Helvetica", 20), bg="white").pack(pady=20)

class ProgressPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Progress Page", font=("Helvetica", 20), bg="white").pack(pady=20)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Settings Page", font=("Helvetica", 20), bg="white").pack(pady=20)

if __name__ == "__main__":
    app = AssignmentTrackerApp()
    app.mainloop()
