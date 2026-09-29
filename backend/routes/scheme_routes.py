import sqlite3
import os
from flask import Blueprint, render_template

scheme_bp = Blueprint('scheme', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schemes.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@scheme_bp.route('/schemes')
def all_schemes():
    """Fetches and displays all schemes."""
    conn = get_db_connection()
    schemes = conn.execute('SELECT * FROM schemes').fetchall()
    conn.close()
    return render_template('schemes.html', schemes=schemes)

@scheme_bp.route('/scheme/<int:scheme_id>')
def scheme_detail(scheme_id):
    """Fetches and displays details for one specific scheme."""
    conn = get_db_connection()
    scheme = conn.execute('SELECT * FROM schemes WHERE id = ?', (scheme_id,)).fetchone()
    conn.close()
    
    if scheme is None:
        return "Scheme not found!", 404
        
    return render_template('scheme_detail.html', scheme=scheme)