import psycopg2
from psycopg2 import sql

def init_db():
    conn = psycopg2.connect(
        dbname="spectra_db",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"  
    )
    cursor = conn.cursor()

    # spectra table for user personal data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spectra (
        id SERIAL PRIMARY KEY,
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

    # unpd table for unpd data
    cursor.execute('''
    DROP TABLE IF EXISTS UNPD;
    CREATE TABLE IF NOT EXISTS UNPD (
        id SERIAL PRIMARY KEY,
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
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
