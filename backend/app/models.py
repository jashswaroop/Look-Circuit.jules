from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Profile Information ---
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    height = db.Column(db.String(20)) # Storing as string to handle units, e.g., "5'11\"" or "180cm"
    body_shape = db.Column(db.String(50)) # e.g., Pear, Apple, Hourglass
    location_climate = db.Column(db.String(100))
    fashion_style = db.Column(db.String(100)) # e.g., Gen-Z, Millennial

    # --- Style Guide & Analysis Data ---
    style_guide_data = db.Column(db.Text) # To store JSON data from the questionnaire

    # Relationship to images
    images = db.relationship('UserImage', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class UserImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Analysis Results ---
    face_shape = db.Column(db.String(50))
    skin_tone = db.Column(db.String(50))
    dominant_colors = db.Column(db.Text) # Storing as JSON string
    analysis_complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<UserImage {self.filename}>'

class WardrobeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    product_link = db.Column(db.String(500))
    notes = db.Column(db.Text)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WardrobeItem {self.product_name}>'

class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wardrobe_item_id = db.Column(db.Integer, db.ForeignKey('wardrobe_item.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False) # e.g., 'save', 'like', 'dislike'
    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('interactions', lazy=True))
    wardrobe_item = db.relationship('WardrobeItem', backref=db.backref('interactions', lazy=True))

    def __repr__(self):
        return f'<UserInteraction {self.user_id} - {self.interaction_type} - {self.wardrobe_item_id}>'
