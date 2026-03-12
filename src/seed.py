"""
Seed script to populate the database with test data.
All strings are in English to avoid encoding issues with Russian characters in some environments.
"""
from src.core.database import SESSION_LOCAL
from src.models.models import Activity, Building, Organization, Phone


# pylint: disable=too-many-locals
def seed_data():
    """
    Populate the database with initial test data.
    """
    db = SESSION_LOCAL()
    try:
        # 1. Buildings
        b1 = Building(
            address="Moscow, Lenina 1, off. 3",
            latitude=55.7558,
            longitude=37.6173
        )
        b2 = Building(
            address="Novosibirsk, Bluhera 32/1",
            latitude=54.9833,
            longitude=82.8964
        )
        db.add_all([b1, b2])
        db.commit()

        # 2. Activities (Tree)
        # Level 1
        food = Activity(name="Food")
        cars = Activity(name="Cars")
        db.add_all([food, cars])
        db.commit()

        # Level 2
        meat = Activity(name="Meat products", parent_id=food.id)
        milk = Activity(name="Dairy products", parent_id=food.id)
        trucks = Activity(name="Trucks", parent_id=cars.id)
        passengers = Activity(name="Passenger cars", parent_id=cars.id)
        db.add_all([meat, milk, trucks, passengers])
        db.commit()

        # Level 3
        parts = Activity(name="Spare parts", parent_id=passengers.id)
        accessories = Activity(name="Accessories", parent_id=passengers.id)
        db.add_all([parts, accessories])
        db.commit()

        # 3. Organizations
        org1 = Organization(name='Horns and Hooves LLC', building_id=b2.id)
        org1.activities = [meat, milk]

        org2 = Organization(name="SuperAuto", building_id=b1.id)
        org2.activities = [parts]

        org3 = Organization(name="Meat Garden", building_id=b2.id)
        org3.activities = [meat]

        db.add_all([org1, org2, org3])
        db.commit()

        # 4. Phones
        p1 = Phone(number="2-222-222", organization_id=org1.id)
        p2 = Phone(number="3-333-333", organization_id=org1.id)
        p3 = Phone(number="8-923-666-13-13", organization_id=org1.id)
        p4 = Phone(number="1-111-111", organization_id=org2.id)

        db.add_all([p1, p2, p3, p4])
        db.commit()

        print("Data successfully seeded!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
