import os
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Récupérer l'URI MongoDB depuis les variables d'environnement
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

# Connexion à la base de données
db = client['Projet4']
collection = db['patients']

# Lecture du fichier CSV
csv_file = "/app/data/healthcare_dataset.csv"
data = pd.read_csv(csv_file, delimiter=";")

# Changer la première colonne (par exemple "Name") pour mettre des majuscules au début de chaque mot
data["Name"] = data["Name"].str.title()

# Fonction simple pour nettoyer et séparer la chaîne
def clean_and_split(text):
    # Enlever "and" au début de la chaîne
    text = text.lstrip("and ").strip()
    
    # Supprimer la virgule à la fin, si elle existe
    text = text.rstrip(",")
    
    # Remplacer "and" par une virgule et séparer les éléments en liste
    return [item.strip() for item in text.replace(" and ", ",").split(",")]

# Appliquer la fonction sur la colonne 'Hospital'
data['Hospital'] = data['Hospital'].apply(clean_and_split)

# Fonction de conversion de date en ISO 8601 sans les heures
def convert_date_to_iso(date_str):
    try:
        # Convertir une date de format "DD/MM/YYYY" en format datetime

        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None  # Gérer les dates invalides

# Appliquer la conversion sur les colonnes contenant des dates
data["Date of Admission"] = data["Date of Admission"].apply(convert_date_to_iso)
data["Discharge Date"] = data["Discharge Date"].apply(convert_date_to_iso)

# Arrondir la colonne "Billing Amount" à 2 chiffres après la virgule
data["Billing Amount"] = data["Billing Amount"].round(2)

# Supprimer les doublons en fonction des colonnes "Name" et "Billing Amount"
data = data.drop_duplicates(subset=["Name", "Billing Amount"], keep="first")

# Conversion de chaque ligne en dictionnaire pour MongoDB
patients_data = data.to_dict(orient='records')



# Insertion des données dans MongoDB
collection.insert_many(patients_data)
print(data.count())

print("Données insérées avec succès.")
