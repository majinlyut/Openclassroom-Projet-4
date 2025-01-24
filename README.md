Migration des Données Médicales vers MongoDB avec Docker 

Contexte

Ce projet vise à migrer un dataset de données médicales de patients vers MongoDB à l'aide de Docker, pour garantir la portabilité, la scalabilité, et l'optimisation des ressources. Le déploiement se fait ensuite sur AWS pour assurer la gestion des données dans un environnement Cloud sécurisé et évolutif.

Objectifs

- Migrer un fichier CSV contenant des données médicales vers une base de données MongoDB.
- Utiliser Docker pour conteneuriser MongoDB et le script de migration, garantissant ainsi une solution portable et scalable.
- Mettre en place un déploiement sur AWS pour exploiter les services cloud comme Amazon RDS, DocumentDB, ECS et S3.

Technologies Utilisées

- MongoDB : Base de données NoSQL idéale pour stocker des données semi-structurées, telle que celles contenues dans le dataset.
- Docker : Conteneurisation de l’application pour faciliter le déploiement, la gestion des environnements et assurer la portabilité.
- Python : Langage de programmation utilisé pour le script de migration des données.
- AWS : Déploiement sur le Cloud avec des services comme Amazon ECS (Elastic Container Service) et Amazon RDS ou DocumentDB pour MongoDB.
- Pandas : Librairie Python utilisée pour manipuler et traiter les données du CSV.
- Pymongo : Librairie Python utilisée pour interagir avec MongoDB.
- Pytest : Librairie Python utilisée pour tester la migration

Structure du Projet

.
├── app/
│   ├── migration.py          # Script de migration des données vers MongoDB
│   ├──clean_data.py          #Script nettoyage
├── data/
│   └── healthcare_dataset.csv # Dataset des patients (CSV)
├── tests/
│   └──test_migration.py      #Script test migration
├── Dockerfile                # Fichier de configuration Docker pour l'application
├── docker-compose.yml        # Fichier Docker Compose pour orchestrer les conteneurs
├── requirements.txt          # Liste des dépendances Python à installer
└── README.md                 # Documentation du projet

Installation

1. Pré-requis

Avant de commencer, assurez-vous d’avoir les outils suivants installés sur votre machine :

- Docker : Télécharger Docker (https://www.docker.com/get-started)
- Docker Compose : Télécharger Docker Compose (https://docs.docker.com/compose/install/)
- Python (version 3.6 ou plus récente) : Télécharger Python (https://www.python.org/downloads/)

2. Cloner le projet

Clonez ce projet depuis GitHub sur votre machine locale :

git clone https://github.com/majinlyut/Openclassroom-Projet-4.git
cd Openclassroom-Projet-4

3. Nettoyer le dataset

Utilise le script clean_data pour nettoyer le dataset

python app/clean_data.py

3. Construire et démarrer les conteneurs Docker

Utilisez Docker Compose pour construire et démarrer les conteneurs MongoDB et l'application de migration :

docker-compose up --build

Cette commande :
- Crée un conteneur MongoDB basé sur l'image mongo:latest.
- Crée un conteneur Python avec les dépendances installées à partir du fichier requirements.txt.
- Monte le fichier CSV depuis le répertoire local data/ vers le conteneur.

Une fois les conteneurs démarrés, le script de migration sera exécuté et les données seront insérées dans la base MongoDB.

4. Accéder à MongoDB

MongoDB sera accessible sur le port 27017 de votre machine locale avec le compte admin. Vous pouvez vous connecter à MongoDB en utilisant un client comme MongoDB Compass ou en ligne de commande avec mongo shell :

mongosh "mongodb://admin:admin_password@localhost:27017/admin"


5. Sauvegarde des Données

La base de données MongoDB est configurée pour utiliser un volume persistant (mongo_data) afin de garantir que les données restent après le redémarrage des conteneurs.


Sécurité et Gestion des Accès

1. Authentification MongoDB

MongoDB est configuré pour autoriser l'authentification. Un utilisateur administrateur est créé avec des rôles spécifiques pour gérer les bases de données et les utilisateurs. Pour un accès en lecture seule, vous pouvez créer un utilisateur avec les rôles appropriés, par exemple :

use admin
db.createUser({
    user: "readonlyUser",
    pwd: "securePassword",
    roles: [{ role: "read", db: "Projet4" }]
})

Cela permet aux utilisateurs d’accéder aux données sans pouvoir modifier quoi que ce soit.






