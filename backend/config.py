import os

class Config:
    SECRET_KEY = 'super-secret-college-project-key'
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'schemes.db')