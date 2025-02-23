from . import db
from datetime import datetime
from flask_login import UserMixin

# Association table for the many-to-many relationship between Pizza and Topping
pizza_toppings = db.Table('pizza_toppings',
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'), primary_key=True),
    db.Column('topping_id', db.Integer, db.ForeignKey('topping.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150))
    # is_owner True means the user manages toppings, False means they are a chef
    is_owner = db.Column(db.Boolean, default=False)
    # Pizzas created by the user if they are a chef
    pizzas = db.relationship('Pizza', backref='chef', lazy=True)
    # Toppings managed by the user if they are an owner
    toppings = db.relationship('Topping', backref='owner', lazy=True)
    

    def __repr__(self):
        role = 'Owner' if self.is_owner else 'Chef'
        return f"<User {self.name} - {role}>"

class Topping(db.Model):
    __tablename__ = 'topping'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    # Owner who manages this topping (User with is_owner True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Topping {self.name}>"

class Pizza(db.Model):
    __tablename__ = 'pizza'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    # Chef who creates the pizza (User with is_owner False)
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Many-to-many relationship: a pizza can have multiple toppings
    toppings = db.relationship('Topping', secondary=pizza_toppings, backref=db.backref('pizzas', lazy='dynamic'))

    def __repr__(self):
        return f"<Pizza {self.name}>"
