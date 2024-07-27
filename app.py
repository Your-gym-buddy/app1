from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'jwtsecretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class GymPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    performance = db.Column(db.String(200), nullable=False)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    except:
        return jsonify({'message': 'Username already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/performance', methods=['GET', 'POST'])
@jwt_required()
def performance():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    if request.method == 'POST':
        data = request.get_json()
        new_performance = GymPerformance(user_id=user.id, date=data['date'], performance=data['performance'])
        db.session.add(new_performance)
        db.session.commit()
        return jsonify({'message': 'Performance added successfully'})
    elif request.method == 'GET':
        performances = GymPerformance.query.filter_by(user_id=user.id).all()
        output = [{'date': p.date, 'performance': p.performance} for p in performances]
        return jsonify({'performances': output})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
