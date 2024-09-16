from datetime import UTC, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))

    # Method to set the password (hashes the password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password (compares the hashed password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    text = db.Column(db.Text(), nullable=True)
    response_text = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    products = db.relationship("Product", backref="message", lazy=True)

    @property
    def sender(self):
        return User.query.filter_by(id=self.sender_id).first()

    @property
    def receiver(self):
        return User.query.filter_by(id=self.receiver_id).first()

    def __repr__(self):
        return f"Message by {self.sender.name} to {self.receiver.name} : {self.text}"


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(
        db.Integer, db.ForeignKey("messages.id", ondelete="CASCADE"), nullable=True
    )
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float)  # Ensure this field is in a consistent format
    link = db.Column(db.String(10000))
    image = db.Column(db.String(10000))
    source = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    rating = db.Column(db.Float)  # Add rating attribute
