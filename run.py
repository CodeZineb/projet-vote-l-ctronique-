import os
from flask import Flask, render_template
from app.db import db  # Importer la base de données
from app.routes.votant import votant_bp
from app.routes.comptage import comptage_bp
from app.routes.depouillement import depouillement_bp

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "app", "templates")
)

# Configuration de SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'votre_cle_secrete'  # Nécessaire pour flash

# Initialiser la base de données
db.init_app(app)

# Enregistrer les blueprints
app.register_blueprint(votant_bp)
app.register_blueprint(comptage_bp)
app.register_blueprint(depouillement_bp)

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Créer les tables si elles n'existent pas
    app.run(debug=True)


