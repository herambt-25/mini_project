import sqlite3
import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

# Create the admin blueprint. url_prefix means all routes here start with /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schemes.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    # If the admin submits the login form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        # Check if user exists AND if the password matches the hash
        if admin and check_password_hash(admin['password_hash'], password):
            # Save a secure session token
            session['admin_logged_in'] = True
            session['admin_id'] = admin['id']
            return redirect(url_for('admin.dashboard'))
        else:
            error = "Invalid username or password. Please try again."
            
    # Show the login page
    return render_template('admin/login.html', error=error)

@admin_bp.route('/logout')
def logout():
    """Clears the session and logs the admin out."""
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
def dashboard():
    """Protected Admin Dashboard."""
    # SECURITY: Check if the user is actually logged in!
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    schemes = conn.execute('SELECT id, name_en, category, state_applicability FROM schemes ORDER BY id DESC').fetchall()
    conn.close()
    
    return render_template('admin/dashboard.html', schemes=schemes)

@admin_bp.route('/schemes/add', methods=['GET', 'POST'])
def add_scheme():
    """Allows admin to create a new scheme."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO schemes (
                name_en, description_en, ministry, category, state_applicability, 
                min_age, max_age, max_income, target_gender, target_occupation, benefits_en, official_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['name'], request.form['description'], request.form['ministry'],
            request.form['category'], request.form['state'], request.form['min_age'],
            request.form['max_age'], request.form['max_income'], request.form['gender'],
            request.form['occupation'], request.form['benefits'], request.form['source']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/add_scheme.html')

@admin_bp.route('/schemes/edit/<int:id>', methods=['GET', 'POST'])
def edit_scheme(id):
    """Allows admin to update an existing scheme."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    
    if request.method == 'POST':
        conn.execute('''
            UPDATE schemes SET 
                name_en=?, description_en=?, ministry=?, category=?, state_applicability=?, 
                min_age=?, max_age=?, max_income=?, target_gender=?, target_occupation=?, 
                benefits_en=?, official_source=?
            WHERE id=?
        ''', (
            request.form['name'], request.form['description'], request.form['ministry'],
            request.form['category'], request.form['state'], request.form['min_age'],
            request.form['max_age'], request.form['max_income'], request.form['gender'],
            request.form['occupation'], request.form['benefits'], request.form['source'], id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('admin.dashboard'))
        
    # GET request: fetch existing data to pre-fill the form
    scheme = conn.execute('SELECT * FROM schemes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('admin/edit_scheme.html', scheme=scheme)

@admin_bp.route('/schemes/delete/<int:id>', methods=['POST'])
def delete_scheme(id):
    """Securely deletes a scheme (and its linked documents via CASCADE)."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM schemes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.dashboard'))