import sqlite3
import os
import re 
from flask import Blueprint, render_template, request

scheme_bp = Blueprint('scheme', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schemes.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@scheme_bp.route('/schemes')
def all_schemes():
    """Fetches and displays schemes, with optional search and filtering."""
    conn = get_db_connection()
    
    search_query = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '')
    state_filter = request.args.get('state', '')

    # NEW: Save to search history if the user actively applied a filter
    if search_query or category_filter or state_filter:
        user = conn.execute('SELECT id FROM users ORDER BY id DESC LIMIT 1').fetchone()
        if user:
            conn.execute('''
                INSERT INTO search_history (user_id, search_query, category_filter, state_filter)
                VALUES (?, ?, ?, ?)
            ''', (user['id'], search_query, category_filter, state_filter))
            conn.commit()

    sql = "SELECT * FROM schemes WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (name_en LIKE ? OR description_en LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    
    if category_filter:
        sql += " AND category = ?"
        params.append(category_filter)
        
    if state_filter:
        sql += " AND state_applicability = ?"
        params.append(state_filter)

    schemes = conn.execute(sql, params).fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM schemes").fetchall()
    states = conn.execute("SELECT DISTINCT state_applicability FROM schemes").fetchall()
    
    conn.close()
    
    return render_template(
        'schemes.html', 
        schemes=schemes, 
        categories=categories, 
        states=states,
        current_q=search_query,
        current_cat=category_filter,
        current_state=state_filter
    )

@scheme_bp.route('/scheme/<int:scheme_id>')
def scheme_detail(scheme_id):
    """Fetches and displays details for one specific scheme, including docs and benefits."""
    conn = get_db_connection()
    scheme = conn.execute('SELECT * FROM schemes WHERE id = ?', (scheme_id,)).fetchone()
    
    if scheme is None:
        conn.close()
        return "Scheme not found!", 404
        
    # 1. Fetch the required documents for this scheme
    documents = conn.execute('SELECT * FROM scheme_documents WHERE scheme_id = ?', (scheme_id,)).fetchall()
    conn.close()
    
    # 2. Annual Benefit Calculator Logic
    annual_benefit = None
    benefits_text = scheme['benefits_en'].lower()
    
    # Check if the benefit is monthly
    if 'per month' in benefits_text or 'a month' in benefits_text:
        # Find all numbers in the text (e.g., "1,500" or "1500")
        numbers = re.findall(r'\d+,\d+|\d+', benefits_text)
        if numbers:
            # Remove commas and convert to integer
            monthly_amount = int(numbers[0].replace(',', ''))
            annual_benefit = monthly_amount * 12

    return render_template('scheme_detail.html', scheme=scheme, documents=documents, annual_benefit=annual_benefit)

@scheme_bp.route('/compare')
def compare_schemes():
    """Displays a side-by-side comparison of two selected schemes."""
    conn = get_db_connection()
    
    # 1. Fetch all scheme names for the dropdown menus
    all_schemes = conn.execute('SELECT id, name_en FROM schemes ORDER BY name_en').fetchall()
    
    # 2. Get the selected IDs from the URL (if any)
    id1 = request.args.get('scheme1')
    id2 = request.args.get('scheme2')
    
    scheme1_data = None
    scheme2_data = None
    
    # 3. If the user selected two schemes, fetch their full details
    if id1 and id2:
        scheme1_data = conn.execute('SELECT * FROM schemes WHERE id = ?', (id1,)).fetchone()
        scheme2_data = conn.execute('SELECT * FROM schemes WHERE id = ?', (id2,)).fetchone()
        
    conn.close()
    
    return render_template('comparison.html', 
                           all_schemes=all_schemes,
                           scheme1=scheme1_data,
                           scheme2=scheme2_data,
                           sel_id1=int(id1) if id1 and id1.isdigit() else '',
                           sel_id2=int(id2) if id2 and id2.isdigit() else '')