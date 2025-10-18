from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
mongo = None  # Will be set in app.py

@auth_bp.record
def record_params(setup_state):
    global mongo
    mongo = setup_state.app.config['MONGO']

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    users = mongo.db.users
    if users.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    users.insert_one({"username": username, "password": hashed_pw})
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = mongo.db.users.find_one({"username": username})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token}), 200
