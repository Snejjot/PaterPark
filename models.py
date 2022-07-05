from app import db
from datetime import datetime


class Plate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    def __init__(self, plate):
        self.plate = plate

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'plate': self.plate,
            'timestamp': self.timestamp
        }
