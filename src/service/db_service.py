import sqlite3
from service.db_setup import DB_FILE

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
            nom = ?, adresse = ?, telephone = ?, email = ?, 
            siret = ?, tva = ?, rib = ?, logo = ? WHERE id = 1
        """, (data["nom"], data["adresse"], data["telephone"], data["email"], 
              data["siret"], data["tva"], data["rib"], data["logo"]))
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
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (nom, adresse, telephone, email) VALUES (?, ?, ?, ?)", 
                   (nom, adresse, telephone, email))
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    result = cursor.fetchall()
    conn.close()
    return result

# Gestion des fournisseurs
def add_fournisseur(nom, adresse, telephone, email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fournisseurs (nom, adresse, telephone, email) VALUES (?, ?, ?, ?)", 
                   (nom, adresse, telephone, email))
    conn.commit()
    conn.close()

def get_fournisseurs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fournisseurs")
    result = cursor.fetchall()
    conn.close()
    return result
