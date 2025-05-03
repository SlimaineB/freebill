import pandas as pd

class ClientService:
    def __init__(self, fichier="clients.csv"):
        """Initialisation avec le fichier CSV pour stocker les clients."""
        self.fichier = fichier
        self.clients = self.load_clients()

    def load_clients(self):
        """Charge les clients à partir du fichier CSV."""
        try:
            return pd.read_csv(self.fichier)
        except FileNotFoundError:
            return pd.DataFrame(columns=["ID", "Nom", "Adresse", "SIRET", "Numéro TVA"])

    def save_clients(self):
        """Sauvegarde les clients dans le fichier CSV."""
        self.clients.to_csv(self.fichier, index=False)

    def add_client(self, nom, adresse, siret, num_tva):
        """Ajoute un nouveau client."""
        new_id = len(self.clients) + 1
        new_client = {"ID": new_id, "Nom": nom, "Adresse": adresse, "SIRET": siret, "Numéro TVA": num_tva}
        self.clients = pd.concat([self.clients, pd.DataFrame([new_client])], ignore_index=True)
        self.save_clients()
        print(f"✅ Client {nom} ajouté avec succès.")

    def delete_client(self, client_id):
        """Supprime un client par son ID."""
        if client_id in self.clients["ID"].values:
            self.clients = self.clients[self.clients["ID"] != client_id]
            self.save_clients()
            print(f"🗑️ Client ID {client_id} supprimé avec succès.")
        else:
            print("⚠️ Client non trouvé.")

# Exemple d'utilisation
if __name__ == "__main__":
    manager = ClientService()
    manager.add_client("Jean Dupont", "75 Rue des Lilas, Paris", "12345678901234", "FR12345678901")
    manager.add_client("Sophie Martin", "18 Avenue de Lyon, Lyon", "98765432109876", "FR98765432109")
    manager.delete_client(1)  # Suppression du client avec ID 1
