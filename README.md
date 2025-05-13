# clps-0950-final-project
Assignment Tracker
A simple Python desktop application built using Tkinter that helps students manage their assignments. We were inspired by finals and the roles the members of our group currently have as an Academic Coach, a tutor, and a CC. We wanted to create the basis for a functional tool that would be programmable and usable for our own endeavors.  Features include login/signup, admin control, assignment entry, calendar view, an automatically generated to-do list, a settings page, and a progress tracking page to show how much of your assignments you've completed. 

Features
- User Login and Signup that stores your data. 
- Add assignments with due dates, priority, and completion status
- Calendar view of upcoming assignments
- To-Do List that shows uncompleted and priority assignments
- Progress tracking that shows how much of the assignments have been completed 


Project Structure
assignment_tracker/
├── main.py
├── assignments.csv
├── users.csv
└── README.md
```

Requirements to run:
- Python 3.x
- `tkinter` (usually comes with Python)
- `tkcalendar` (`pip install tkcalendar`) (version 9 or above)
- `csv` (built-in)

To install `tkcalendar`, run:
```bash
pip install tkcalendar
```

How to Run:
1. Clone or download this repository.
2. Make sure `assignments.csv` and `users.csv` are in the same folder as `main.py`.
3. Run the app:
```bash
python main.py
```

Usage:
1. Launch the app and log in or sign up as a new user. (Name, Username, Password)
2. Use the assignment page to add tasks with a due date, priority, and completion status.
3. View all assignments on the calendar and see dates when assignments are due.
4. Check the To-Do List page to see uncompleted and high-priority tasks.
5. If you are an admin, you can delete user accounts from the login page.

Authors 
Kaluki Kithome, Selam Asfaw, Shayla Hillis

Notes: 
- All data is stored locally in CSV files.
- Designed for organizing finals for students at Brown.
