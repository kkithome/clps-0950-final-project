# clps-0950-final-project
Read Me: For Assignment Tracker Final Project CLPS 0950 
---
Purpose: 
Assignment Tracker App

This is a Python-based GUI application designed to help students manage their assignments. It includes user authentication, assignment tracking, a calendar view, a to-do list, and admin account management. The app is built using `tkinter`, Python’s standard GUI toolkit, along with `tkcalendar` for date picking.

Features Include: 

User Authentication

* **Sign Up** with first name, last name, username, and password
* **Login** system for returning users
* **Admin login** to delete existing user accounts

Assignment Table

* Add, edit, and delete assignments
* Each assignment has:

  * Title
  * Due Date
  * Class Name
  * Assignment Type
  * Completion Status
  * Priority Status (★)

Calendar View

* See a monthly calendar
* View assignments by date

To-Do List *(In Progress / Planned)*

* Displays priority or incomplete assignments

Progress Tracking *(In Progress / Planned)*

* Visualize progress based on completed assignments

Settings *(In Progress / Planned)*

Structure

Main Classes

* `Assignment`: Model to hold assignment information
* `AssignmentTrackerApp`: Main application class that manages pages and user state
* `LoginPage`, `SignUpPage`: Manage user access
* `TablePage`: Displays and manages the list of assignments
* `CalendarPage`: Monthly calendar to view assignments
* `ToDoPage`, `ProgressPage`, `SettingsPage`: Placeholder pages for future features

Admin Tools

* `admin_login()`: Prompts for admin credentials
* `delete_user_prompt()`: Allows admin to remove users from the system

Data Storage

* User data is saved in a `users.json` file using the `json` module
* Currently, assignments are stored only in memory and not persisted between sessions (can be extended with a save/load feature)

Requirements

Install `tkcalendar` if not already installed:

```bash
pip install tkcalendar
```

How to Run

```bash
python your_script_name.py
```

Files

* `users.json`: Stores user account information in JSON format
* `your_script_name.py`: Main Python script

Admin Account

Admins must have `"role": "admin"` manually added in the `users.json` file:

```json
{
  "adminuser": {
    "first_name": "Admin",
    "last_name": "User",
    "password": "adminpass",
    "role": "admin"
  }
}
```

Future Improvements

* Persistent storage for assignments (e.g., JSON or SQLite)
* Data export and import functionality
* User profile customization
* Filtering and sorting in the assignment table
* Enhanced progress analytics
* Responsive UI improvements

