from app.db import db

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.String(20), nullable=False)
    identifiant = db.Column(db.String(50), unique=True, nullable=False)
    choix_chiffre = db.Column(db.Text, nullable=False)  # Garde cette ligne
    public_key = db.Column(db.Text, nullable=False)

