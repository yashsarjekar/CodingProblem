from flask import Flask, jsonify, request, make_response
import sqlite3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
print('Starting application...')

# Set up the database connection
try:
    conn = sqlite3.connect('database.db', check_same_thread=False)
    connection_db = conn.cursor()
    scheduler = BackgroundScheduler(daemon=True)

    # Create the users and tasks tables if they don't exist
    connection_db.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_free BOOLEAN NOT NULL,
                    is_logged_in BOOLEAN NOT NULL
                )''')
    connection_db.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    time_required INTEGER NOT NULL,
                    time_remaining INTEGER NOT NULL,
                    user_id INTEGER,
                    date_time TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
except Exception as err:
    print('[ERROR] ', err)


@app.route('/login', methods=['POST'])
def login():
    '''
        Summary: Function is used for user login.
        Args:
            username json: Username of user.
            password json: Password of user. 
        Returns:
            response json: Status of user login.
    '''
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        connection_db.execute('SELECT id, is_free FROM users WHERE username = ? AND password = ?', (username, password))
        user = connection_db.fetchone()
        if user is None:
            return make_response(jsonify({'[ERROR]': 'Invalid username or password'}), 401)
        elif not user[1]:
            return make_response(jsonify({'[ERROR]': 'User is already logged in'}), 400)
        else:
            connection_db.execute('UPDATE users SET is_logged_in = 1 WHERE id = ?', (user[0],))
            conn.commit()
            return make_response(jsonify({'[INFO]': 'Login successful'}), 200)
    except Exception as err:
        print('[ERROR] ', err)


@app.route('/logout', methods=['POST'])
def logout():
    '''
        Summary: Function is used for user logout
        Args:
            user_id json: User id.
        Returns:
            response json: Status of user logout.
    '''
    try:
        user_id = request.json.get('user_id')
        connection_db.execute('SELECT id FROM users WHERE id = ? AND is_logged_in = 1', (user_id,))
        user = connection_db.fetchone()
        if user is None:
            return make_response(jsonify({'[ERROR]': 'Invalid user ID or user is not logged in'}), 401)
        else:
            connection_db.execute('UPDATE users SET is_logged_in = 0 WHERE id = ?', (user_id,))
            conn.commit()
            return make_response(jsonify({'[INFO]': 'Logout successful'}), 200)
    except Exception as err:
        print('[ERROR] ', err)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    '''
        Summary: Function returns all the tasks.
        Returns:
            response json: All tasks
    '''
    try:
        connection_db.execute('SELECT id, task_name, description, time_required, time_remaining, user_id FROM tasks')
        tasks = connection_db.fetchall()
        return jsonify({'tasks': tasks})
    except Exception as err:
        print('[ERROR] ', err)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    '''
        Summary: Function returns the task whose ID matches the input ID.
        Args:
            id int: ID of task.
        Returns:
            response json: Task with given ID.
    '''
    try:
        connection_db.execute('SELECT id, task_name, description, time_required, time_remaining, user_id FROM tasks WHERE id = ?', (id,))
        task = connection_db.fetchone()
        if task is None:
            return make_response(jsonify({'[ERROR]': 'Invalid task ID'}), 404)
        else:
            return jsonify({'task': task})
    except Exception as err:
        print('[ERROR] ', err)


@app.route('/users', methods=['POST'])
def create_user():
    '''
        Summary: Function create new user.
        Args:
            username json: Username of user.
            password json: Password of user.
        Returns:
            response json: Information regarding User creation.
    '''
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        connection_db.execute('INSERT INTO users (username, password, is_free, is_logged_in) VALUES (?, ?, 1, 0)', (username, password))
        conn.commit()
        return make_response(jsonify({'[INFO]': 'User created successfully'}), 201)
    except Exception as err:
        print('[ERROR] ', err)


@app.route('/tasks', methods=['POST'])
def create_task():
    '''
        Summary: Function create new task.
        Args:
            task_name json: Task Name.
            description json: Task Description.
            time_required json: Time required to complete task.
        Returns:
            response json: Information regarding Task creation.
    '''
    try:
        task_name = request.json.get('task_name')
        description = request.json.get('description')
        time_required = request.json.get('time_required')
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = None
        connection_db.execute('INSERT INTO tasks (task_name, description, time_required, time_remaining, user_id, date_time) VALUES (?, ?, ?, ?, ?, ?)', (task_name, description, time_required, time_required, user_id, date_time))
        conn.commit()
        return make_response(jsonify({'[INFO]': 'Task created successfully'}), 201)
    except Exception as err:
        print('[ERROR] ', err)


def assign_task():
    '''
        Summary: Automatically Assign task to user who is free.
    '''
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        connection_db = conn.cursor()

        # Select a task that has not been assigned yet
        connection_db.execute("SELECT * FROM tasks WHERE user_id IS NULL and time_remaining > 0 ORDER BY date_time ASC LIMIT 1")
        task = connection_db.fetchone()

        # Select a free user
        connection_db.execute("SELECT * FROM users WHERE is_free = 1 and is_logged_in = 1")
        user = connection_db.fetchone()

        # If there is a task and a free user, assign the task to the user
        if task and user:
            # Update the task with the user_id and date_time fields
            task_id = task[0]
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            connection_db.execute("UPDATE tasks SET user_id = ?, date_time = ? WHERE id = ?", (user[0], date_time, task_id))

            # Update the user's is_free field
            connection_db.execute("UPDATE users SET is_free = 0 WHERE id = ?", (user[0],))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            print(f"[INFO] Task '{task[1]}' has been assigned to user '{user[1]}' at {date_time}.")
        else:
            print("[INFO] No tasks or free users available.")
    except Exception as err:
        print('[ERROR] ', err)


def complete_task():
    """Periodically check for tasks that are assigned to a user and have exceeded their time limit."""
    
    try:
        # Get the current time
        now = datetime.now()
        # Select all tasks that are assigned to a user and have a time remaining greater than zero
        query = "SELECT * FROM tasks WHERE user_id IS NOT NULL AND time_remaining > 0"
        cursor = conn.cursor()
        cursor.execute(query)
        tasks = cursor.fetchall()

        # Loop over the tasks and check if they have exceeded their time limit
        for task in tasks:
            # Get the task details
            task_id, task_name, description, time_required, time_remaining, user_id, date_time = task
            # Get the user details
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            # Check if the user is free
            if user[3] == 0:
                # Calculate the time difference between the current time and the date_time field
                task_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                time_diff = now - task_time

                # Check if the time difference is greater than the time required for the task
                if time_diff.total_seconds() > time_required*60:
                    # Update the task with a time_remaining of 0
                    query = "UPDATE tasks SET time_remaining = 0 WHERE id = ?"
                    cursor.execute(query, (task_id,))

                    query1 = "UPDATE users SET is_free = 1 WHERE id = ?"
                    cursor.execute(query1, (user_id,))
                    conn.commit()
                    print(f"[INFO] Task Name:- {task_name}, Task ID:- {task_id} Completed by User:- {user[1]}")
                    print(f"[INFO] Username:- {user[1]} is free")
    except Exception as err:
        print('[ERROR] ', err)


# Add the task to the scheduler to run every minute
scheduler.add_job(assign_task, 'interval', minutes=1)
scheduler.add_job(complete_task, 'interval', minutes=1)
# Start the scheduler
scheduler.start()

app.run()