from app import db
from datetime import datetime


class Estoque(db.Model):

    __tablename__ = "estoque"

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
        nullable=False,
        default=0
    )

    unidade = db.Column(
        db.String(20),
        default="Kg"
    )

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Estoque {self.produto}>"