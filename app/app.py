from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power  # Import the models correctly

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Routes
@app.route('/')
def home():
    return ''

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [power.name for power in hero.powers]
        }
        hero_list.append(hero_data)
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [power.name for power in hero.powers]
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        power_list.append(power_data)
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']

    db.session.commit()
    return jsonify({
        'id': power.id,
        'name': power.name,
        'description': power.description
    })

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if hero_id is None or power_id is None:
        return jsonify({'error': 'Hero ID and Power ID are required'}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        return jsonify({'error': 'Hero or Power not found'}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({
        'id': hero_power.id,
        'hero_id': hero_power.hero_id,
        'power_id': hero_power.power_id,
        'strength': hero_power.strength
    }), 201

if __name__ == '__main__':
    app.run(port=5000)
