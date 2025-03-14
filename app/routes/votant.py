from flask import Blueprint, render_template, request, flash
from app.db import db
from app.models import Vote
import gnupg  # Import de gnupg pour le chiffrement
from app.email_utils import send_email
import os  # Assurez-vous que le module os est importé

co_email = "zineb.boussihi@uit.ac.ma"  # Email du centre de comptage

# Initialiser GPG
gpg = gnupg.GPG(gnupghome='C:\\Users\\HP\\AppData\\Roaming\\gnupg')  # Spécifie le chemin vers ton dossier .gnupg

votant_bp = Blueprint('votant', __name__, url_prefix='/votant')

# Chemin de la clé publique du centre de comptage
comptage_public_key_path = r"C:\projet fed\projet fed\comptage_public_key.asc"

# Importer la clé publique du centre de comptage
if os.path.exists(comptage_public_key_path):
    with open(comptage_public_key_path, 'r') as f:
        public_key = f.read()
    gpg.import_keys(public_key)

@votant_bp.route('/', methods=['GET', 'POST'])
def votant():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        date_naissance = request.form.get('date_naissance')
        identifiant = request.form.get('identifiant')
        choix = request.form.get('choix')

        if not (nom and prenom and date_naissance and identifiant and choix):
            flash('Tous les champs sont obligatoires.', 'danger')
            return render_template('votant.html')

        # Vérifier si le votant  existe déjà
        if Vote.query.filter_by(nom=nom, prenom=prenom, date_naissance=date_naissance, identifiant=identifiant).first():
            flash("Ce votant a déjà voté.", 'danger')
            return render_template('votant.html')

        # Chiffrer le choix avec la clé publique du centre de comptage
        encrypted_choice = gpg.encrypt(choix, co_email)  # L'email du centre de comptage
        if encrypted_choice.ok:
            encrypted_choice_str = str(encrypted_choice.data, 'utf-8')  # Récupérer la chaîne chiffrée en UTF-8
        else:
            flash('Erreur lors du chiffrement du choix.', 'danger')
            return render_template('votant.html')

        # Ajouter la clé publique dans l'enregistrement
        public_key = "clé publique du centre de comptage"  # Remplacer par la clé publique réelle

        # Sauvegarder le vote dans la base de données
        new_vote = Vote(
            nom=nom, 
            prenom=prenom, 
            date_naissance=date_naissance, 
            identifiant=identifiant, 
            choix_chiffre=encrypted_choice_str,
            public_key=public_key  # Assurer que public_key est fourni
        )
        db.session.add(new_vote)
        db.session.commit()

        # Envoyer un email de confirmation
        send_email(co_email, 'Confirmation de vote', f'Votre choix a été bien enregistré ')

        flash('Votre vote a été enregistré avec succès.', 'success')
        return render_template('votant.html')
    return render_template('votant.html')




