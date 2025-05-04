from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
import service.db_service as db_service

def generate_pdf(client, date, lignes, total_ht, total_tva, total_ttc, facture_num):
    config = db_service.get_entreprise_info()
    filename = f"facture_{facture_num}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    # Affichage du logo
    if config["logo"]:
        logo = ImageReader(config["logo"])
        c.drawImage(logo, 50, 750, width=100, height=50)  # ✅ Descendre légèrement le logo

    # Infos entreprise
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, 770, config["nom"])  # ✅ Réserver plus d’espace en baissant la zone entreprise
    c.setFont("Helvetica", 12)
    c.drawString(180, 750, config["adresse"])
    c.drawString(180, 730, f"Tél : {config['telephone']} | Email : {config['email']}")
    c.drawString(180, 710, f"SIRET : {config['siret']} | TVA : {config['tva']}")

    # Infos facture
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 680, f"Facture N° {facture_num}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 660, f"Client : {client}")
    c.drawString(50, 640, f"Date : {date}")

    # Ajuster la position du tableau dynamiquement
    y_start_table = 600 - (len(lignes) * 10)  # ✅ Calcul dynamique en fonction du nombre de lignes

    if y_start_table < 400:  # ✅ Si trop bas, nouvelle page
        c.showPage()  # ✅ Crée une nouvelle page
        y_start_table = 650  # ✅ Repositionne le tableau plus haut

    # Tableau des lignes
    data = [["Description", "Quantité", "Montant Unitaire (€)", "TVA (%)", "Total TTC (€)"]]
    for ligne in lignes:
        data.append([ligne["Description"], str(ligne["Quantité"]), f"{ligne['Montant Unitaire']:.2f}", str(ligne["TVA"]), f"{ligne['Total TTC']:.2f}"])

    table = Table(data, colWidths=[150, 50, 100, 50, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSize', (0, 0), (-1, -1), 10)  # ✅ Réduction légère de la taille du texte pour économiser de l’espace
    ]))

    table.wrapOn(c, 50, y_start_table)
    table.drawOn(c, 50, y_start_table - 30)  # ✅ Descendre le tableau de 30 pixels pour éviter l'écrasement

    # Totaux
    y_total = y_start_table - (len(lignes) * 15) - 50  # ✅ Ajuster la position des totaux dynamiquement
    if y_total < 200:  # ✅ Si trop bas, on crée une nouvelle page
        c.showPage()
        y_total = 650

    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y_total, f"Total HT : {total_ht:.2f} €")
    c.drawString(400, y_total - 20, f"Total TVA : {total_tva:.2f} €")
    c.drawString(400, y_total - 40, f"Total TTC : {total_ttc:.2f} €")

    # RIB
    c.drawString(50, y_total - 80, f"⚡ Paiement : {config['rib']}")

    # Sauvegarde du PDF
    c.save()
    print(f"✅ Facture PDF générée avec succès ! Fichier : {filename}")
