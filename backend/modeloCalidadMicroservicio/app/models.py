from sqlalchemy import CheckConstraint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class QualityCharacteristic(db.Model):
    __tablename__ = 'quality_characteristics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weight_percentage = db.Column(db.Numeric(5, 2), nullable=False)

    subcharacteristics = db.relationship('Subcharacteristic', backref='characteristic', cascade='all, delete-orphan', lazy=True)

    __table_args__ = (
        CheckConstraint('weight_percentage >= 0 AND weight_percentage <= 100', name='check_weight_percentage'),
    )

    def __repr__(self):
        return f'<QualityCharacteristic {self.name}>'


class Subcharacteristic(db.Model):
    __tablename__ = 'subcharacteristics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('quality_characteristics.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_score = db.Column(db.SmallInteger, default=3, nullable=False)

    __table_args__ = (
        CheckConstraint('max_score > 0', name='check_max_score'),
    )

    def __repr__(self):
        return f'<Subcharacteristic {self.name} (max {self.max_score})>'
