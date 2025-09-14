from app import db


class Target(db.Model):
    __name__ = 'target'
    id = db.Column(db.Integer, primary_key=True)
    face_identification = db.Column(db.Boolean, nullable=False)
    face_identification_time = db.Column(db.String(100), nullable=False)
    is_killed = db.Column(db.Boolean, nullable=False)
