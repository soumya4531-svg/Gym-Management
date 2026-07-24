from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationship to members
    members = db.relationship('Member', backref='subscription', lazy=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    photo_filename = db.Column(db.String(255), nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional health info
    weight = db.Column(db.Float, nullable=True)  # in kg
    height = db.Column(db.Float, nullable=True)  # in cm
    medical_condition = db.Column(db.Text, nullable=True)
    
    # Workout goals and schedule
    fitness_goal = db.Column(db.String(100), nullable=True)
    workout_monday = db.Column(db.String(255), nullable=True)
    workout_tuesday = db.Column(db.String(255), nullable=True)
    workout_wednesday = db.Column(db.String(255), nullable=True)
    workout_thursday = db.Column(db.String(255), nullable=True)
    workout_friday = db.Column(db.String(255), nullable=True)
    workout_saturday = db.Column(db.String(255), nullable=True)
    workout_sunday = db.Column(db.String(255), nullable=True)
    
    # Foreign key to Subscription
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=True)
    subscription_start = db.Column(db.Date, nullable=True)
    
    # Relationship to payments
    payments = db.relationship('Payment', backref='member', lazy=True, cascade='all, delete-orphan')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)   # 1-12
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0)
    is_paid = db.Column(db.Boolean, default=False)
    paid_date = db.Column(db.DateTime, nullable=True)
    
    __table_args__ = (db.UniqueConstraint('member_id', 'month', 'year', name='uq_member_month_year'),)
