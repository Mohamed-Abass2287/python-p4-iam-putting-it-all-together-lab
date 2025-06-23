#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    print("Creating users...")
    users = []

    for _ in range(20):
        username = fake.unique.first_name()
        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url="https://cdn.iconscout.com/icon/free/png-256/avatar-372-456324-screenshot_4.jpg"
        )
        user.password_hash = f"{username}123"
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating recipes...")
    recipes = []

    for _ in range(100):
        user = rc(users)
        instructions = fake.paragraph(nb_sentences=10)
        if len(instructions) < 50:
            instructions += " Additional steps added to meet the required 50 characters."

        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15, 90),
            user_id=user.id
        )
        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()
    print("Seeding complete.")