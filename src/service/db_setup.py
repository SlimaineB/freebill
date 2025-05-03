import sqlite3

DB_FILE = "gestion_factures.db"

def init_db():
    """Crée les tables Clients, Fournisseurs, Entreprise et Factures si elles n'existent pas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table Entreprise
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entreprise (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        adresse TEXT,
        telephone TEXT,
        email TEXT,
        siret TEXT,
        tva TEXT,
        rib TEXT,
        logo TEXT
    )
    """)

    # Table Clients
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        adresse TEXT,
        telephone TEXT,
        email TEXT
    )
    """)

    # Table Fournisseurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fournisseurs (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        adresse TEXT,
        telephone TEXT,
        email TEXT
    )
    """)

    # Table Factures
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS factures (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        date TEXT,
        total_ht REAL,
        total_tva REAL,
        total_ttc REAL,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    conn.commit()
    conn.close()
