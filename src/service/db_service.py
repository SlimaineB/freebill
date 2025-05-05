import sqlite3

DB_FILE = "gestion_factures.db"


def init_db():
    """Crée la table entreprises si elle n'existe pas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ✅ Table Entreprises (mise à jour pour gérer plusieurs entreprises)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entreprises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE,
        adresse TEXT,
        telephone TEXT,
        email TEXT,
        siret TEXT,
        tva TEXT,
        rib TEXT,
        logo TEXT,
        tjm REAL DEFAULT 0.0,
        libelle_court TEXT DEFAULT ""
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
        entreprise_id INTEGER,
        client_id INTEGER,
        date TEXT,
        total_ht REAL,
        total_tva REAL,
        total_ttc REAL,
        FOREIGN KEY (client_id) REFERENCES clients(id) , 
        FOREIGN KEY (entreprise_id) REFERENCES entreprises(id)
    )
    """)

    # Table des Notes de Frais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS frais (
        id INTEGER PRIMARY KEY,
        date DATE,
        type TEXT,
        montant_ttc REAL,
        tva REAL,
        montant_ht REAL,
        description TEXT,
        mode_paiement TEXT,
        justificatif TEXT
    )
    """)


    conn.commit()
    conn.close()

def get_entreprises():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme des dictionnaires
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM entreprises")
            return [dict(row) for row in cursor.fetchall()]  # Convertir en liste de dictionnaires
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []

def get_entreprise_by_name(nom):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme des dictionnaires
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM entreprises where nom = ? LIMIT 1", (nom,))
            return [dict(row) for row in cursor.fetchall()]  # Convertir en liste de dictionnaires
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []

def save_entreprise(data):
    """Ajoute ou met à jour une entreprise."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            if get_entreprise_by_name(data["nom"]):
                cursor.execute("""
                UPDATE entreprises SET adresse=?, telephone=?, email=?, siret=?, tva=?, rib=?, logo=?, tjm=?, libelle_court=? 
                WHERE nom=?
                """, (data["adresse"], data["telephone"], data["email"], data["siret"], data["tva"], 
                      data["rib"], data["logo"], data["tjm"], data["libelle_court"], data["nom"]))
            else:
                cursor.execute("""
                INSERT INTO entreprises (nom, adresse, telephone, email, siret, tva, rib, logo, tjm, libelle_court) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (data["nom"], data["adresse"], data["telephone"], data["email"], data["siret"], 
                      data["tva"], data["rib"], data["logo"], data["tjm"], data["libelle_court"]))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")


def delete_entreprise(nom):
    """Supprime une entreprise spécifique."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM entreprises WHERE nom = ?", (nom,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")



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
            cursor.execute("SELECT * FROM clients where nom = ? LIMIT 1", (nom,))
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


def add_facture(entreprise_id, client_id, date, total_ht, total_tva, total_ttc):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO factures (entreprise_id, client_id, date, total_ht, total_tva, total_ttc) VALUES (?, ?, ?, ?, ?, ?)", 
                   (entreprise_id, client_id, date, total_ht, total_tva, total_ttc))
    conn.commit()
    conn.close()

def get_factures(filter_client=None, filter_date=None):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT f.id, e.nom, c.nom, f.date, f.total_ht, f.total_tva, f.total_ttc 
                FROM factures f 
                INNER JOIN clients c ON f.client_id = c.id
                INNER JOIN entreprises e ON f.entreprise_id = e.id
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


def add_frais(date, type_frais, montant_ttc, tva, montant_ht, description, mode_paiement, justificatif):
    """Ajoute une note de frais en BDD avec la date en format DATE."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO frais (date, type, montant_ttc, tva, montant_ht, description, mode_paiement, justificatif) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, type_frais, montant_ttc, tva, montant_ht, description, mode_paiement, justificatif))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return None


def get_frais():
    """Récupère toutes les notes de frais stockées en BDD."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM frais")
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return []

def update_frais(frais_data):
    """Met à jour les notes de frais sans bidouiller les dates."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            for frais in frais_data:
                cursor.execute("""
                UPDATE frais SET date=?, type=?, montant_ttc=?, tva=?, montant_ht=?, 
                description=?, mode_paiement=?, justificatif=? WHERE id=?
                """, (frais["date"], frais["type"], frais["montant_ttc"], frais["tva"], frais["montant_ht"],
                      frais["description"], frais["mode_paiement"], frais["justificatif"], frais["id"]))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
