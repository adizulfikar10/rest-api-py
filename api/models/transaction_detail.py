from api.models.db import db

class TransactionDetail(db.Model):
    __tablename__ = 'transaction_detail'
    id = db.Column(db.String(36), primary_key=True)
    transaction_id = db.Column(db.String(36), db.ForeignKey('transaction_header.id'))
    transaction_category_id = db.Column(db.String(36), db.ForeignKey('ms_category.id'))
    name = db.Column(db.String(255))
    value_idr = db.Column(db.Float)
    
    # Parent relationship
    header = db.relationship('TransactionHeader', back_populates='details')

    # Category relationship
    category = db.relationship('MsCategory', back_populates='details')
