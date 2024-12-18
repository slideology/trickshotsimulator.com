from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credits = db.Column(db.Integer, default=0)
    stripe_customer_id = db.Column(db.String(120), unique=True)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    image_generations = db.relationship('ImageGeneration', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_credits(self, amount):
        self.credits += amount
        db.session.commit()

    def use_credits(self, amount):
        if self.credits >= amount:
            self.credits -= amount
            db.session.commit()
            return True
        return False

    def get_stripe_customer(self):
        if not self.stripe_customer_id:
            customer = stripe.Customer.create(
                email=self.email,
                metadata={'user_id': self.id}
            )
            self.stripe_customer_id = customer.id
            db.session.commit()
        return self.stripe_customer_id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_ai = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(200))  # For storing generated image URLs
    credits_used = db.Column(db.Integer, default=1)  # 使用的信用点数

class ImageGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credits_used = db.Column(db.Integer, default=5)  # 使用的信用点数

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    credits = db.Column(db.Integer, nullable=False)
    stripe_payment_id = db.Column(db.String(120), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    stripe_subscription_id = db.Column(db.String(120), unique=True)
    status = db.Column(db.String(20), default='active')  # active, canceled, expired
    credits_per_month = db.Column(db.Integer, nullable=False)
    price_per_month = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    auto_renew = db.Column(db.Boolean, default=True)

class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    stripe_price_id = db.Column(db.String(120), unique=True)
    is_subscription = db.Column(db.Boolean, default=False)
    interval = db.Column(db.String(20))  # monthly, yearly (for subscriptions)

def init_db():
    db.create_all()
    
    # 只有当没有定价计划时才创建默认计划
    if not PricingPlan.query.first():
        plans = [
            PricingPlan(
                name='Basic Package',
                description='Perfect for getting started',
                price=9.99,
                credits=100,
                is_subscription=False
            ),
            PricingPlan(
                name='Pro Package',
                description='Most popular choice for regular users',
                price=24.99,
                credits=300,
                is_subscription=False
            ),
            PricingPlan(
                name='Premium Subscription',
                description='Best value for power users',
                price=49.99,
                credits=1000,
                is_subscription=True
            )
        ]
        
        for plan in plans:
            db.session.add(plan)
        
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error creating default plans: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_db()
