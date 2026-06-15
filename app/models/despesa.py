from app import db
from datetime import datetime


class Despesa(db.Model):

    __tablename__ = "despesas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    descricao = db.Column(
        db.String(200),
        nullable=False
    )

    fornecedor = db.Column(
        db.String(200),
        nullable=False
    )

    valor = db.Column(
        db.Float,
        nullable=False
    )

    vencimento = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pendente"
    )

    observacao = db.Column(
        db.Text
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Despesa {self.descricao}>"