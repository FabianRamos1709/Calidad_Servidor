from sqlalchemy import CheckConstraint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, nullable=False)  
    date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    global_score_percentage = db.Column(db.Numeric(5, 2), nullable=True)

    details = db.relationship('EvaluationDetail', backref='evaluation', cascade='all, delete-orphan')
    characteristic_summaries = db.relationship('EvaluationCharacteristicSummary', backref='evaluation', cascade='all, delete-orphan')


class EvaluationCharacteristicSummary(db.Model):
    __tablename__ = 'evaluation_characteristic_summary'

    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id', ondelete='CASCADE'), nullable=False)
    characteristic_id = db.Column(db.Integer, db.ForeignKey('quality_characteristics.id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    max_value = db.Column(db.Integer, nullable=False)
    result_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    weighted_percentage = db.Column(db.Numeric(5, 2), nullable=False)

    # Establece la relación
    characteristic = db.relationship("QualityCharacteristic", backref="evaluations_summary")


class EvaluationDetail(db.Model):
    __tablename__ = 'evaluation_details'

    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id', ondelete='CASCADE'), nullable=False)
    subcharacteristic_id = db.Column(db.Integer, db.ForeignKey('subcharacteristics.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.SmallInteger, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    # Establece la relación
    subcharacteristic = db.relationship("Subcharacteristic", backref="evaluation_details")

    __table_args__ = (
        db.CheckConstraint('score BETWEEN 0 AND 3', name='check_score_between_0_and_3'),
    )

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
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'weight_percentage': float(self.weight_percentage)
        }

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
    
    def serialize(self):
        return {
            'id': self.id,
            'characteristic_id': self.characteristic_id,
            'name': self.name,
            'description': self.description,
            'max_score': self.max_score
        }

    def __repr__(self):
        return f'<Subcharacteristic {self.name} (max {self.max_score})>'
