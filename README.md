# Expense Tracker

## Overview

This Flask application serves as an Expense Tracker, allowing users to manage their expenses by logging, editing, and deleting entries. The application uses a PostgreSQL database to store user information and expense records.

## Features

1. **User Authentication:**
    - Users can log in with their username and password.
    - New users can register for an account. 
	> **Warning**
	>
	> This is not yet secure. Please use a mock username and password.

2. **Expense Management:**
    - Users can add new expenses, providing details such as amount, description, expense date, and notes.
    - Expenses can be edited or deleted.

3. **Session Handling:**
    - User sessions are managed to keep users logged in during their interactions with the application.

## Getting Started

1. **Set Up Database:**
    - Create a PostgreSQL database named `ExpenseTracker`.
    - Adjust the database connection details in the `db_conn()` function within `app.py` to match your configuration.

2. **Install Dependencies:**
    - Install required Python packages using the following command:

    ```bash
    pip install psycopg2 flask
    ```

3. **Run the Application:**
    - Execute the `app.py` script to start the Flask application.

    ```bash
    python app.py
    ```

4. **Access the Application:**
    - Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the Expense Tracker.

## Usage

1. **Login:**
    - Existing users can log in with their username and password.

2. **Registration:**
    - New users can register for an account by providing their full name, username, and password.

3. **Expense Management:**
    - After logging in, users can add new expenses, view existing ones, and perform actions like editing or deleting.

4. **Logout:**
    - Users can log out, terminating their session.

## Folder Structure

- **templates:** Contains HTML templates for rendering pages.
- **static:** Reserved for css files.
- **app.py:** The main Flask application script.
- **schema.sql:** SQL script to create the necessary database tables.

## Database Schema

The application assumes the following database schema:

- **users:**
    - id (serial primary key)
    - fullname (varchar)
    - username (varchar)
    - password (varchar)

- **expenses:**
    - expense_id (serial primary key)
    - amount (numeric)
    - description (varchar)
    - expense_date (date)
    - notes (text)
    - created_at (timestamp)
    - userid (foreign key referencing users.id)

## Contributing

Feel free to contribute to the development of this Flask Expense Tracker by opening issues or submitting pull requests. Your feedback and enhancements are highly appreciated.

For any questions or issues, please open an [issue](https://github.com/valpaulo/ExpenseTracker/issues).

Happy expense tracking!