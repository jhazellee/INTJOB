from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
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

# ----------------- Signup Route ----------------------------
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
@app.route('/applicant')
def applicant_dashboard():
    return render_template('main2.html') # This is your applicant page

@app.route('/employer')
def employer_dashboard():
    return render_template('owner.html') # This is your employer page

@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')
# --------------------------------------------------------------------------

# -------------------- Admin Management Routes --------------------
@app.route('/admin/users')
def admin_users():
    return render_template('usermanage.html') # Admin user management page

@app.route('/admin/applications')
def admin_applications():
    return render_template('applimanage.html') # Admin applications management page

@app.route('/admin/content')
def admin_content():
    return render_template('contntmanage.html') # Admin content management page

@app.route('/admin/report')
def admin_report():    
    return render_template('report.html') # Admin reports & analytics page

@app.route('/admin/payments')
def admin_payments():
    return render_template('payment.html') # Admin payment/subscription management page

@app.route('/admin/feed')
def admin_feed():
    return render_template('feed.html') # Admin feedback & complaints page

@app.route('/admin/settings')
def admin_settings():
    return render_template('sysSett.html') # Admin system settings page

@app.route('/admin/security')
def admin_security():
    return render_template('security.html') # Admin security & monitoring page
#-------------------------------------------------------------------------

#--------------------- Employer Routes --------------------
@app.route('/employer/owner')
def view_applicants():
    if 'user_id' not in session or session.get('role') != 'employer':
        return redirect(url_for('index'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # This query groups skills by user so you don't get duplicate rows for one person
        # STRING_AGG is a SQL Server function that puts skills in a comma-separated list
        query = """
            SELECT u.full_name, s.skill_name, s.category
            FROM users u
            JOIN user_skills us ON u.id = us.user_id
            JOIN skills s ON us.skill_id = s.id
            WHERE u.role = 'applicant'
        """
        cursor.execute(query)
        applicants = cursor.fetchall()
        conn.close()

        return render_template('viewapp.html', applicants=applicants)
    except Exception as e:
        return f"Error loading applicants: {e}" # Employer view applicants page

@app.route('/employer/jobspost')
def jobspost():
    return render_template('jobspost.html') # Employer job posting page

@app.route('/employer/appupdate')
def applicant_update():
    return render_template('applicantsupdates.html') # Employer applicant update page

@app.route('/employer/mess')
def mess():
    return render_template('mess.html') # Employer messaging page  

@app.route('/employer/companypfp')
def companypfp():
    return render_template('companypfp.html') # Employer company profile page

@app.route('/employer/sett')
def sett():
    return render_template('sett.html') # Employer settings page
#-------------------Employer Route End ---------------------------

# --------------------- Applicant Routes --------------------
@app.route('/applicant/jobcatego')
def jobcatego():
    return render_template('jobcatego.html') # Applicant job categories page

@app.route('/applicant/inbox')
def inbox():
    return render_template('inbox.html') # Applicant inbox page 

@app.route('/applicant/appliedsta')
def appliedsta():
    return render_template('appliedsta.html') # Applicant application status page

@app.route('/applicant/resume')
def resume():
    return render_template('resume.html') # Applicant resume page

@app.route('/skills-checklist')
def skills_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('skillsandsports.html')

@app.route('/applicant/settings')
def applicant_settings():
    return render_template('settings.html')

@app.route('/applicant/profile')
def applicant_profile():
    return render_template('profile.html')

@app.route('/applicant/customersupport')
def customersupport():
    return render_template('customersupport.html')

# ------------------- Applicant Route End ---------------------------


# -------------------- Login Route --------------------
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

        if user and check_password_hash(user.password_hash, password):
            if user.role != role:
                conn.close()
                return jsonify({"success": False, "message": "Invalid role selected."})

            # Set Session
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['role'] = user.role

            # --- APPLICANT REDIRECTION LOGIC ---
            if user.role == 'applicant':
                # Check if this user has any skills saved already
                cursor.execute("SELECT COUNT(*) FROM user_skills WHERE user_id = ?", (user.id,))
                has_skills = cursor.fetchone()[0]
                conn.close()

                if has_skills > 0:
                    # User exists and has profile completed
                    return jsonify({"success": True, "redirect": url_for('applicant_dashboard')})
                else:
                    # New user or profile incomplete
                    return jsonify({"success": True, "redirect": url_for('skills_page')})

            # --- EMPLOYER REDIRECTION LOGIC ---
            elif user.role == 'employer':
                conn.close()
                return jsonify({"success": True, "redirect": url_for('employer_dashboard')})

        if conn: conn.close()
        return jsonify({"success": False, "message": "Invalid email or password."})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

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


# -------------------- For Saving Skills ---------------------------
@app.route('/save-skills', methods=['POST'])
def save_skills():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Session expired"}), 401

    data = request.get_json()
    skills_list = data.get('skills', [])
    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_skills WHERE user_id = ?", (user_id,))
        for skill_name in skills_list:
            cursor.execute("SELECT id FROM skills WHERE skill_name = ?", (skill_name,))
            row = cursor.fetchone()
            if row:
                skill_id = row[0]
            else:
                cursor.execute("INSERT INTO skills (skill_name) OUTPUT INSERTED.id VALUES (?)", (skill_name,))
                skill_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO user_skills (user_id, skill_id) VALUES (?, ?)", (user_id, skill_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


 # ------------------------------------------  
if __name__ == '__main__':
    app.run(debug=True)