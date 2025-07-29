from api.models.db import db

class TransactionHeader(db.Model):
    __tablename__ = 'transaction_header'
    id = db.Column(db.String(36), primary_key=True)
    description = db.Column(db.String(255))
    code = db.Column(db.String(50))
    rate_euro = db.Column(db.Float)
    date_paid = db.Column(db.DateTime)

    # Relationship with TransactionDetail
    details = db.relationship('TransactionDetail', back_populates='header', cascade='all, delete-orphan')
