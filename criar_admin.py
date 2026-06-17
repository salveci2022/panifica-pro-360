from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    usuario = Usuario(
        nome="Administrador",
        email="admin@panificapro360.com.br",
        senha=generate_password_hash("Panifica@2026"),
        perfil="admin",
        ativo=True
    )

    db.session.add(usuario)
    db.session.commit()

    print("Administrador criado com sucesso!")