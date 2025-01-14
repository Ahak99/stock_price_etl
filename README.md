# Projet : Pipeline ETL pour l'analyse de l'indice S&P500 🚀📊

## Description du projet 🌟

Ce projet vise à développer et à orchestrer une pipeline ETL (Extraction, Transformation, Chargement) pour la collecte et le traitement des données liées à l'indice S&P500 et aux actions qui le composent. 
L'objectif est de fournir une solution automatisée pour analyser et transformer des données financières en formats exploitables pour les équipes décisionnelles. 💡

## Fonctionnalités principales ✨

- **Analyse des besoins fonctionnels** : Identification des flux de données et des exigences techniques.
- **Extraction des données** : Utilisation de l'API Yahoo Finance pour collecter des informations sur l'indice S&P500 et les actions associées.
- **Transformation et analyse des données** : Utilisation de Python, Pandas, et Numpy pour nettoyer, transformer, et analyser les données.
- **Orchestration de pipeline** : Mise en place d'une pipeline ETL automatisée à l'aide d'Apache Airflow.
- **Déploiement cloud** : Création et gestion d'un environnement cloud complet sur AWS grâce à Terraform :
  - EC2 pour l'hébergement d'Apache Airflow et des scripts Python.
  - S3 pour le stockage des données brutes et transformées.

## Technologies utilisées 🛠️

- **Langages** : Python 🐍
- **Bibliothèques** : Pandas, Numpy 📚
- **Orchestration ETL** : Apache Airflow 🌀
- **Infrastructure Cloud** : AWS (EC2, S3) ☁️
- **Infrastructure as Code** : Terraform 🏗️
- **API** : Yahoo Finance API 🌐
- **Gestion de version** : Git 🧰

## Prérequis ✅

- **Python 3.x**
- **Terraform**
- **AWS CLI** configuré avec des accès appropriés
- **Apache Airflow**

## Installation ⚙️

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Ahak99/stock_price_etl.git
   cd stock_price_etl
   ```

2. **Installer les dépendances Python** :
   ```bash
   pip install -r src/stock_price_etl/requirements.txt
   ```

3. **Configurer l'environnement AWS avec Terraform** :
   - Naviguez dans le répertoire `terraform`.
   - Initialisez Terraform :
     ```bash
     terraform init
     ```
   - Appliquez la configuration pour déployer l'infrastructure :
     ```bash
     terraform apply
     ```

4. **Configurer Apache Airflow** :
   - Installer Airflow si ce n'est pas déjà fait.
   - Ajouter les DAGs au répertoire Airflow.
   - Lancer le service Airflow :
     ```bash
     airflow standalone
     ```

## Utilisation 🚀

1. **Lancer la pipeline ETL** :
   - Accédez à l'interface web d'Airflow.
   - Activez et exécutez le DAG correspondant.

2. **Vérification des données** :
   - Les données brutes et transformées seront disponibles dans le bucket S3 configuré.
