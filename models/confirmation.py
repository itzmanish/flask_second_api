from uuid import uuid4
from time import time

from db import db

CONFIRMATION_EXIPIRATION_DELTA = 1800


class ConfirmationModel(db.Model):

    __tablename__ = "confirmation"

    id = db.Column(db.String(80), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.confirmed = False
        self.id = str(uuid4())
        self.expire_at = int(time()) + CONFIRMATION_EXIPIRATION_DELTA

    @classmethod
    def find_by_id(cls, _id: str) -> 'ConfirmationModel':
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()