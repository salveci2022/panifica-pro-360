from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

from reportlab.pdfgen import canvas
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.receita import Receita
    from app.models.despesa import Despesa
    from app.models.fornecedor import Fornecedor
    from app.models.compra import Compra
    from app.models.estoque import Estoque
    from app.models.producao import Producao
    from app.models.produto import Produto
    from app.models.receita_producao import ReceitaProducao
    from app.models.movimento_estoque import MovimentoEstoque
    from app.models.venda import Venda

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard():

        receita_total = db.session.query(
            db.func.sum(Receita.valor)
        ).scalar() or 0

        despesa_total = db.session.query(
            db.func.sum(Despesa.valor)
        ).scalar() or 0

        boletos = Despesa.query.filter_by(
            status="Pendente"
        ).count()

        lucro_total = receita_total - despesa_total

        fluxo_caixa = receita_total - despesa_total

        total_compras = Compra.query.count()
        total_vendas = Venda.query.count()

        estoque_itens = Estoque.query.count()

        alertas_estoque = []

        produtos_cadastrados = Produto.query.all()

        for produto in produtos_cadastrados:

            item = Estoque.query.filter_by(
                produto=produto.nome
            ).first()

            if item:

                if item.quantidade <= produto.estoque_minimo:

                    alertas_estoque.append(
                        f"{produto.nome} abaixo do minimo"
                    )

        return render_template(
            "dashboard.html",
            receita_total=receita_total,
            despesa_total=despesa_total,
            lucro_total=lucro_total,
            fluxo_caixa=fluxo_caixa,
            total_compras=total_compras,
            total_vendas=total_vendas,
            estoque_itens=estoque_itens,
            alertas_estoque=alertas_estoque,
            boletos=boletos
        )

    @app.route("/financeiro", methods=["GET", "POST"])
    def financeiro():

        if request.method == "POST":

            nova_receita = Receita(
                descricao=request.form["descricao"],
                valor=float(request.form["valor"])
            )

            db.session.add(nova_receita)
            db.session.commit()

            return redirect("/financeiro")

        receitas = Receita.query.order_by(
            Receita.id.desc()
        ).all()

        return render_template(
            "financeiro.html",
            receitas=receitas
        )

    @app.route("/contas-pagar", methods=["GET", "POST"])
    def contas_pagar():

        if request.method == "POST":

            nova_despesa = Despesa(
                descricao=request.form["descricao"],
                fornecedor=request.form["fornecedor"],
                valor=float(request.form["valor"]),
                vencimento=datetime.strptime(
                    request.form["vencimento"],
                    "%Y-%m-%d"
                ).date(),
                status="Pendente"
            )

            db.session.add(nova_despesa)
            db.session.commit()

            return redirect("/contas-pagar")

        despesas = Despesa.query.order_by(
            Despesa.id.desc()
        ).all()

        return render_template(
            "contas_pagar.html",
            despesas=despesas
        )

    @app.route("/fornecedores", methods=["GET", "POST"])
    def fornecedores():

        if request.method == "POST":

            novo_fornecedor = Fornecedor(
                nome=request.form["nome"],
                produto=request.form["produto"],
                telefone=request.form.get("telefone"),
                whatsapp=request.form.get("whatsapp"),
                email=request.form.get("email"),
                cidade=request.form.get("cidade"),
                observacao=request.form.get("observacao")
            )

            db.session.add(novo_fornecedor)
            db.session.commit()

            return redirect("/fornecedores")

        fornecedores = Fornecedor.query.order_by(
            Fornecedor.id.desc()
        ).all()

        return render_template(
            "fornecedores.html",
            fornecedores=fornecedores
        )

    @app.route("/compras", methods=["GET", "POST"])
    def compras():

        if request.method == "POST":

            produto = request.form["produto"]
            quantidade = float(request.form["quantidade"])

            nova_compra = Compra(
                fornecedor=request.form["fornecedor"],
                produto=produto,
                quantidade=quantidade,
                valor_total=float(request.form["valor_total"])
            )

            db.session.add(nova_compra)

            mov = MovimentoEstoque(
                produto=produto,
                tipo="ENTRADA",
                quantidade=quantidade,
                observacao="Compra de fornecedor"
            )

            db.session.add(mov)

            item_estoque = Estoque.query.filter_by(
                produto=produto
            ).first()

            if item_estoque:
                item_estoque.quantidade += quantidade
            else:
                item_estoque = Estoque(
                    produto=produto,
                    quantidade=quantidade
                )
                db.session.add(item_estoque)

            db.session.commit()

            return redirect("/compras")

        fornecedores_list = Fornecedor.query.order_by(
            Fornecedor.nome
        ).all()

        compras_list = Compra.query.order_by(
            Compra.id.desc()
        ).all()

        return render_template(
            "compras.html",
            fornecedores=fornecedores_list,
            compras=compras_list
        )

    @app.route("/estoque")
    def estoque():

        produtos = Estoque.query.order_by(
            Estoque.produto
        ).all()

        return render_template(
            "estoque.html",
            produtos=produtos
        )

    @app.route("/producao", methods=["GET", "POST"])
    def producao():

        if request.method == "POST":

            nova_producao = Producao(
                produto=request.form["produto"],
                quantidade=float(request.form["quantidade"]),
                observacao=request.form.get("observacao")
            )

            db.session.add(nova_producao)

            mov = MovimentoEstoque(
                produto=request.form["produto"],
                tipo="SAIDA",
                quantidade=float(request.form["quantidade"]),
                observacao="Producao"
            )

            db.session.add(mov)

            receitas = ReceitaProducao.query.filter_by(
                produto_final=request.form["produto"]
            ).all()

            for receita in receitas:

                item = Estoque.query.filter_by(
                    produto=receita.ingrediente
                ).first()

                if item:

                    consumo = (
                        receita.quantidade *
                        float(request.form["quantidade"])
                    )

                    item.quantidade -= consumo

                    mov_receita = MovimentoEstoque(
                        produto=receita.ingrediente,
                        tipo="SAIDA",
                        quantidade=consumo,
                        observacao=f"Producao de {request.form['produto']}"
                    )

                    db.session.add(mov_receita)

            item_estoque = Estoque.query.filter_by(
                produto=request.form["produto"]
            ).first()

            if item_estoque:
                item_estoque.quantidade -= float(
                    request.form["quantidade"]
                )

            db.session.commit()

            return redirect("/producao")

        producoes = Producao.query.order_by(
            Producao.id.desc()
        ).all()

        produtos = Estoque.query.order_by(
            Estoque.produto
        ).all()

        return render_template(
            "producao.html",
            producoes=producoes,
            produtos=produtos
        )

    @app.route("/produtos", methods=["GET", "POST"])
    def produtos():

        if request.method == "POST":

            novo_produto = Produto(
                nome=request.form["nome"],
                categoria=request.form.get("categoria"),
                unidade=request.form.get("unidade"),
                estoque_minimo=float(
                    request.form.get("estoque_minimo", 0)
                )
            )

            db.session.add(novo_produto)
            db.session.commit()

            return redirect("/produtos")

        produtos = Produto.query.order_by(
            Produto.nome
        ).all()

        return render_template(
            "produtos.html",
            produtos=produtos
        )

    @app.route("/ficha-tecnica", methods=["GET", "POST"])
    def ficha_tecnica():

        if request.method == "POST":

            nova_receita = ReceitaProducao(
                produto_final=request.form["produto_final"],
                ingrediente=request.form["ingrediente"],
                quantidade=float(
                    request.form["quantidade"]
                ),
                unidade=request.form["unidade"]
            )

            db.session.add(nova_receita)
            db.session.commit()

            return redirect("/ficha-tecnica")

        receitas = ReceitaProducao.query.order_by(
            ReceitaProducao.produto_final
        ).all()

        return render_template(
            "ficha_tecnica.html",
            receitas=receitas
        )

    @app.route("/vendas", methods=["GET", "POST"])
    def vendas():

        if request.method == "POST":

            quantidade = float(
                request.form["quantidade"]
            )

            valor_unitario = float(
                request.form["valor_unitario"]
            )

            valor_total = quantidade * valor_unitario

            nova_venda = Venda(
                produto=request.form["produto"],
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total
            )

            db.session.add(nova_venda)

            item = Estoque.query.filter_by(
                produto=request.form["produto"]
            ).first()

            if item:
                item.quantidade -= quantidade

            mov = MovimentoEstoque(
                produto=request.form["produto"],
                tipo="SAIDA",
                quantidade=quantidade,
                observacao="Venda"
            )

            db.session.add(mov)

            db.session.commit()

            return redirect("/vendas")

        vendas = Venda.query.order_by(
            Venda.id.desc()
        ).all()

        produtos = Estoque.query.order_by(
            Estoque.produto
        ).all()

        return render_template(
            "vendas.html",
            vendas=vendas,
            produtos=produtos
        )

    @app.route("/movimentos")
    def movimentos():

        movimentos = MovimentoEstoque.query.order_by(
            MovimentoEstoque.id.desc()
        ).all()

        return render_template(
            "movimentos.html",
            movimentos=movimentos
        )

    @app.route("/relatorios")
    def relatorios():

        receita_total = db.session.query(
            db.func.sum(Receita.valor)
        ).scalar() or 0

        despesa_total = db.session.query(
            db.func.sum(Despesa.valor)
        ).scalar() or 0

        vendas_total = db.session.query(
            db.func.sum(Venda.valor_total)
        ).scalar() or 0

        lucro_total = (
            receita_total +
            vendas_total -
            despesa_total
        )

        return render_template(
            "relatorios.html",
            receita_total=receita_total,
            despesa_total=despesa_total,
            vendas_total=vendas_total,
            lucro_total=lucro_total
        )

    @app.route("/relatorio-pdf")
    def relatorio_pdf():

        receita_total = db.session.query(
            db.func.sum(Receita.valor)
        ).scalar() or 0

        despesa_total = db.session.query(
            db.func.sum(Despesa.valor)
        ).scalar() or 0

        vendas_total = db.session.query(
            db.func.sum(Venda.valor_total)
        ).scalar() or 0

        lucro_total = (
            receita_total +
            vendas_total -
            despesa_total
        )

        arquivo = os.path.abspath("relatorio_panifica.pdf")

        pdf = canvas.Canvas(arquivo)

        pdf.setTitle("Relatorio Financeiro")

        pdf.drawString(
            100,
            800,
            "PANIFICA PRO 360 - Relatorio Financeiro"
        )

        pdf.drawString(
            100,
            760,
            f"Receita: R$ {receita_total:.2f}"
        )

        pdf.drawString(
            100,
            740,
            f"Vendas: R$ {vendas_total:.2f}"
        )

        pdf.drawString(
            100,
            720,
            f"Despesas: R$ {despesa_total:.2f}"
        )

        pdf.drawString(
            100,
            700,
            f"Lucro: R$ {lucro_total:.2f}"
        )

        pdf.save()

        print("PDF GERADO:", arquivo)

        return send_file(
            arquivo,
            as_attachment=True,
            download_name="relatorio_panifica.pdf"
        )

    @app.route("/ia-financeira")
    def ia_financeira():

        total_vendas = Venda.query.count()

        total_compras = Compra.query.count()

        produtos_estoque = Estoque.query.count()

        produtos_criticos = 0

        produtos = Produto.query.all()

        for produto in produtos:

            item = Estoque.query.filter_by(
                produto=produto.nome
            ).first()

            if item and item.quantidade <= produto.estoque_minimo:
                produtos_criticos += 1

        return render_template(
            "ia_financeira.html",
            total_vendas=total_vendas,
            total_compras=total_compras,
            produtos_estoque=produtos_estoque,
            produtos_criticos=produtos_criticos
        )

    return app
