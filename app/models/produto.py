

from app import db

class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(200),
        nullable=False
    )

    categoria = db.Column(
        db.String(100)
    )

    unidade = db.Column(
        db.String(20),
        default="Kg"
    )

    estoque_minimo = db.Column(
        db.Float,
        default=0
    )

    custo_medio = db.Column(
        db.Float,
        default=0
    )

    preco_venda = db.Column(
        db.Float,
        default=0
    )