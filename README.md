# Projet de Vote Électronique Sécurisé

Ce projet met en place un système de vote électronique sécurisé basé sur la technologie de chiffrement PGP (Pretty Good Privacy) et Flask. Les utilisateurs peuvent voter en toute sécurité, et les résultats peuvent être déchiffrés et comptabilisés de manière transparente.

## Description

Ce projet se compose de trois parties principales :

1. **Votant** : Le module où les utilisateurs peuvent soumettre leur vote de manière sécurisée. Les votes sont chiffrés à l'aide de la clé publique du centre de comptage.
2. **Centre de Comptage** : Cette partie permet de recevoir les votes chiffrés et de les stocker dans une base de données. Elle notifie le centre de dépouillement lorsqu'un nouveau vote est enregistré.
3. **Centre de Dépouillement** : Le module qui déchiffre les votes à l'aide de la clé privée du centre de dépouillement et génère un rapport sur les résultats des votes.

## Fonctionnalités

- **Sécurisation des votes** : Les votes sont chiffrés avec la clé publique du centre de comptage pour garantir la confidentialité.
- **Dépouillement sécurisé** : Les votes sont déchiffrés à l'aide de la clé privée du centre de dépouillement.
- **Base de données** : Utilisation de SQLAlchemy pour gérer les votes dans une base de données relationnelle.
- **Notifications par e-mail** : Envoi d'e-mails pour notifier les parties prenantes sur l'état des votes et des résultats.

## Technologies Utilisées

- **Flask** : Framework web pour la gestion des routes, des templates, et des formulaires.
- **SQLAlchemy** : ORM pour interagir avec la base de données.
- **PGP (Pretty Good Privacy)** : Pour le chiffrement et le déchiffrement des votes.
- **GPG** : Librairie Python pour l'utilisation de PGP.
- **HTML/CSS** : Pour la structure et la mise en forme des pages web.
- **SQLite** : Base de données pour stocker les informations sur les votes.

## Installation

### Prérequis

- Python 3.13.2
- Flask
- SQLAlchemy
- GPG (GNU Privacy Guard)

### Étapes

1. Clonez ce repository :
    ```bash
    git clone https://github.com/votre-utilisateur/projet-vote-electronique.git
    cd projet-vote-electronique
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Configurez les clés GPG (si ce n'est pas déjà fait) :
    - Assurez-vous que vos clés publiques et privées PGP sont bien configurées et accessibles sur votre machine. Vous devrez remplacer les chemins des fichiers dans le code par vos propres chemins locaux.

5. Lancez l'application Flask :
    ```bash
    python run.py
    ```

6. Accédez à l'application dans votre navigateur à l'adresse suivante :
    ```
    http://127.0.0.1:5000
    ```

## Utilisation

### Voter

1. Rendez-vous sur la page **Voter** (`/votant`).
2. Remplissez le formulaire avec votre nom, prénom, date de naissance, identifiant, et votre choix.
3. Le vote sera automatiquement chiffré et sauvegardé dans la base de données.

### Comptage

1. Accédez à la page **Centre de Comptage** (`/comptage`) pour visualiser les votes enregistrés.
2. Un e-mail de notification sera envoyé à l'adresse du centre de comptage après chaque nouveau vote.

### Dépouillement

1. Rendez-vous sur la page **Centre de Dépouillement** (`/depouillement`).
2. Les votes seront déchiffrés et les résultats s'afficheront avec leur statut (réussi ou erreur de déchiffrement).
## Contact

Réaliser par Zineb Boussihi
Email: zinebboussihi@gmail.com


