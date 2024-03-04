from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_connection
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secure secret key

@app.route("/")
def landing_page():
    return render_template('landing_page.html')

@app.route("/signin", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_connection()
            query = text(f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'")
            result = list(conn.execute(query).fetchone())
            print(result)

            if result:
                session['user_id'] = result[0]
                return redirect(url_for('dashboard'))
        except Exception as e:
            print("Error:", e)
            #flash('User does not exists. Please register.', 'error')
            return redirect(url_for('sign_up'))

    return render_template('sign_in.html')

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_connection()
            query = text(f"INSERT INTO users (name, username, password) VALUES ('{name}', '{username}', '{password}')")
            conn.execute(query)
            flash('Account created successfully. Please sign in.', 'success')
            return redirect(url_for('sign_in'))

        except Exception as e:
            print("Error:", e)
            flash('An error occurred while creating the account. Please try again.', 'error')

    return render_template('sign_up.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('sign_in'))

@app.route("/dashboard")
def dashboard():
    # Add authentication check
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_connection()
        query = text(f"select username from users where id = '{user_id}';")
        result = list(conn.execute(query).fetchone())
        if result:
            username = result[0]
            return render_template('dashboard.html', username = username)
    else:
        flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

if __name__ == "__main__":
    app.run(debug=True)
