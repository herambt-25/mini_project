-- Drop tables if they exist so we can start fresh
DROP TABLE IF EXISTS search_history;
DROP TABLE IF EXISTS scheme_documents;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS schemes;
DROP TABLE IF EXISTS admins;

-- Users Table: Stores citizen profiles
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    state TEXT,
    district TEXT,
    annual_income REAL,
    occupation TEXT,
    category TEXT,
    is_student BOOLEAN DEFAULT 0,
    language_pref TEXT DEFAULT 'en'
);

-- Schemes Table: Stores government schemes and eligibility rules
CREATE TABLE schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    description_en TEXT,
    ministry TEXT,
    category TEXT,
    state_applicability TEXT DEFAULT 'All', -- 'All' means central scheme
    min_age INTEGER DEFAULT 0,
    max_age INTEGER DEFAULT 150,
    max_income REAL,
    target_gender TEXT DEFAULT 'All',
    target_occupation TEXT,
    benefits_en TEXT,
    official_source TEXT
);

-- Scheme Documents Table
CREATE TABLE scheme_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_id INTEGER,
    document_name_en TEXT NOT NULL,
    FOREIGN KEY (scheme_id) REFERENCES schemes (id) ON DELETE CASCADE
);

-- Admins Table
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Search History Table
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    search_query TEXT,
    category_filter TEXT,
    state_filter TEXT,
    search_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);