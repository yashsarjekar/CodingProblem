# Problem 2

## Description

There is a manual QC process which happens. There is a portal from which each individual qc task is assigned. The portal needs to check how many qc persons are logged in and which of the logged in persons are free, as in not on a task, and automatically assign tasks. Once the task is finished the person will automatically get assigned the next task if any is pending. How would you architect this? I want to understand step by step the methodology you used to come to the final solution. Can you illustrate a basic API framework written in Python using Flask and SQLite as the database.


## Requirements

```
pip install -r requirements.txt
```

## Usage
Open two command prompt window in first window run the Flask application. Use second command prompt window for cURL commands execution.
```
python app.py
```

## Solution 

To architect a solution for the given problem, we can follow the below steps:

Define the data model - We need to define the data model for the QC tasks and the QC persons. The data model should capture the necessary information about the tasks and the persons.

Design the API - We need to design the API for the portal, which will allow us to assign tasks to free users automatically, check the status of persons, and create users and tasks.

Implement the API - We need to implement the API using Python Flask and SQLite as the database.

Test the API - We need to test the API thoroughly to ensure that it is working as expected.

Now, let's dive into the details of each step:

### Define the data model:
We need to define the data model for the tasks and the persons. We can define the data model as follows:


```
users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        is_free BOOLEAN NOT NULL,
        is_logged_in BOOLEAN NOT NULL
    )
```
```
tasks (
        id INTEGER PRIMARY KEY,
        task_name TEXT NOT NULL,
        description TEXT NOT NULL,
        time_required INTEGER NOT NULL,
        time_remaining INTEGER NOT NULL,
        user_id INTEGER,
        date_time TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
```

### Design the API:
Based on the data model, we can design the API for the portal. We need to design the following endpoints:

/login [POST]: Endpoint to login a user.
/logout [POST]: Endpoint to logout a user.
/tasks [GET]: Endpoint to get all tasks.
/tasks/<int:id> [GET]: Endpoint to get specific task based on ID.
/users [POST]: Endpoint to create new user.
/tasks [POST]: Endpoint to create new task


There are two function which executes in backgroud periodically to assign task to free users and to check
where task is completed or not, If task get completed make time_remaining to 0 and make user free.
The two functions are:

- assign_task
- complete_task


### Implement the API:
We can implement the API using Python Flask and SQLite as the database. We need to create the following Python files:

- app.py: This file contains the Flask application and the endpoints for the API.

### Test the API:
We need to test the API thoroughly to ensure that it is working as expected. We can use tools like Postman or cURL to test the API endpoints.


Below are some examples 

Create User
```
curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"newuser\", \"password\": \"newpassword\"}" http://127.0.0.1:5000/users
```

Login command
```
curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"newuser\", \"password\": \"newpassword\"}" http://127.0.0.1:5000/login
```

Create Task
```
curl -X POST -H "Content-Type: application/json" -d "{\"task_name\":\"task1\",\"description\":\"description1\",\"time_required\":3}" http://127.0.0.1:5000/tasks
```

Get task with ID
```
curl http://localhost:5000/tasks/1
```

Get all tasks
```
curl http://localhost:5000/tasks
```

Logout Command
```
curl -X POST -H "Content-Type: application/json" -d "{\"user_id\": \"1\"}" http://127.0.0.1:5000/logout
```