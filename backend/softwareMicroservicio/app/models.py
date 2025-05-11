from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    general_objective = db.Column(db.String(250), nullable = False)
    description = db.Column(db.String(300), unique=True, nullable=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Software {self.name}>'
    
class SoftwareParticipant(db.Model):
    __tablename__ = 'software_participants'

    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    software = db.relationship('Software', backref=db.backref('participants', cascade='all, delete-orphan', lazy=True))

    def __repr__(self):
        return f'<SoftwareParticipant {self.name} - {self.role}>'
