from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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
    permits = db.relationship('Permit', backref='ship', lazy=True, cascade="all, delete-orphan")
    catch_logs = db.relationship('CatchLog', backref='ship', lazy=True, cascade="all, delete-orphan")
    inspections = db.relationship('Inspection', backref='ship', lazy=True, cascade="all, delete-orphan")

class Permit(db.Model):
    __tablename__ = 'permits'
    id = db.Column(db.Integer, primary_key=True)
    permit_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    gear_type = db.Column(db.String(200))
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=False)

class CatchLog(db.Model):
    __tablename__ = 'catch_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    fish_species = db.Column(db.String(100), nullable=False)
    quantity_kg = db.Column(db.Float, nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Inspection(db.Model):
    __tablename__ = 'inspections'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(200), nullable=False)
    violations = db.Column(db.Text)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=False)
    fines = db.relationship('Fine', backref='inspection', lazy=True)


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    holder_name = db.Column(db.String(150), nullable=False)
    egn = db.Column(db.String(10), nullable=False)
    ticket_type = db.Column(db.String(50), nullable=False)
    validity_period = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    telk_number = db.Column(db.String(50))

    def __repr__(self):
        return f'<Ticket {self.holder_name} - {self.ticket_type}>'


class Fine(db.Model):
    __tablename__ = 'fines'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspections.id'), nullable=False)
    act_number = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Fine {self.act_number}>'