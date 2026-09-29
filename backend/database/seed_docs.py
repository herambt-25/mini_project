import sqlite3
import os

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemes.db')

def seed_documents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear old documents just in case
    cursor.execute("DELETE FROM scheme_documents")

    # A list of documents linked to scheme IDs (1 to 8)
    docs = [
        (1, 'Aadhaar Card'), (1, 'Recent Electricity Bill'), (1, 'Bank Passbook'),
        (2, 'Aadhaar Card'), (2, 'Domicile Certificate (Maharashtra)'), (2, 'Bank Account Linked with Aadhaar'), (2, 'Income Certificate'),
        (3, 'Aadhaar Card'), (3, 'Skill Certificate / Artisan Proof'), (3, 'Bank Account Details'),
        (4, 'Aadhaar Card'), (4, 'Vending Certificate / ID Card'), (4, 'Bank Passbook'),
        (5, 'Aadhaar Card'), (5, 'Land Ownership Records (7/12 extract)'), (5, 'Active Bank Account'),
        (6, 'Birth Certificate of Girl Child'), (6, 'Parent/Guardian Identity Proof'), (6, 'Address Proof'),
        (7, 'Aadhaar Card'), (7, 'Savings Bank Account'),
        (8, 'Aadhaar Card'), (8, 'Ration Card'), (8, 'Income Certificate')
    ]

    for scheme_id, doc_name in docs:
        cursor.execute('''
            INSERT INTO scheme_documents (scheme_id, document_name_en) 
            VALUES (?, ?)
        ''', (scheme_id, doc_name))

    conn.commit()
    print("✅ Successfully added required documents to the database!")
    conn.close()

if __name__ == '__main__':
    seed_documents()