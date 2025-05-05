import tkinter as tk
from tkinter import ttk

class AssignmentTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("800x600")
        self.configure(bg="white")

        self.frames = {}

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
        frame.tkraise()

    def show_home(self): self.show_page(HomePage)
    def show_table(self): self.show_page(TablePage)
    def show_calendar(self): self.show_page(CalendarPage)
    def show_todo(self): self.show_page(ToDoPage)
    def show_progress(self): self.show_page(ProgressPage)
    def show_settings(self): self.show_page(SettingsPage)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Welcome to the Assignment Tracker!", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


class TablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        label = tk.Label(self, text="Table View Page", font=("Helvetica", 20), bg="white")
        label.pack(pady=50)


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


if __name__ == "__main__":
    app = AssignmentTrackerApp()
    app.mainloop()
