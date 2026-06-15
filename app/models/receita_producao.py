from app import db


class ReceitaProducao(db.Model):

    __tablename__ = "receitas_producao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    produto_final = db.Column(
        db.String(200),
        nullable=False
    )

    ingrediente = db.Column(
        db.String(200),
        nullable=False
    )

    quantidade = db.Column(
        db.Float,
        nullable=False
    )

    unidade = db.Column(
        db.String(20),
        default="Kg"
    )