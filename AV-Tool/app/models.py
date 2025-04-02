from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Campus(db.Model):
    __tablename__ = 'campus'
    campus_id = db.Column(db.Integer, primary_key=True)
    campus_name = db.Column(db.String(100), unique=True, nullable=False)
    buildings = db.relationship('Building', backref='campus', lazy=True)
    
class Building(db.Model):
    __tablename__ = 'building'
    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(100), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.campus_id'), nullable=False)
    rooms = db.relationship('Room', backref='building', lazy=True)
    __table_args__ = (db.UniqueConstraint('building_name', 'campus_id'),)
    
class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.building_id'), nullable=False)
    devices = db.relationship('Device', backref='room', lazy=True)
    __table_args__ = (db.UniqueConstraint('room_number', 'building_id'),)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    devices = db.relationship('Device', backref='category', lazy=True)

class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45))
    mac_address = db.Column(db.String(17), unique=True)
    hostname = db.Column(db.String(100))
    serial_number = db.Column(db.String(100), unique=True)
    firmware_version = db.Column(db.String(50))
    device_link = db.Column(db.String(255))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    
class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(64), unique = True)