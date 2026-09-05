from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)         # NGN integer
    condition = db.Column(db.String(30), nullable=False)   # Brand New, Tokunbo, Nigerian Used
    listing_type = db.Column(db.String(30), nullable=False) # Sale, Rent
    body_style = db.Column(db.String(30), nullable=True)
    drive_type = db.Column(db.String(10), nullable=True)
    transmission = db.Column(db.String(20), nullable=True)
    mileage = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    primary_image = db.Column(db.String(255), nullable=True)
    image_paths = db.Column(db.Text, nullable=True)
    featured = db.Column(db.Boolean, default=False)
    customs_verified = db.Column(db.Boolean, default=False)
    inspection_score = db.Column(db.Integer, nullable=True)
    inspection_report_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_images(self):
        images = []
        if self.primary_image:
            images.append(self.primary_image)
        if self.image_paths:
            extra = [img.strip() for img in self.image_paths.split(',') if img.strip()]
            images.extend(extra)
        return images

    def get_primary(self):
        return self.primary_image or (self.get_images()[0] if self.get_images() else None)

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    name = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    source = db.Column(db.String(20), default='whatsapp')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship('Vehicle', backref='leads')
