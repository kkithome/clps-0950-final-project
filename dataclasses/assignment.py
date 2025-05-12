import tkinter
from tkinter import Tk
from tkinter import *

class Assignment:
    def __init__(self, title, due_date, class_name, assignment_type, completed=False, priority=False):
        self.title = title
        self.due_date = due_date 
        self.class_name = class_name
        self.assignment_type = assignment_type
        self.completed = completed
        self.priority = priority  # priority added to link to to do list later







