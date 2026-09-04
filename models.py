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
    price = db.Column(db.Integer, nullable=False)         # in NGN
    condition = db.Column(db.String(30), nullable=False)   # Brand New, Tokunbo, Nigerian Used
    listing_type = db.Column(db.String(30), nullable=False) # Sale, Rent
    body_style = db.Column(db.String(30), nullable=True)   # Sedan, SUV, Coupe
    drive_type = db.Column(db.String(10), nullable=True)   # AWD, RWD, FWD
    transmission = db.Column(db.String(20), nullable=True) # Automatic, Manual
    mileage = db.Column(db.String(20), nullable=True)      # e.g., "45,000 km"
    description = db.Column(db.Text, nullable=True)
    primary_image = db.Column(db.String(255), nullable=True)   # filename or URL
    image_paths = db.Column(db.Text, nullable=True)            # comma-separated URLs or filenames
    featured = db.Column(db.Boolean, default=False)
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
