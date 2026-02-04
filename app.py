from flask import Flask, render_template, request, session, redirect, url_for, flash
import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'anyaaaa1234'  # Needed for session management


# Connection string for SQL Server
# Change 'YourServerName' and 'YourDatabaseName' to your actual details
def get_db_connection():
    # Use a raw string (r'...') to prevent backslash errors in server names
    conn_str = (
        r'DRIVER={ODBC Driver 18 for SQL Server};'
        r'SERVER=MRSVELASCO\SQLEXPRESS;'
        r'DATABASE=thesis_prac;'
        r'Trusted_Connection=yes;'
        r'Encrypt=yes;'
        r'TrustServerCertificate=yes;'
    )
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    # Hash the password before it ever touches the database
    hashed_pw = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # We save hashed_pw, NOT the raw password
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (full_name, email, hashed_pw, role)
        )
        conn.commit()
        conn.close()
        return "Account created securely! You can now login."
    except Exception as e:
        return f"Signup Error: {e}"

# --------------------------------------------------------------------------
# Applicant, Employer, Admin Home Routes
@app.route('/applicant-home')
def applicant_dashboard():
    return render_template('owner.html') # This is your applicant page

@app.route('/employer-home')
def employer_dashboard():
    return render_template('skillsandsports.html') # This is your employer page

@app.route('/admin-home')
def admin_dashboard():
    return render_template('admin.html')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user.password_hash, password):
            # 1. Save info to session
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['role'] = user.role

            # 2. Redirect based on role (The Python version of your JS logic)
            if user.role == 'applicant':
                return redirect(url_for('applicant_dashboard'))
            elif user.role == 'employer':
                return redirect(url_for('employer_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
        
        return "Invalid credentials"
    except Exception as e:
        return f"Error: {e}"

# Logout Route
@app.route('/logout')
def logout():
    # Remove all data from the session
    session.clear()
    return redirect(url_for('index'))

# Protected Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index')) # Boot them out if not logged in
    
    return "This is your private job dashboard!"