import sqlite3

DB_FILE = "gestion_factures.db"


def init_db():
    """Crée la table entreprise si elle n'existe pas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
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

def get_entreprise_info():
    """Récupère les informations de l'entreprise."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entreprise LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "nom": result[1],
            "adresse": result[2],
            "telephone": result[3],
            "email": result[4],
            "siret": result[5],
            "tva": result[6],
            "rib": result[7],
            "logo": result[8]
        }
    else:
        return None

def save_entreprise_info(data):
    """Sauvegarde ou met à jour les infos de l'entreprise."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if get_entreprise_info():
        cursor.execute("""
        UPDATE entreprise SET 
             adresse = ?, telephone = ?, email = ?, 
            siret = ?, tva = ?, rib = ?, logo = ? WHERE nom = ?
        """, ( data["adresse"], data["telephone"], data["email"], 
              data["siret"], data["tva"], data["rib"], data["logo"],data["nom"]))
    else:
        cursor.execute("""
        INSERT INTO entreprise (nom, adresse, telephone, email, siret, tva, rib, logo) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data["nom"], data["adresse"], data["telephone"], data["email"], 
              data["siret"], data["tva"], data["rib"], data["logo"]))
    
    conn.commit()
    conn.close()

def reset_entreprise_info():
    """Supprime les données et réinitialise la table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entreprise")
    conn.commit()
    conn.close()


# Gestion des clients
def add_client(nom, adresse, telephone, email):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (nom, adresse, telephone, email) VALUES (?, ?, ?, ?)", 
                           (nom, adresse, telephone, email))
            return cursor.lastrowid  # Retourner l'ID du client ajouté
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return None
    

def get_clients():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme des dictionnaires
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients")
            return [dict(row) for row in cursor.fetchall()]  # Convertir en liste de dictionnaires
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []

def get_client_by_name(nom):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme des dictionnaires
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients where nom = ?", (nom,))
            return [dict(row) for row in cursor.fetchall()]  # Convertir en liste de dictionnaires
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []
    
# Gestion des fournisseurs
def add_fournisseur(nom, adresse, telephone, email):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO fournisseurs (nom, adresse, telephone, email) VALUES (?, ?, ?, ?)", 
                           (nom, adresse, telephone, email))
            return cursor.lastrowid  # Retourner l'ID du fournisseur ajouté
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return None

def get_fournisseurs():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fournisseurs")
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []


def get_all_clients_fournisseurs():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Récupérer les clients
            cursor.execute("SELECT id, nom, adresse, telephone, email FROM clients")
            clients = [{"ID": row[0], "Nom": row[1], "Adresse": row[2], "Téléphone": row[3], "Email": row[4], "Type": "Client"} for row in cursor.fetchall()]

            # Récupérer les fournisseurs
            cursor.execute("SELECT id, nom, adresse, telephone, email FROM fournisseurs")
            fournisseurs = [{"ID": row[0], "Nom": row[1], "Adresse": row[2], "Téléphone": row[3], "Email": row[4], "Type": "Fournisseur"} for row in cursor.fetchall()]

        return clients + fournisseurs  # Fusionner les listes
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []


def add_facture(client_id, date, total_ht, total_tva, total_ttc):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO factures (client_id, date, total_ht, total_tva, total_ttc) VALUES (?, ?, ?, ?, ?)", 
                   (client_id, date, total_ht, total_tva, total_ttc))
    conn.commit()
    conn.close()

def get_factures(filter_client=None, filter_date=None):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT f.id, c.nom, f.date, f.total_ht, f.total_tva, f.total_ttc 
                FROM factures f 
                INNER JOIN clients c ON f.client_id = c.id
            """
            params = []

            if filter_client:
                query += " WHERE c.nom LIKE ?"
                params.append(f"%{filter_client}%")

            if filter_date:
                query += " AND f.date = ?" if filter_client else " WHERE f.date = ?"
                params.append(filter_date)

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []
