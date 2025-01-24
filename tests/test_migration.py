import os
import pytest
import pandas as pd
from pymongo import MongoClient
import random

# Connexion à la base de données MongoDB
mongo_uri = "mongodb://admin:admin_password@localhost:27017/admin?authSource=admin"
client = MongoClient(mongo_uri)
db = client['Projet4']
collection = db['patients']

# Chemin du fichier CSV nettoyé
cleaned_file_path = "data/cleaned_healthcare_dataset.csv"

# Fonction pour lire le CSV nettoyé
def read_cleaned_csv():
    return pd.read_csv(cleaned_file_path, delimiter=";")

# Fonction pour récupérer tous les documents de la collection
def get_mongo_documents():
    return list(collection.find())

def test_column_and_row_count():
    # Lire le CSV nettoyé
    data = read_cleaned_csv()

    # Liste des colonnes attendues (sans la colonne '_id')
    expected_columns = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Date of Admission',
                        'Doctor', 'Hospital', 'Insurance Provider', 'Billing Amount', 'Room Number', 
                        'Admission Type', 'Discharge Date', 'Medication', 'Test Results']
    
    # Récupérer les documents de MongoDB
    mongo_documents = get_mongo_documents()

    # Exclure la colonne '_id' des documents MongoDB
    mongo_columns = [col for col in mongo_documents[0].keys() if col != '_id']
    
    # Vérifier que les colonnes MongoDB correspondent exactement aux colonnes attendues
    assert sorted(mongo_columns) == sorted(expected_columns), f"Les colonnes MongoDB ne correspondent pas aux colonnes attendues : {mongo_columns} vs {expected_columns}"
    
    # Vérifier le nombre de lignes 
    assert len(data) == len(mongo_documents), f"Le nombre de lignes ne correspond pas : CSV ({len(data)}) vs MongoDB ({len(mongo_documents)})"

def test_random_row_integrity():
    # Lire le CSV nettoyé
    data = read_cleaned_csv()

    # Récupérer les documents de MongoDB
    mongo_documents = get_mongo_documents()

    # Choisir une ligne aléatoire du CSV
    random_row = data.sample(n=1).iloc[0]  # n=1 pour obtenir une seule ligne au hasard

    # Convertir la ligne en dictionnaire pour comparaison
    row_dict = random_row.to_dict()

    # Trouver le document MongoDB correspondant
    mongo_doc = next(
        (doc for doc in mongo_documents if doc['Name'] == random_row['Name'] and doc['Billing Amount'] == random_row['Billing Amount']),
        None
    )

    # Vérifier si le document existe
    assert mongo_doc is not None, f"Le document correspondant à {random_row['Name']} avec le montant {random_row['Billing Amount']} n'a pas été trouvé dans MongoDB"
    
    # Vérifier si les autres champs correspondent
    for column in data.columns:
        assert mongo_doc[column] == random_row[column], f"La valeur pour {column} ne correspond pas pour {random_row['Name']}"


# Test pour vérifier si la somme des montants de facturation est la même dans MongoDB et le CSV
def test_billing_sum():
    # Lire le CSV nettoyé
    data = read_cleaned_csv()

    # Récupérer les documents de MongoDB
    mongo_documents = get_mongo_documents()

    # Calculer la somme des Billing Amount dans le CSV
    csv_billing_sum = data['Billing Amount'].sum()

    # Calculer la somme des Billing Amount dans MongoDB
    mongo_billing_sum = sum(doc['Billing Amount'] for doc in mongo_documents)

    # Arrondir les sommes à 2 décimales
    csv_billing_sum = round(csv_billing_sum, 2)
    mongo_billing_sum = round(mongo_billing_sum, 2)

    # Vérifier si la somme des montants de facturation est la même
    assert csv_billing_sum == mongo_billing_sum, f"La somme des montants de facturation ne correspond pas : CSV ({csv_billing_sum}) vs MongoDB ({mongo_billing_sum})"