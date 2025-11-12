import os
import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'username': self.username
        }

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- Rotas da API ---
@app.route('/health')
def health_check():
    return jsonify({"status": "Flask API is healthy"}), 200


# POST /users -- cria um usuário
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    required_fields = ['name', 'email', 'username', 'password']

    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": f"Missing one or more fields: {', '.join(required_fields)}"}), 400

    name = data['name']
    email = data['email']
    username = data['username']
    plain_password = data['password']

    if User.query.filter_by(name=name).first():
        return jsonify({"error": "Name already exists"}), 409

    existing_users = User.query.all()
    for user in existing_users:
        if check_password(plain_password, user.password):
            return jsonify({"error": "Password already exists"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = hash_password(plain_password)
    new_user = User(name=name, email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


# GET /users -- lista todos os usuários
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# GET /users/{id} -- consulta usuário por ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# --- Atualizar usuário ---
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}

    if 'name' in data and data['name'] != user.name:
        if User.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Name already exists"}), 409
        user.name = data['name']

    if 'password' in data:
        new_plain = data['password']

        existing_users = User.query.all()
        for u in existing_users:
            if check_password(new_plain, u.password):
                return jsonify({"error": "Password already exists"}), 409

        user.password = hash_password(new_plain)

    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 409
        user.email = data['email']

    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 409
        user.username = data['username']

    db.session.commit()
    return jsonify(user.to_dict()), 200


# --- Deletar usuário ---
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run()