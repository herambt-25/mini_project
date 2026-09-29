import sqlite3
import os

# Safely locate the database file. 
# __file__ is seed_data.py, so dirname(__file__) is the 'database' folder.
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemes.db')

def seed_schemes():
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing schemes so we don't get duplicates if you run this twice
    cursor.execute("DELETE FROM schemes")
    
    # Our list of real, verified government schemes
    schemes = [
        {
            "name_en": "PM Surya Ghar Muft Bijli Yojana",
            "description_en": "Provides subsidy for installing rooftop solar panels to provide free electricity.",
            "ministry": "Ministry of New and Renewable Energy",
            "category": "Infrastructure",
            "state_applicability": "All",
            "min_age": 21,
            "max_age": 75,
            "max_income": 0, 
            "target_gender": "All",
            "target_occupation": "All",
            "benefits_en": "Up to Rs. 78,000 subsidy for rooftop solar.",
            "official_source": "https://pmsuryaghar.gov.in"
        },
        {
            "name_en": "Mukhyamantri Majhi Ladki Bahin Yojana",
            "description_en": "Financial assistance for women in Maharashtra to improve health and nutrition.",
            "ministry": "Women and Child Development",
            "category": "Women",
            "state_applicability": "Maharashtra",
            "min_age": 21,
            "max_age": 65,
            "max_income": 250000,
            "target_gender": "Female",
            "target_occupation": "All",
            "benefits_en": "Financial Assistance of Rs 1,500 per month.",
            "official_source": "https://ladakibahin.maharashtra.gov.in"
        },
        {
            "name_en": "PM Vishwakarma Scheme",
            "description_en": "Support for traditional artisans and craftspeople through collateral-free loans.",
            "ministry": "Ministry of MSME",
            "category": "Employment",
            "state_applicability": "All",
            "min_age": 18,
            "max_age": 150,
            "max_income": 0, 
            "target_gender": "All",
            "target_occupation": "Artisan",
            "benefits_en": "Collateral-free loans up to Rs 3 lakh at 5% interest.",
            "official_source": "https://pmvishwakarma.gov.in"
        },
        {
            "name_en": "PM SVANidhi",
            "description_en": "Micro-credit facility for street vendors to resume their livelihoods.",
            "ministry": "Ministry of Housing and Urban Affairs",
            "category": "Entrepreneurship",
            "state_applicability": "All",
            "min_age": 18,
            "max_age": 150,
            "max_income": 0,
            "target_gender": "All",
            "target_occupation": "Street Vendor",
            "benefits_en": "Working capital loan up to Rs 50,000.",
            "official_source": "https://pmsvanidhi.mohua.gov.in"
        },
        {
            "name_en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "description_en": "Income support to all landholding farmer families.",
            "ministry": "Ministry of Agriculture",
            "category": "Agriculture",
            "state_applicability": "All",
            "min_age": 18,
            "max_age": 150,
            "max_income": 0,
            "target_gender": "All",
            "target_occupation": "Farmer",
            "benefits_en": "Rs 6,000 per year in three equal installments.",
            "official_source": "https://pmkisan.gov.in"
        },
        {
            "name_en": "Sukanya Samriddhi Yojana",
            "description_en": "A small deposit scheme for the girl child to fund her education and marriage.",
            "ministry": "Ministry of Finance",
            "category": "Financial Assistance",
            "state_applicability": "All",
            "min_age": 0,
            "max_age": 10, 
            "max_income": 0,
            "target_gender": "Female",
            "target_occupation": "All",
            "benefits_en": "High interest rate savings account with tax benefits.",
            "official_source": "https://www.nsiindia.gov.in"
        },
        {
            "name_en": "Atal Pension Yojana",
            "description_en": "A pension scheme focused on unorganized sector workers.",
            "ministry": "Ministry of Finance",
            "category": "Senior Citizens",
            "state_applicability": "All",
            "min_age": 18,
            "max_age": 40,
            "max_income": 0,
            "target_gender": "All",
            "target_occupation": "All",
            "benefits_en": "Guaranteed minimum pension of Rs 1,000 to Rs 5,000 per month after age 60.",
            "official_source": "https://npscra.nsdl.co.in/scheme-details.php"
        },
        {
            "name_en": "Ayushman Bharat PM-JAY",
            "description_en": "Provides health cover per family per year for secondary and tertiary care.",
            "ministry": "Ministry of Health and Family Welfare",
            "category": "Healthcare",
            "state_applicability": "All",
            "min_age": 0,
            "max_age": 150,
            "max_income": 0, 
            "target_gender": "All",
            "target_occupation": "All",
            "benefits_en": "Health cover of Rs. 5 lakhs per family per year.",
            "official_source": "https://pmjay.gov.in"
        }
    ]

    # Loop through the list and insert each one into the database
    for s in schemes:
        cursor.execute('''
            INSERT INTO schemes 
            (name_en, description_en, ministry, category, state_applicability, min_age, max_age, max_income, target_gender, target_occupation, benefits_en, official_source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            s['name_en'], s['description_en'], s['ministry'], s['category'], 
            s['state_applicability'], s['min_age'], s['max_age'], 
            s['max_income'], s['target_gender'], s['target_occupation'], 
            s['benefits_en'], s['official_source']
        ))

    conn.commit()
    print(f"✅ Successfully seeded {len(schemes)} schemes into the database!")
    conn.close()

if __name__ == '__main__':
    seed_schemes()