from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# User model for authentication and authorization
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #primary key
    username = db.Column(db.String(100), unique=True, nullable=False) #unique username
    password = db.Column(db.String(200), nullable=False) #hashed password
    role = db.Column(db.String(20), default='user')  # set role default as 'user'
    reservations = db.relationship('Reservation', backref='user', cascade="all, delete", lazy=True) # relationship to Reservation model

# ParkingLotfor the parking system
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key
    prime_location_name = db.Column(db.String(100), nullable=False) # name of the parking lot
    price = db.Column(db.Float, nullable=False) # price per hour
    address = db.Column(db.String(200), nullable=False) # address of the parking lot
    pin_code = db.Column(db.String(10), nullable=False) # pin code of the parking lot
    maximum_number_of_spots = db.Column(db.Integer, nullable=False) # maximum number of parking spots in the lot

    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete", lazy=True) # relationship to ParkingSpot model

# ParkingSpot models for the parking system
class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False) # foreign key to ParkingLot
    status = db.Column(db.String(1), default='A')  # A - Available, O - Occupied 

    reservations = db.relationship('Reservation', backref='spot', cascade="all, delete", lazy=True) # relationship to Reservation model

# Reservation models for the parking system
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)  # foreign key to ParkingSpot
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # foreign key to User
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow) # timestamp when the reservation was made
    leaving_timestamp = db.Column(db.DateTime, nullable=True) # timestamp when the user leaves
    parking_cost = db.Column(db.Float, nullable=True) # cost of the parking reservation
    # New fields for feedback
    rating = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    @property # to get the ParkingSpot object
    def lot(self):
        return self.spot.lot if self.spot else None 
    
