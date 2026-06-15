from app import db
from datetime import datetime


class Venda(db.Model):

    __tablename__ = "vendas"

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

    valor_unitario = db.Column(
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