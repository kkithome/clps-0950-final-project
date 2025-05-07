import tkinter as tk
from tkinter import ttk

# Assignment data model
class Assignment:
    def __init__(self, title, due_date, class_name, assignment_type, completed=False):
        self.title = title
        self.due_date = due_date
        self.class_name = class_name
        self.assignment_type = assignment_type
        self.completed = completed


# Main application
class AssignmentTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("800x600")
        self.configure(bg="white")

        self.frames = {}

        # List to store assignment objects
        self.assignments = [
            Assignment("Problem Set 1", "2025-05-10", "Physics", "Homework"),
            Assignment("Essay Draft", "2025-05-12", "English", "Writing", completed=True)
        ]

        # Navigation bar
        nav_bar = tk.Frame(self, bg="#eee", height=50)
        nav_bar.pack(fill='x')

        buttons = [
            ("Home", self.show_home),
            ("Table", self.show_table),
            ("Calendar", self.show_calendar),
            ("To-Do", self.show_todo),
            ("Progress", self.show_progress),
            ("Settings", self.show_settings),
        ]

        for name, command in buttons:
            tk.Button(nav_bar, text=name, command=command, bg="#ddd").pack(side='left', padx=5, pady=10)

        # Container for pages
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.init_pages()
        self.show_home()

    def init_pages(self):
        for PageClass in (HomePage, TablePage, CalendarPage, ToDoPage, ProgressPage, SettingsPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_class):
        frame = self.frames[page_class.__name__]
        if hasattr(frame, 'refresh'):
            frame.refresh()  # call refresh if the page supports it
        frame.tkraise()

    def show_home(self): self.show_page(HomePage)
    def show_table(self): self.show_page(TablePage)
    def show_calendar(self): self.show_page(CalendarPage)
    def show_todo(self): self.show_page(ToDoPage)
    def show_progress(self): self.show_page(ProgressPage)
    def show_settings(self): self.show_page(SettingsPage)


# Individual pages
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Welcome to the Assignment Tracker!", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


class TablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        label = tk.Label(self, text="Assignment Table", font=("Helvetica", 20), bg="white")
        label.pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("Title", "Due Date", "Class", "Type", "Completed"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        # Clear previous entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert updated assignment list
        for a in self.controller.assignments:
            self.tree.insert("", "end", values=(a.title, a.due_date, a.class_name, a.assignment_type, "Yes" if a.completed else "No"))


class CalendarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Calendar View Page", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="To-Do List Page", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


class ProgressPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Progress Tracker Page", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Settings Page", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


# Run the application
if __name__ == "__main__":
    app = AssignmentTrackerApp()
    app.mainloop()
