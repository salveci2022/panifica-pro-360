from app import db
from datetime import datetime


class Fornecedor(db.Model):

    __tablename__ = "fornecedores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(200),
        nullable=False
    )

    produto = db.Column(
        db.String(200),
        nullable=False
    )

    telefone = db.Column(
        db.String(50)
    )

    whatsapp = db.Column(
        db.String(50)
    )

    email = db.Column(
        db.String(200)
    )

    cidade = db.Column(
        db.String(150)
    )

    observacao = db.Column(
        db.Text
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"