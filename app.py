import mysql.connector as connector
import configparser

# Read configuration from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Establishing a connection to the database using config file
db = connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    passwd=config['mysql']['passwd'],
    database=config['mysql']['database']
)

cursor = db.cursor()


class ToDoApp:
    def __init__(self):
        self.user_name = None  # Initialize user name
        self.first_func()  # Start the first function

    def first_func(self):
        print("Welcome to the ToDo App!")
        while True:
            try:
                # User choice for login, register or exit
                first_func_choice = int(input("For Login press 1.\nFor Register press 2.\nFor Leaving the app press 3.\n--> "))
                if first_func_choice == 1:
                    login_success = self.login_user()  # Attempt to log in
                    if login_success: 
                        self.to_do_func()  # Go to task functions if login is successful
                elif first_func_choice == 2:
                    self.register_user()  # Register a new user
                elif first_func_choice == 3:
                    print("Thanks for using the app!")  # Exit message
                    break
                else:
                    print("Invalid Input. Please choose a valid option (1, 2, or 3).")  # Error message
            except ValueError:
                print("Invalid Input. Please enter a number (1, 2, or 3).")  # Error message for invalid input

    def login_user(self):
        # Prompt for username and validate
        input_username = str(input("Please enter your Username: "))
        cursor.execute("SELECT * FROM user_data WHERE username = %s", (input_username,))
        user = cursor.fetchone()
        if user:
            attempts = 2  # Maximum password attempts
            input_password = input("Please enter your password: ")
            if user[2] == input_password:
                print("Login Successful!")  # Success message
                self.user_name = input_username
                return True  # Indicate successful login
            else:
                # Loop for password attempts
                while attempts > 0:
                    input_password = input(f"Incorrect Password. You have {attempts} attempts left. Please enter your password: ")
                    if user[2] == input_password:
                        print("Login Successful!")  # Success message
                        self.user_name = input_username
                        return True  # Indicate successful login
                    else:
                        attempts -= 1
                print("You have exceeded the maximum number of attempts. Try later...")  # Error message
        else:
            # Prompt to register a new user if not found
            while True:
                login_choice = input("User not found in database. Do you want to register a New User? (Y/N): ").lower()
                if login_choice == "y":
                    self.register_user()  # Register new user
                    break
                elif login_choice == "n":
                    print("Thanks for using the app!")  # Exit message
                    break
                else:
                    print("Invalid Input. Please choose a valid option (Y/N).")  # Error message
        return False  # Indicate unsuccessful login
        
    def register_user(self):
        # Prompt for user's name
        input_name = str(input("Please enter your name: \n--> "))

        while True:
            # Loop for unique username
            input_user_name = str(input("Please enter the username you want to set: \n--> "))
            cursor.execute("SELECT * FROM user_data WHERE username = %s", (input_user_name,))
            if cursor.fetchone():
                print("Username already exists! Please try a different one.")  # Error message
            else:
                break  # Username is unique, break loop
        
        while True:
            # Prompt for password with length validation
            input_password = str(input("Please enter the password you want to set: \nnote - password must be exactly 8 characters.\n--> "))
            if len(input_password) == 8:
                break  # Valid password length
            else:
                print("Invalid password! It must be exactly 8 characters long. Please try again.")  # Error message

        # Get the next available user ID
        cursor.execute("SELECT MAX(id) FROM user_data")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id else 1

        # Insert new user into the database
        cursor.execute("INSERT INTO user_data (id, username, password, name) VALUES (%s, %s, %s, %s)",
                       (new_id, input_user_name, input_password, input_name))
        db.commit()

        print(f"User '{input_user_name}' registered successfully!")  # Success message
        self.user_name = input_user_name  # Set the current user name
        self.to_do_func()  # Move to task functions
        
    def to_do_func(self):
        while True: 
            try:
                # Menu options for task management
                to_do_func_choice = int(input("\nHow would you like to proceed\nPress 1 to Add Task\nPress 2 to Show Tasks\nPress 3 to Update a Task\nPress 4 to Delete Task\nPress 5 to Filter Task\nPress 6 to Clear all tasks\nPress 7 to Logout\n--> "))

                if to_do_func_choice == 1:
                    self.add_task_func()  # Add a new task
                elif to_do_func_choice == 2:
                    self.show_tasks_func()  # Show existing tasks
                elif to_do_func_choice == 3:
                    self.update_task_func()  # Update an existing task
                elif to_do_func_choice == 4:
                    self.delete_task_func()  # Delete a task
                elif to_do_func_choice == 5:
                    self.filter_task_func()  # Filter tasks based on criteria
                elif to_do_func_choice == 6:
                    self.clear_all_tasks_func()  # Clear all tasks
                elif to_do_func_choice == 7:
                    print("Thanks For Using! Logging Out...")  # Exit message
                    break
                else:
                    print("Invalid choice! Please try again.")  # Error message
            except ValueError:
                print("Invalid choice! Please try again.")  # Error message

    def add_task_func(self):
        while True:
            input_task_name = str(input("Enter task you want to add\n--> "))
            if input_task_name == '':
                print("Task name can't be empty")  # Error message
                continue  # Repeat the loop for a valid task name
            break

        while True:
            # Prompt for task description
            input_task_description_choice = str(input("Do you want to add a description to your task? (Y/N): \n--> ")).lower()
            if input_task_description_choice == "y":
                input_task_description = str(input("Enter description of task\n--> "))
                break
            elif input_task_description_choice == "n":
                input_task_description = None  # No description
                break
            else:
                print("Invalid choice! Please choose Y or N.")  # Error message

        while True:
            # Prompt for task priority
            input_task_priority_choice = str(input("Do you want to add a priority to your task? (Y/N): \n--> ")).lower()
            if input_task_priority_choice == "y":
                input_task_priority_selection = int(input("Enter 1 for 'Low'\nEnter 2 for 'Medium'\nEnter 3 for 'High': \n--> "))
                if input_task_priority_selection == 1:
                    input_task_priority = "Low"
                    break
                elif input_task_priority_selection == 2:
                    input_task_priority = "Medium"
                    break
                elif input_task_priority_selection == 3:
                    input_task_priority = "High"
                    break
                else:
                    print("Invalid choice! Please choose 1, 2, or 3.")  # Error message
            else:
                input_task_priority = None  # No priority
                break
            
        while True:
            # Prompt for task status
            input_task_status_choice = str(input("Do you want to add a status? (Y/N): \n--> ")).lower()
            if input_task_status_choice == "y":
                input_task_status_selection = int(input("Enter 1 for 'Not Started'\nEnter 2 for 'Working'\nEnter 3 for 'Completed': \n--> "))
                if input_task_status_selection == 1:
                    input_task_status = "Not Started"
                    break
                elif input_task_status_selection == 2:
                    input_task_status = "Working"
                    break
                elif input_task_status_selection == 3:
                    input_task_status = "Completed"
                    break
                else:
                    print("Invalid choice! Please choose 1, 2, or 3.")  # Error message
            else:
                input_task_status = None  # No status
                break

        while True:
            # Prompt for task due date
            input_task_due_date_choice = str(input("Do you want to add a due date to your task? (Y/N): \n--> "))
            if input_task_due_date_choice == "y":
                input_task_due_date = str(input("Enter due date of task (in YYYY-MM-DD format)\n--> "))
                break
            elif input_task_due_date_choice == "n":
                input_task_due_date = None  # No due date
                break
            else:
                print("Invalid choice! Please choose Y or N.")  # Error message

        # Get the next available task ID
        cursor.execute("SELECT MAX(task_id) FROM task_data")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id else 1

        # Insert new task into the database
        cursor.execute("INSERT INTO task_data (task_id, task_name, task_description, task_priority, task_status, task_due_date, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (new_id, input_task_name, input_task_description, input_task_priority, input_task_status, input_task_due_date, self.user_name))
        db.commit()

        print(f"Task '{input_task_name}' added successfully!")  # Success message

    def show_tasks_func(self):
        # Retrieve tasks for the logged-in user
        cursor.execute("SELECT * FROM task_data WHERE user_name = %s", (self.user_name,))
        tasks = cursor.fetchall()

        if not tasks:
            print("You have no tasks yet!")  # Message when no tasks are found
            return

        print("\nYour Tasks:")  # Header for task display
        print("-" * 50)  # Divider line

        for task in tasks:
            print(f"Task ID     : {task[0]}")
            print(f"Task Name   : {task[2]}")
            print(f"Description : {task[3]}")
            print(f"Priority    : {task[4]}")
            print(f"Status      : {task[5]}")
            print(f"Due Date    : {task[6]}")
            print("-" * 50)  # Divider between tasks


    def update_task_func(self):
        # Show current tasks
        self.show_tasks_func()
        try:
            task_id = int(input("Enter the ID of the task you want to update: \n--> "))  # Prompt for task ID
            cursor.execute("SELECT * FROM task_data WHERE task_id = %s AND user_id = %s", (task_id, self.user_name))
            task = cursor.fetchone()
            if task is None:
                print("Task not found or you do not have permission to update this task.")  # Error message
                return

            # Prompt for new task name
            input_new_task_name = str(input("Enter the new task name: \n--> "))
            cursor.execute("UPDATE task_data SET task_name = %s WHERE task_id = %s", (input_new_task_name, task_id))  # Update task name
            db.commit()
            print("Task updated successfully!")  # Success message
        except ValueError:
            print("Invalid input. Please enter a valid task ID.")  # Error message

    def delete_task_func(self):
        self.show_tasks_func()  # Show current tasks
        try:
            task_id = int(input("Enter the ID of the task you want to delete: \n--> "))  # Prompt for task ID
            cursor.execute("DELETE FROM task_data WHERE task_id = %s AND user_id = %s", (task_id, self.user_name))  # Delete task
            db.commit()
            print("Task deleted successfully!")  # Success message
        except ValueError:
            print("Invalid input. Please enter a valid task ID.")  # Error message


    def filter_task_func(self):
        filter_choice = input("Filter tasks by:\n1. Priority\n2. Status\n--> ")
        if filter_choice == '1':
            priority = input("Enter the priority (Low, Medium, High): \n--> ")
            cursor.execute("SELECT * FROM task_data WHERE user_name = %s AND task_priority = %s", (self.user_name, priority))  # Filter by priority
        elif filter_choice == '2':
            status = input("Enter the status (Not Started, Working, Completed): \n--> ")
            cursor.execute("SELECT * FROM task_data WHERE user_name = %s AND task_status = %s", (self.user_name, status))  # Filter by status
        else:
            print("Invalid choice!")  # Error message
            return

        tasks = cursor.fetchall()
        if not tasks:
            print("No tasks found for the given filter criteria.")  # Message when no tasks match filter
            return

        print("\nFiltered Tasks:")  # Header for filtered tasks display
        for task in tasks:
            print(f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Priority: {task[3]}, Status: {task[4]}, Due Date: {task[5]}")  # Display filtered tasks

    def clear_all_tasks_func(self):
        cursor.execute("DELETE FROM task_data WHERE user_name = %s", (self.user_name,))  # Clear all tasks for the user
        db.commit()
        print("All tasks cleared successfully!")  # Success message


if __name__ == "__main__":
    ToDoApp()  # Start the ToDo app

# Close the database connection when done
db.close()
