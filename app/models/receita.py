

from app import db
from datetime import datetime


class Receita(db.Model):

    __tablename__ = "receitas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    descricao = db.Column(
        db.String(200),
        nullable=False
    )

    valor = db.Column(
        db.Float,
        nullable=False
    )

    categoria = db.Column(
        db.String(100),
        default="Venda"
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Receita {self.descricao}>"