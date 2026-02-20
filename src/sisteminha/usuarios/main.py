from ..database.main import DatabaseService
from ..models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError, OperationalError
from tabulate import tabulate
import arrow


class UsuarioService:
    def __init__(self, dao: "UsuarioDAO"):
        self.dao = dao

    def novo_usuario(self) -> None:
        email = input("Digite o email para login: ")
        nome = input("Digite o nome do usuário: ")
        senha = input("Escolha uma senha: ")
        usuario = Usuario(nome=nome, email=email, senha=senha)
        try:
            self.dao.criar(usuario)
            print(f"Usuário '{nome}' criado com sucesso.")
        except IntegrityError:
            print("Erro: já existe um usuário com esse e-mail.")
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")

    def alterar_usuario(self) -> None:
        email = input("Digite o e-mail do usuário: ")
        try:
            usuario = self.dao.buscar_por_email(email)
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return
        if usuario is None:
            print("Usuário não encontrado.")
            return
        print(f"Nome atual: {usuario.nome}")
        novo_nome = input("Novo nome (deixe em branco para manter): ").strip()
        if not novo_nome or novo_nome == usuario.nome:
            print("Nome não alterado.")
            return
        try:
            self.dao.atualizar_nome(usuario, novo_nome)
            print(f"Nome atualizado para '{novo_nome}'.")
        except OperationalError as e:
            print(f"Erro ao atualizar o banco de dados: {e}")

    def mudar_senha(self) -> None:
        email = input("Digite o e-mail do usuário: ")
        try:
            usuario = self.dao.buscar_por_email(email)
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return
        if usuario is None:
            print("Usuário não encontrado.")
            return
        senha_antiga = input("Digite a senha atual: ")
        senha_nova = input("Digite a nova senha: ")
        try:
            sucesso = self.dao.atualizar_senha(usuario, senha_antiga, senha_nova)
            if sucesso:
                print("Senha alterada com sucesso.")
            else:
                print("Erro: senha atual incorreta.")
        except OperationalError as e:
            print(f"Erro ao atualizar o banco de dados: {e}")

    def remover_usuario(self) -> None:
        email = input("Digite o e-mail do usuário a remover: ")
        try:
            self.dao.deletar(email)
            print("Usuário removido com sucesso.")
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")

    def listar_usuarios(self) -> None:
        try:
            usuarios = self.dao.listar()
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
        rows = [(u.nome, u.email) for u in usuarios]
        print(tabulate(rows, headers=["Nome", "E-mail"], tablefmt="rounded_outline"))

    def login(self) -> None:
        email = input("E-mail: ")
        senha = input("Senha: ")
        try:
            if self.dao.login(email, senha):
                print("Login realizado com sucesso. Bem vindo!")
            else:
                print("E-mail ou senha incorretos.")
        except OperationalError as e:
            print(f"Erro ao acessar o banco de dados: {e}")


class UsuarioDAO:
    def __init__(self, db: DatabaseService):
        self.db = db

    def criar(self, usuario: Usuario) -> None:
        agora = arrow.utcnow().datetime
        cursor = self.db.connection.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (usuario.nome, usuario.email, usuario.senha, agora, agora),
        )
        self.db.connection.commit()

    def buscar_por_email(self, email: str) -> Usuario | None:
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT nome, email, senha FROM usuarios WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        usuario = object.__new__(Usuario)
        usuario.nome, usuario.email, usuario.senha = row
        return usuario

    def listar(self) -> list[Usuario]:
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT nome, email, senha FROM usuarios")
        usuarios = []
        for row in cursor.fetchall():
            usuario = object.__new__(Usuario)
            usuario.nome, usuario.email, usuario.senha = row
            usuarios.append(usuario)
        return usuarios

    def atualizar_nome(self, usuario: Usuario, novo_nome: str) -> None:
        agora = arrow.utcnow().datetime
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE usuarios SET nome = ?, updated_at = ? WHERE email = ?",
            (novo_nome, agora, usuario.email),
        )
        self.db.connection.commit()
        usuario.nome = novo_nome

    def atualizar_senha(self, usuario: Usuario, senha_antiga: str, senha_nova: str) -> bool:
        if not check_password_hash(usuario.senha, senha_antiga):
            return False
        nova_senha_hash = generate_password_hash(senha_nova)
        agora = arrow.utcnow().datetime
        cursor = self.db.connection.cursor()
        cursor.execute(
            "UPDATE usuarios SET senha = ?, updated_at = ? WHERE email = ?",
            (nova_senha_hash, agora, usuario.email),
        )
        self.db.connection.commit()
        usuario.senha = nova_senha_hash
        return True

    def deletar(self, email: str) -> None:
        cursor = self.db.connection.cursor()
        cursor.execute(
            "DELETE FROM usuarios WHERE email = ?",
            (email,),
        )
        self.db.connection.commit()

    def login(self, email: str, senha: str) -> bool:
        usuario = self.buscar_por_email(email)
        if usuario is None:
            return False
        return check_password_hash(usuario.senha, senha)
