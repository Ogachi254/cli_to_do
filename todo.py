# todo.py
from datetime import datetime
from models import Session, User, Task
from sqlalchemy.exc import IntegrityError
import sys
import getpass
import re
import bcrypt

def login():
    session = Session()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    user = session.query(User).filter(User.username == username).first()
    if user:
        if user.check_password(password):
            print("Login successful!")
            return user
        else:
            print("Invalid password.")
    else:
        print("Invalid username.")
    return None

def register():
    session = Session()
    username = input("Enter a username: ")
    
    while True:
        password = getpass.getpass("Enter a password: ")
        if len(password) < 8 or not re.search("[A-Z]", password) or not re.search("[a-z]", password) or not re.search("[0-9]", password) or not re.search("[!@#$%^&*()\[\]\-+=?]", password):
            print("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        else:
            break

    try:
        new_user = User(username=username)
        new_user.set_password(password) 
        session.add(new_user)
        session.commit()
        print("Registration successful! You can now login.")
    except IntegrityError:
        session.rollback()
        print("Username already exists. Please choose another one.")

def add_task():
    session = Session()

    while True:
        title = input("Enter the title for the new task: ")
        if title:
            break
        else:
            print("Title cannot be empty. Please enter a title.")

    while True:
        description = input("Enter the description for the new task: ")
        if description:
            break
        else:
            print("Description cannot be empty. Please enter a description.")

    while True:
        due_date_str = input("Enter the due date for the task (YYYY-MM-DD HH:MM) or leave blank if none: ")
        if not due_date_str:
            break
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M')
            break
        except ValueError:
            print("Invalid date format. Please enter the due date in the format YYYY-MM-DD HH:MM or leave blank if none.")

    if due_date_str:
        task = Task(title=title, description=description, due_date=due_date)
    else:
        task = Task(title=title, description=description)

    session.add(task)
    session.commit()
    print("Task added successfully.")

def delete_task():
    session = Session()
    tasks = session.query(Task).all()
    if tasks:
        print("Task List:")
        for task in tasks:
            print(f"Task #{task.id}: {task.title}")
        
        while True:
            task_id_str = input("Enter the ID of the task you want to delete: ")
            if task_id_str.isdigit():
                task_id = int(task_id_str)
                if any(task.id == task_id for task in tasks):
                    break
                else:
                    print("Task with provided ID not found. Please enter a valid ID.")
            else:
                print("Invalid input. Please enter a numerical ID.")

        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            print("Task deleted successfully.")
        else:
            print("Task not found.")
    else:
        print("No tasks found.")

def update_task():
    session = Session()
    tasks = session.query(Task).all()
    if tasks:
        print("Task List:")
        for task in tasks:
            print(f"Task #{task.id}: {task.title}")
        
        while True:
            task_id_str = input("Enter the ID of the task you want to update: ")
            if task_id_str.isdigit():
                task_id = int(task_id_str)
                if any(task.id == task_id for task in tasks):
                    break
                else:
                    print("Task with provided ID not found. Please enter a valid ID.")
            else:
                print("Invalid input. Please enter a numerical ID.")

        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            while True:
                new_title = input("Enter the new title for the task: ")
                if new_title:
                    break
                else:
                    print("Title cannot be empty. Please enter a title.")

            while True:
                new_description = input("Enter the new description for the task: ")
                if new_description:
                    break
                else:
                    print("Description cannot be empty. Please enter a description.")

            while True:
                new_due_date_str = input("Enter the new due date for the task (YYYY-MM-DD HH:MM) or leave blank if unchanged: ")
                if not new_due_date_str or (new_due_date_str and len(new_due_date_str) == 16 and new_due_date_str[4] == '-' and new_due_date_str[7] == '-' and new_due_date_str[10] == ' ' and new_due_date_str[13] == ':'):
                    break
                else:
                    print("Invalid date format. Please enter the due date in the format YYYY-MM-DD HH:MM or leave blank if unchanged.")

            task.title = new_title
            task.description = new_description
            if new_due_date_str:
                new_due_date = datetime.strptime(new_due_date_str, '%Y-%m-%d %H:%M')
                task.due_date = new_due_date
            session.commit()
            print("Task updated successfully.")
        else:
            print("Task not found.")
    else:
        print("No tasks found.")

def list_tasks():
    session = Session()
    tasks = session.query(Task).all()
    if tasks:
        print("All Tasks:")
        for task in tasks:
            print(f"Task #{task.id}:")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")
            print(f"  Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'None'}")
            print(f"  Is Completed: {'Yes' if task.is_completed else 'No'}")
            if task.user:
                print(f"  Assigned to: {task.user.username}")
            else:
                print("  Assigned to: None")
    else:
        print("No tasks found.")


def main():
    while True:
        print("\nWhat would you like to do?")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            user = login()
            if user:
                task_menu(user)
        elif choice == "2":
            register()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def view_task_details():
    session = Session()
    tasks = session.query(Task).all()
    if tasks:
        print("Task List:")
        for task in tasks:
            print(f"Task #{task.id}: {task.title}")
        task_id = int(input("Enter the ID of the task you want to view: "))
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            print(f"Task #{task.id}:")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")
            print(f"  Created At: {task.created_at}")
            print(f"  Due Date: {task.due_date}")
            print(f"  Is Completed: {task.is_completed}")
        else:
            print("Task not found.")
    else:
        print("No tasks found.")


def task_menu(user):
    while True:
        print("\nTask Management Menu:")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. Update a task")
        print("4. List all tasks")
        print("5. View task details")
        print("6. Logout")

        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            add_task()
        elif choice == "2":
            delete_task()
        elif choice == "3":
            update_task()
        elif choice == "4":
            list_tasks()
        elif choice == "5":
            view_task_details()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
      
if __name__ == "__main__":
    main()
