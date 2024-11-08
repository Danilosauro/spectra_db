import sqlite3

def init_db():
   
    conn = sqlite3.connect('spectra_db.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spectra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        FILENAME TEXT,
        PEPMASS REAL,
        CHARGE TEXT,
        UNPD_ID TEXT,
        MOLECULAR_FORMULA TEXT,
        IONMODE TEXT,
        EXACTMASS REAL,
        NAME TEXT,
        SMILES TEXT,
        INCHI TEXT,
        INCHIAUX TEXT,
        SCANS INTEGER,
        MZ REAL,
        INTENSITY REAL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
