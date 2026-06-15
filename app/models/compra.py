from app import db
from datetime import datetime


class Compra(db.Model):

    __tablename__ = "compras"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fornecedor = db.Column(
        db.String(200),
        nullable=False
    )

    produto = db.Column(
        db.String(200),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False
    )

    valor_total = db.Column(
        db.Float,
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Compra {self.produto}>"