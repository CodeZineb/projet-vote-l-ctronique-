from flask import Blueprint, render_template, flash
from app.models import Vote
import gnupg
from app.db import db
import os

# Initialiser GPG
gpg = gnupg.GPG(gnupghome='C:\\Users\\HP\\AppData\\Roaming\\gnupg')  # Spécifie le chemin vers ton dossier .gnupg

# Chemin des clés du centre de dépouillement
depouillement_private_key_path = r"C:\projet fed\projet fed\depouillement_private_key.asc"
depouillement_public_key_path = r"C:\projet fed\projet fed\depouillement_public_key.asc"

# Importer la clé privée et publique pour le centre de dépouillement
if os.path.exists(depouillement_private_key_path):
    with open(depouillement_private_key_path, 'r') as f:
        private_key = f.read()
    gpg.import_keys(private_key)

if os.path.exists(depouillement_public_key_path):
    with open(depouillement_public_key_path, 'r') as f:
        public_key = f.read()
    gpg.import_keys(public_key)

depouillement_bp = Blueprint('depouillement', __name__, url_prefix='/depouillement')

@depouillement_bp.route('/', methods=['GET'])
def depouillement():
    try:
       # Supprimer les anciens résultats avec "Aucun bulletin" ou "Échec de déchiffrement"
        db.session.query(Vote).filter(
            Vote.choix_chiffre == "Aucun bulletin",
            Vote.choix_chiffre == "Échec de déchiffrement"
        ).delete(synchronize_session=False)
        db.session.commit()  # Confirmer les changements dans la base de données

        # Récupérer tous les votes de la base de données
        votes = Vote.query.all()

        results = []

        # Traitement des votes
        for vote in votes:
            identifiant = vote.identifiant
            bulletin_chiffre = vote.choix_chiffre
            bulletin_dechiffre = "Échec déchiffrement"
            statut = "Validé"

            try:
                # Déchiffrer le bulletin avec la clé privée du centre de dépouillement
                decrypted_vote = str(gpg.decrypt(bulletin_chiffre))
                if decrypted_vote:
                    bulletin_dechiffre = decrypted_vote
                else:
                    statut = "Erreur: Déchiffrement échoué"
            except Exception as e:
                statut = f"Erreur: {str(e)}"

            results.append({
                'identifiant': identifiant,
                'bulletin': bulletin_dechiffre,
                'statut': statut
            })

        return render_template('depouillement.html', results=results)

    except Exception as e:
        flash(f"Erreur lors du traitement des votes : {str(e)}", 'danger')
        return render_template('depouillement.html', results=[])





