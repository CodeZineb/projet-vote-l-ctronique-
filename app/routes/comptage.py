from flask import Blueprint, render_template, flash
from app.models import Vote
from app.email_utils import send_email
from app.db import db
import gnupg
import os

# Initialiser GPG
gpg = gnupg.GPG(gnupghome='C:\\Users\\HP\\AppData\\Roaming\\gnupg')  # Spécifie le chemin vers ton dossier .gnupg

# Chemin des clés du centre de comptage
comptage_private_key_path = r"C:\projet fed\projet fed\comptage_private_key.asc"
comptage_public_key_path = r"C:\projet fed\projet fed\comptage_public_key.asc"

# Importer la clé privée et publique pour le centre de comptage
if os.path.exists(comptage_private_key_path):
    with open(comptage_private_key_path, 'r') as f:
        private_key = f.read()
    gpg.import_keys(private_key)

if os.path.exists(comptage_public_key_path):
    with open(comptage_public_key_path, 'r') as f:
        public_key = f.read()
    gpg.import_keys(public_key)

# Email de notification
de_email = "zinebboussihi@gmail.com"

comptage_bp = Blueprint('comptage', __name__, url_prefix='/comptage')

@comptage_bp.route('/', methods=['GET'])
def comptage():
    try:
       # Supprimer les anciens résultats avec "Aucun bulletin" ou "Échec de déchiffrement"
        db.session.query(Vote).filter(
            Vote.choix_chiffre == "Aucun bulletin",
            Vote.choix_chiffre == "Échec de déchiffrement"
        ).delete(synchronize_session=False)
        db.session.commit()  # Confirmer les changements dans la base de données

        # Récupérer tous les votes de la base de données

    
        votes = Vote.query.all()

        if not votes:
            flash("Aucun vote trouvé.", "warning")

            return render_template('comptage.html', votes=[])

    # Dictionnaire pour stocker les votants par (nom, prénom)
        votants_uniques = {}
    
        for vote in votes:
          key = (vote.nom, vote.prenom)
          if key not in votants_uniques:
            votants_uniques[key] = vote  # Prendre uniquement le premier vote trouvé

    # Envoi d'un e-mail pour notifier du comptage
        send_email(de_email, "Notification de dépouillement", f"Un total de {len(votants_uniques)} votes a été transmis pour dépouillement.")

    # Retourner la vue 'comptage.html' avec les résultats des votes filtrés
        return render_template('comptage.html', votes=votants_uniques.values())

    except Exception as e:
     flash(f"Erreur lors de la récupération des votes : {str(e)}", 'danger')
    return render_template('comptage.html', votes=[])  

    
