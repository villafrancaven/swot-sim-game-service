from app import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    brand_market_score = db.Column(db.Integer)
    brand_market_reason = db.Column(db.Text)
    brand_market_status = db.Column(db.String(50), default="TBD")

    tech_infra_score = db.Column(db.Integer)
    tech_infra_reason = db.Column(db.Text)
    tech_infra_status = db.Column(db.String(50), default="TBD")

    def __repr__(self):
        return f"<Player {self.name}, Role: {self.role}>"
