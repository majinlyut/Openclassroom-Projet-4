import pytest
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from io import StringIO

# Connexion à MongoDB
@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient('mongodb://localhost:27017/')
    yield client
    client.close()

@pytest.fixture(scope="module")
def mongo_collection(mongo_client):
    db = mongo_client['Projet4']
    collection = db['patients']
    collection.delete_many({})  # Nettoyer la collection avant chaque test
    return collection

@pytest.fixture(scope="module")
def sample_data():
    return [
        {"Name": "John Doe", "Hospital": ["City Hospital"], "Date of Admission": "2025-01-01", "Discharge Date": "2025-01-10", "Billing Amount": 150.50},
        {"Name": "Jane Smith", "Hospital": ["Green Hospital"], "Date of Admission": "2025-01-03", "Discharge Date": "2025-01-08", "Billing Amount": 200.75}
    ]

### TEST CRUD OPERATIONS
def test_crud_operations(mongo_collection, sample_data):
    # CREATE
    mongo_collection.insert_many(sample_data)
    assert mongo_collection.count_documents({}) == 2

    # READ
    john = mongo_collection.find_one({"Name": "John Doe"})
    assert john["Billing Amount"] == 150.50

    # UPDATE
    mongo_collection.update_one({"Name": "John Doe"}, {"$set": {"Billing Amount": 175.00}})
    john = mongo_collection.find_one({"Name": "John Doe"})
    assert john["Billing Amount"] == 175.00

    # DELETE
    mongo_collection.delete_one({"Name": "Jane Smith"})
    assert mongo_collection.count_documents({}) == 1

### TEST INTEGRITY BEFORE AND AFTER MIGRATION
@pytest.fixture(scope="module")
def csv_data():
    # Exemple de données CSV simulées
    csv_content = """Name;Hospital;Date of Admission;Discharge Date;Billing Amount
    John Doe;City Hospital;01/01/2025;10/01/2025;150.50
    Jane Smith;Green Hospital;03/01/2025;08/01/2025;200.75"""
    data = pd.read_csv(StringIO(csv_content), delimiter=";")
    return data

def test_data_integrity_before_migration(csv_data):
    # Vérification des colonnes
    expected_columns = {"Name", "Hospital", "Date of Admission", "Discharge Date", "Billing Amount"}
    assert set(csv_data.columns) == expected_columns

    # Vérification des doublons
    assert csv_data.duplicated().sum() == 0

    # Vérification des valeurs manquantes
    assert csv_data.isnull().sum().sum() == 0

    # Vérification des types
    assert csv_data["Billing Amount"].dtype == float

@pytest.fixture(scope="module")
def data_after_migration(mongo_collection):
    return pd.DataFrame(list(mongo_collection.find()))

def test_data_integrity_after_migration(data_after_migration):
    # Vérification des colonnes
    expected_columns = {"_id", "Name", "Hospital", "Date of Admission", "Discharge Date", "Billing Amount"}
    assert set(data_after_migration.columns) >= expected_columns

    # Vérification des doublons
    assert data_after_migration.duplicated().sum() == 0

    # Vérification des valeurs manquantes
    assert data_after_migration.isnull().sum().sum() == 0

    # Vérification des types
    assert data_after_migration["Billing Amount"].dtype == float

### TEST AUTOMATISÉ : CONVERT DATE FUNCTION
def convert_date_to_iso(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def test_convert_date_to_iso():
    # Date valide
    valid_date = "10/01/2025"
    assert convert_date_to_iso(valid_date) == datetime(2025, 1, 10)

    # Date invalide
    invalid_date = "32/01/2025"
    assert convert_date_to_iso(invalid_date) is None

### TEST AUTOMATISÉ : CLEAN AND SPLIT FUNCTION
def clean_and_split(text):
    text = text.lstrip("and ").strip()  # Supprimer "and" au début
    text = text.rstrip(",")  # Supprimer la virgule finale
    return [item.strip() for item in text.replace(" and ", ",").split(",")]

def test_clean_and_split():
    text = "John, Jane and Jack, Mary"
    expected_output = ["John", "Jane", "Jack", "Mary"]
    assert clean_and_split(text) == expected_output

    text = "and John, Jane, Jack, Mary"
    expected_output = ["John", "Jane", "Jack", "Mary"]
    assert clean_and_split(text) == expected_output

    text = "John, Jane, Jack, Mary,"
    expected_output = ["John", "Jane", "Jack", "Mary"]
    assert clean_and_split(text) == expected_output

### TEST AUTOMATISÉ : ROUND BILLING AMOUNT
def test_round_billing_amount():
    data = pd.DataFrame({
        'Billing Amount': [100.12345, 50.6789, 123.4567]
    })
    data['Billing Amount'] = data['Billing Amount'].round(2)
    assert data['Billing Amount'][0] == 100.12
    assert data['Billing Amount'][1] == 50.68
    assert data['Billing Amount'][2] == 123.46
