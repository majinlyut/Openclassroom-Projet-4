import pandas as pd

csv_file = "data/healthcare_dataset.csv"  # Chemin vers le fichier
data = pd.read_csv(csv_file, delimiter=";")
print(data.head())  # Affiche les premières lignes pour vérifier
