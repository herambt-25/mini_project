import sqlite3
import os
from flask import Blueprint, render_template, request
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
    """Displays the user's eligibility dashboard and recent search history."""
    conn = get_db_connection()
    
    # 1. Get the current user
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()
    
    if not user:
        conn.close()
        return "No user profile found! Please create a profile first."

    # 2. Get all schemes
    schemes = conn.execute('SELECT * FROM schemes').fetchall()
    

    eligible_schemes = []
    ineligible_schemes = []

    # 3. Run the Eligibility Engine
    for scheme in schemes:
        result = check_single_scheme_eligibility(user, scheme)
        if result['is_eligible']:
            eligible_schemes.append(result)
        else:
            ineligible_schemes.append(result)

    # 4. Fetch the user's 5 most recent searches
    recent_searches = conn.execute('''
        SELECT * FROM search_history 
        WHERE user_id = ? 
        ORDER BY search_date DESC LIMIT 5
    ''', (user['id'],)).fetchall()
    
    conn.close()

    # 6. Send the data to the HTML template
    return render_template('dashboard.html', 
                           user=user, 
                           eligible_schemes=eligible_schemes, 
                           ineligible_schemes=ineligible_schemes,
                           recent_searches=recent_searches)

@eligibility_bp.route('/report')
def generate_report():
    """Generates a complete, printable personalized report for the user."""
    conn = get_db_connection()
    
    # Get the current user
    user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()
    if not user:
        conn.close()
        return "No user profile found! Please create a profile first."

    # Get all schemes
    schemes = conn.execute('SELECT * FROM schemes').fetchall()
    conn.close()

    eligible_schemes = []
    ineligible_schemes = []

    # Run the eligibility engine
    for scheme in schemes:
        result = check_single_scheme_eligibility(user, scheme)
        if result['is_eligible']:
            eligible_schemes.append(result)
        else:
            ineligible_schemes.append(result)

    # Render the report template
    return render_template('report.html', 
                           user=user, 
                           eligible_schemes=eligible_schemes, 
                           ineligible_schemes=ineligible_schemes)

@eligibility_bp.route('/simulator')
def simulator():
    """Interactive tool to test how different attributes affect eligibility without saving to the DB."""
    conn = get_db_connection()
    
    # Try to get the existing user to use as a realistic starting point
    base_user = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1').fetchone()
    
    # Grab simulated values from URL, fallback to base_user, or fallback to generic defaults
    sim_age = int(request.args.get('age', base_user['age'] if base_user else 25))
    sim_income = float(request.args.get('income', base_user['annual_income'] if base_user else 100000))
    sim_gender = request.args.get('gender', base_user['gender'] if base_user else 'Female')
    sim_state = request.args.get('state', base_user['state'] if base_user else 'Maharashtra')
    sim_occupation = request.args.get('occupation', base_user['occupation'] if base_user else 'Student')
    
    # Build a temporary "mock" user profile in memory
    mock_user = {
        'age': sim_age,
        'annual_income': sim_income,
        'gender': sim_gender,
        'state': sim_state,
        'occupation': sim_occupation
    }
    
    schemes = conn.execute('SELECT * FROM schemes').fetchall()
    conn.close()
    
    eligible_schemes = []
    
    # Run the engine purely in memory
    for scheme in schemes:
        result = check_single_scheme_eligibility(mock_user, scheme)
        if result['is_eligible']:
            eligible_schemes.append(result)
            
    return render_template('simulator.html', 
                           mock_user=mock_user, 
                           eligible_schemes=eligible_schemes)