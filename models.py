from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trial_ends_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    is_active = db.Column(db.Boolean, default=True)
    is_paid = db.Column(db.Boolean, default=False)
    subscription_end_date = db.Column(db.DateTime, nullable=True)

    tickets = db.relationship('RepairTicket', backref='shop', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_shop(cls, shop_name, owner_name, phone, password):
        shop = cls(shop_name=shop_name, owner_name=owner_name, phone=phone)
        shop.set_password(password)
        db.session.add(shop)
        db.session.commit()
        return shop

    def is_trial_active(self):
        return datetime.utcnow() <= self.trial_ends_at

class RepairTicket(db.Model):
    __tablename__ = 'repair_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    device_model = db.Column(db.String(100), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='قيد الفحص')
    cost = db.Column(db.Float, default=0.0)
    
    # حقل جديد خاص بالأرشفة (True تعني ظاهرة في اللوحة، False تعني مؤرشفة ومخفية ولكنها محفوظة)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)