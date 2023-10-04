from faker import Faker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def seed_database():
    faker = Faker()

    # Create a few heroes
    heroes = []
    for i in range(10):
        hero = Hero(
            name=faker.name(),
            super_name=faker.name(),
        )
        heroes.append(hero)

    # Create a few powers
    powers = []
    for i in range(10):
        power = Power(
            name=faker.word(),
            description=faker.sentence(),
        )
        powers.append(power)

    # Create some hero-power relationships
    for hero in heroes:
        for i in range(random.randint(1, 3)):
            power = random.choice(powers)
            hero_power = HeroPower(
                hero=hero,
                power=power,
                strength=faker.word(),
            )
            db.session.add(hero_power)
 
    # Commit the changes to the database
    db.session.commit()
