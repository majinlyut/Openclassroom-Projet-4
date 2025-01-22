import os
from pymongo import MongoClient
import pandas as pd

def migrate_to_mongo(input_file, mongo_uri = os.getenv("MONGO_URI"), db_name="Projet4", collection_name="patients"):
    # Connexion à MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Supprimer tous les documents existants dans la collection
    collection.delete_many({})  # Supprime tous les documents de la collection

    # Lecture du fichier CSV nettoyé
    data = pd.read_csv(input_file, delimiter=";")
    
    # Conversion des données en dictionnaires pour MongoDB
    patients_data = data.to_dict(orient='records')

    # Insertion des données dans MongoDB
    collection.insert_many(patients_data)
    print(f"Données insérées avec succès dans la collection '{collection_name}'.")

if __name__ == "__main__":
    # Spécifier le chemin du fichier CSV nettoyé
    cleaned_file = "/app/data/cleaned_healthcare_dataset.csv"  # Chemin dans le conteneur
    migrate_to_mongo(cleaned_file)