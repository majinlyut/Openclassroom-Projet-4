import os
import pandas as pd
from datetime import datetime

def clean_and_split(text):
    text = text.lstrip("and ").strip()
    text = text.rstrip(",")
    return [item.strip() for item in text.replace(" and ", ",").split(",")]

def convert_date_to_iso(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return None

def clean_data(input_file, output_file):
    # Lire le fichier CSV d'entrée
    data = pd.read_csv(input_file, delimiter=";")

    # Nettoyage des données
    data["Name"] = data["Name"].str.title()
    data['Hospital'] = data['Hospital'].apply(clean_and_split)
    data["Date of Admission"] = data["Date of Admission"].apply(convert_date_to_iso)
    data["Discharge Date"] = data["Discharge Date"].apply(convert_date_to_iso)
    data["Billing Amount"] = data["Billing Amount"].round(2)
    data = data.drop_duplicates(subset=["Name", "Billing Amount"], keep="first")

    # Enregistrer les données nettoyées dans un fichier CSV
    data.to_csv(output_file, index=False, sep=";")
    print(f"Fichier nettoyé sauvegardé dans : {output_file}")

if __name__ == "__main__":
    # Spécifier les chemins d'entrée et de sortie
    input_file = "C:/Users/lyuta/a COURS/Projet 4/data/healthcare_dataset.csv"
    output_file = "C:/Users/lyuta/a COURS/Projet 4/data/cleaned_healthcare_dataset.csv"
    clean_data(input_file, output_file)
