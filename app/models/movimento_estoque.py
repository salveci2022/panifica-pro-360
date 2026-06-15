from app import db
from datetime import datetime


class MovimentoEstoque(db.Model):

    __tablename__ = "movimentos_estoque"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto = db.Column(
        db.String(200),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False
    )

    observacao = db.Column(
        db.String(300)
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )