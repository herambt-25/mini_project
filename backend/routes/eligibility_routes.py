import sqlite3
import os
from flask import Blueprint, render_template
from services.eligibility import check_single_scheme_eligibility

eligibility_bp = Blueprint('eligibility', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schemes.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

@eligibility_bp.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    
    # 1. Get the most recently created user profile (for testing purposes)
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()
    
    if not user:
        conn.close()
        return "No user profile found! Please create a profile first."

    # 2. Get all schemes
    schemes = conn.execute('SELECT * FROM schemes').fetchall()
    conn.close()

    eligible_schemes = []
    ineligible_schemes = []

    # 3. Run the Eligibility Engine for every scheme
    for scheme in schemes:
        result = check_single_scheme_eligibility(user, scheme)
        if result['is_eligible']:
            eligible_schemes.append(result)
        else:
            ineligible_schemes.append(result)

    # 4. Send the data to the HTML template
    return render_template('dashboard.html', 
                           user=user, 
                           eligible_schemes=eligible_schemes, 
                           ineligible_schemes=ineligible_schemes)