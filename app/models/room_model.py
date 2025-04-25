from app import db
from datetime import datetime


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    players = db.relationship("Player", backref="room", lazy=True)

    def __repr__(self):
        return f"<Room {self.room_number}>"
