
# Python To-Do App

The Python To-Do App is a simple and efficient task management application designed for users to create, view, and delete their tasks. Built using Python and MySQL, this project showcases fundamental programming skills and provides a practical solution for organizing daily activities. It serves as an educational tool for learning about database integration and user interface development.




## Features

- **Add Tasks**: Easily add new tasks to your to-do list.
- **View Tasks**: Display all tasks in a clear and organized format.
- **Mark as Complete**: Check off tasks when completed to keep track of progress.
- **Delete Tasks**: Remove tasks from the list once they are no longer needed.
- **Save Progress**: Store tasks locally to persist data even after closing the application.
- **User-Friendly Interface**: Simple and intuitive design for easy navigation.


## Installation


1. Clone the repository.
```
git clone https://github.com/AmazingDeveloper0102/Python-To-Do-Project.git
```
2. Navigate to the project directory.
```
cd Python-To-Do-Project
```
3. Make sure you have Python installed. You can then install the required packages using pip.
```
pip install mysql-connector-python
```
4. Set up the database by creating the necessary tables. Refer to the project documentation for details on the database schema.

5. Run the application.
```
python app.py
```
## Database Information

This application uses a MySQL database to store user data and tasks. Below are the details of the required tables:

### user_data Table

- **Table Name:** `user_data`
- **Columns:**
  - `id` (INT, Auto Increment, Primary Key): Unique identifier for each user.
  - `username` (VARCHAR(50), UNIQUE, NOT NULL): Unique username for the user.
  - `password` (VARCHAR(8), NOT NULL): Password for the user (consider hashing for security).
  - `name` (VARCHAR(50), NOT NULL): Name of the user.

### task_data Table

- **Table Name:** `task_data`
- **Columns:**
  - `task_id` (INT, Primary Key): Unique identifier for each task.
  - `user_name` (VARCHAR(50)): Username of the user associated with the task.
  - `task_name` (VARCHAR(50), NOT NULL): Name of the task.
  - `task_description` (TEXT): Detailed description of the task.
  - `task_priority` (VARCHAR(50)): Priority level of the task.
  - `task_status` (VARCHAR(20)): Current status of the task (e.g., Pending, Completed).
  - `task_due_date` (DATE): Due date for the task.
  
- **Foreign Key:**
  - `user_name` references `username` in the `user_data` table. If a user is deleted, all associated tasks will also be deleted (`ON DELETE CASCADE`).

### Example SQL to Create the Tables

```sql
CREATE TABLE user_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(8) NOT NULL,
    name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE task_data (
    task_id INT PRIMARY KEY,
    user_name VARCHAR(50),
    task_name VARCHAR(50) NOT NULL,
    task_description TEXT,
    task_priority VARCHAR(50),
    task_status VARCHAR(20),
    task_due_date DATE,
    FOREIGN KEY (user_name) REFERENCES user_data(username) ON DELETE CASCADE
) ENGINE=InnoDB;
```