
from api.models.db import db
class MsCategory(db.Model):
    __tablename__ = 'ms_category'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255))

    # Relationship with TransactionDetail
    details = db.relationship('TransactionDetail', back_populates='category')
