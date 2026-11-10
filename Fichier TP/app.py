import os
 
from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
 
app = Flask(__name__)
 
# Dans docker compose, "mongo" est le nom du service MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client["tp_docker"]
 
 
@app.route("/")
def accueil():
    return "Hello world"
 
 
@app.route("/db")
def test_db():
    try:
        client.admin.command("ping")
        db.visites.insert_one({"message": "Hello depuis Flask"})
        nb_visites = db.visites.count_documents({})
        return jsonify(statut="Connexion a MongoDB OK", visites=nb_visites)
    except PyMongoError as erreur:
        return jsonify(statut="Erreur de connexion a MongoDB", detail=str(erreur)), 500
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 