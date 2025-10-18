from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import certifi

from config import Config
from corrector import correct_text
from auth import auth_bp, bcrypt

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# MongoDB
app.config["MONGO_URI"] = Config.MONGO_URL
mongo = PyMongo(app, tlsCAFile=certifi.where())
app.config["MONGO"] = mongo

# JWT & Bcrypt
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register auth blueprint
app.register_blueprint(auth_bp, url_prefix="/auth")

# Spell correction endpoint
@app.route("/correct", methods=["POST"])
def correct_endpoint():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    corrected = correct_text(text)
    return jsonify({"corrected_text": corrected})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
