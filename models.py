from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Ship(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    int_number = db.Column(db.String(50), unique=True, nullable=False)
    call_sign = db.Column(db.String(50))
    marking = db.Column(db.String(100))

    owner_name = db.Column(db.String(150), nullable=False)
    captain_name = db.Column(db.String(150), nullable=False)

    length = db.Column(db.Float)
    width = db.Column(db.Float)
    tonnage = db.Column(db.Float)
    draft = db.Column(db.Float)
    engine_power = db.Column(db.Float)
    fuel_type = db.Column(db.String(50))

    def __repr__(self):
        return f'<Ship {self.name} - {self.int_number}>'