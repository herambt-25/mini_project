import os
from flask import Flask, render_template, session, redirect, request, url_for
import config
from routes.profile import profile_bp
from routes.eligibility_routes import eligibility_bp
from routes.scheme_routes import scheme_bp
from services.translation import translate

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

app = Flask(__name__, template_folder=FRONTEND_DIR, static_folder=FRONTEND_DIR)
app.config.from_object(config.Config)

# Register Blueprints
app.register_blueprint(profile_bp)
app.register_blueprint(eligibility_bp)
app.register_blueprint(scheme_bp)

# Context processor makes t() available in EVERY Jinja HTML template automatically
@app.context_processor
def inject_globals():
    current_lang = session.get('lang', 'en')
    
    def t(key):
        return translate(key, current_lang)
        
    return dict(t=t, current_lang=current_lang)

@app.route('/')
def home():
    """Route for the start screen."""
    return render_template('index.html')

@app.route('/set_language/<lang>')
def set_language(lang):
    """Stores language choice ('en', 'hi', or 'mr') in session and reloads current page."""
    if lang in ['en', 'hi', 'mr']:
        session['lang'] = lang
    
    # Redirect back to whichever page the user was on
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)