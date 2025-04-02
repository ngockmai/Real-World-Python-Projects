from app.models import db, User, Role, Campus, Building, Room, Category, Device
import random
from faker import Faker

# Import app and db from app/main
from app.main import app, db
fake = Faker()

def seed_database():
    # Clear existing data
    db.drop_all()
    db.create_all()
    
    # Sample data
    campuses = [
        Campus(campus_name = 'Fort Garry'),
        Campus(campus_name = 'Bannatyne'),
    ]
    db.session.add_all(campuses)
    db.session.commit()
    
    buildings = []
    for campus in campuses:
        for i in range(2):
            buildings.append(Building(
                building_name = f'Building {chr(i + 65)}', 
                campus_id = campus.campus_id))
    db.session.add_all(buildings)
    db.session.commit()
    
    rooms = []
    for building in buildings:
        for i in range(3):
            rooms.append(Room(
                room_number = f'{100+ i}',
                building_id = building.building_id))
    db.session.add_all(rooms)
    db.session.commit()
    
    categories = [
        Category(category_name = "TouchLink Pro Touchpanels"),
        Category(category_name = "IP Link Pro Control Processors"),
        Category(category_name = "Matrix Switchers"),
        Category(category_name = "Medialink Plus Controllers")
    ]
    db.session.add_all(categories)
    db.session.commit()
    
    devices = []
    for _ in range(20):
        devices.append(Device(
            model_name = fake.word().capitalize() + ' ' + fake.bothify('###'),
            ip_address = fake.ipv4(),
            mac_address = fake.mac_address(),
            hostname = fake.hostname(),
            serial_number = fake.uuid4(),
            firmware_version = f'{random.randint(1,5)}.{random.randint(0,9)}',
            device_link = fake.url(),
            room_id = random.choice(rooms).room_id,
            category_id = random.choice(categories).category_id,
        ))
    db.session.add_all(devices)
    db.session.commit()
    
    print(f"Database seeded with {len(campuses)} campuses, {len(buildings)} buildings, "
          f"{len(rooms)} rooms, {len(categories)} categories, and {len(devices)} devices")
    
    if __name__ == '__main__':
        seed_database()