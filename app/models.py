from app import db
from datetime import datetime
import hashlib


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String, unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    spent = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, amount):
        self.amount = amount
        self.spent = False

        current_datetime = datetime.now()
        datetime_str = str(current_datetime)

        self.hash = hashlib.sha256(datetime_str.encode()).hexdigest()

    def __repr__(self):
        return f"Transaction(id:'{self.id}', amount:'{self.amount}, spent:{self.spent}')"
