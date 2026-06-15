from app import db
from datetime import datetime


class Producao(db.Model):

    __tablename__ = "producoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto = db.Column(
        db.String(200),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False
    )

    observacao = db.Column(
        db.Text
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Producao {self.produto}>"