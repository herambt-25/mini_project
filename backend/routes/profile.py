import sqlite3
import os
from flask import Blueprint, request, render_template, redirect, url_for

# Initialize the profile blueprint
profile_bp = Blueprint('profile', __name__)

# Locate the SQLite database relative to this file
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schemes.db')

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Handles displaying the user profile form (GET)
    and storing the user's data in SQLite (POST).
    """
    if request.method == 'POST':
        # Retrieve form data submitted from profile.html
        name = request.form.get('name')
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender')
        state = request.form.get('state')
        income = float(request.form.get('income', 0.0))
        occupation = request.form.get('occupation')
        
        # Insert user profile into SQLite database using parameterized queries
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, age, gender, state, annual_income, occupation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, state, income, occupation))
        
        conn.commit()
        conn.close()
        
        # Redirect user immediately to the eligibility dashboard
        return redirect(url_for('eligibility.dashboard'))

    # Render the blank profile form on GET request
    return render_template('profile.html')