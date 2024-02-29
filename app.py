import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'secret'


def db_conn():
    conn = psycopg2.connect(database="ExpenseTracker", host="localhost",
                            user="postgres", password="password", port="5432")
    return conn


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_username = request.form.get('username')
        entered_password = request.form.get('password')

        user_info = validate_credentials(entered_username, entered_password)

        if user_info:
            user_id = user_info[2]  # id is at index 2 in the result tuple of validate_credentials

            # Store user_id in session
            session['user_id'] = user_id

            print(f"Redirecting to expenses with user_id: {user_id}")
            return redirect(url_for('expenses'))

        error_message = 'Invalid username or password. Please try again.'
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')


def validate_credentials(username, password):
    conn = db_conn()
    cursor = conn.cursor()

    query = """
    SELECT username, password, id FROM users WHERE username = %s AND password = %s;
    """

    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            error_message = 'Passwords do not match. Please try again.'
            return render_template('newuser.html', error_message=error_message)

        # Check if the username is already in use
        if check_username_duplicate(username):
            error_message = 'Username is already in use. Please choose a different one.'
            return render_template('newuser.html', error_message=error_message)

        # Insert user into the database
        conn = db_conn()
        cur = conn.cursor()

        query = """
        INSERT INTO users (fullname, username, password)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        cur.execute(query, (fullname, username, password))
        user_id = cur.fetchone()[0]
        print(user_id)  # For debugging purposes

        conn.commit()
        cur.close()
        conn.close()

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('newuser.html')


def check_username_duplicate(username):
    conn = db_conn()
    cur = conn.cursor()

    query = "SELECT id FROM users WHERE username = %s;"
    cur.execute(query, (username,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    conn = db_conn()
    cur = conn.cursor()

    userid = session.get('user_id')
    print(f"Received user_id in expenses route: {userid}")

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'new':
            print(f"Received user_id in action new: {userid}")
            return add_new_expense(request.form)
        elif action == 'edit':
            return edit_expense()
        elif action == 'delete':
            return delete_expense()

    query = """
    SELECT u.fullname, e.expense_id, e.amount, e.description, e.expense_date, e.notes, e.created_at, e.userid
    FROM expenses AS e
    JOIN users AS u 
    ON e.userid = u.id
    WHERE e.userid = %s;
    """

    cur.execute(query, (userid,))
    data = cur.fetchall()

    cur.close()
    conn.close()

    # print(data)

    return render_template('expenses.html', expenses=data)


def add_new_expense(form_data):
    userid = session.get('user_id')
    print(f"Received user_id in add_new_expense route: {userid}")  # For debugging purposes

    amount = form_data.get('amount')
    description = form_data.get('description')
    expense_date = form_data.get('expense_date')
    notes = form_data.get('notes')

    # Print the values for debugging
    print(f"User ID: {userid}, Amount: {amount}, "
          f"Description: {description}, Expense Date: {expense_date}, Notes: {notes}")

    # Set created_at to the current timestamp
    created_at = datetime.now()

    # Implement logic to add a new expense to the database (adjust the query based on your schema)
    conn = db_conn()
    cur = conn.cursor()

    query = """
    INSERT INTO expenses (amount, description, expense_date, notes, created_at, userid)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    cur.execute(query, (amount, description, expense_date, notes, created_at, userid))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('expenses', user_id=userid))


@app.route('/edit_expense', methods=['GET', 'POST'])
def edit_expense():
    form_data = request.form

    expense_id = form_data.get('expense_id')
    amount = form_data.get('amount')
    description = form_data.get('description')
    expense_date = form_data.get('expense_date')
    notes = form_data.get('notes')

    conn = db_conn()
    cur = conn.cursor()

    query = """
    UPDATE expenses
    SET amount = %s, description = %s, expense_date = %s, notes = %s
    WHERE expense_id = %s;
    """

    cur.execute(query, (amount, description, expense_date, notes, expense_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('expenses'))


@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    expense_id = request.form.get('expense_id')

    conn = db_conn()
    cur = conn.cursor()

    query = """
    DELETE FROM expenses
    WHERE expense_id = %s;
    """
    cur.execute(query, (expense_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('expenses'))


@app.route('/logout')
def logout():
    session.clear()

    # Set the session cookie to expire
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session_id', '', expires=0)

    return response


if __name__ == '__main__':
    app.run(debug=True)
