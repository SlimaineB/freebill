import sqlite3
from db_setup import DB_FILE

def add_facture(client_id, date, total_ht, total_tva, total_ttc):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO factures (client_id, date, total_ht, total_tva, total_ttc) VALUES (?, ?, ?, ?, ?)", 
                   (client_id, date, total_ht, total_tva, total_ttc))
    conn.commit()
    conn.close()

def get_factures(filter_client=None, filter_date=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT f.id, c.nom, f.date, f.total_ht, f.total_tva, f.total_ttc FROM factures f INNER JOIN clients c ON f.client_id = c.id"
    params = []

    if filter_client:
        query += " WHERE c.nom LIKE ?"
        params.append(f"%{filter_client}%")

    if filter_date:
        query += " AND f.date = ?" if filter_client else " WHERE f.date = ?"
        params.append(filter_date)

    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result
