import sqlite3
import hashlib
import os

class BancoDados:
    """Gerencia a conexão e operações no SQLite."""
    def __init__(self, nome_banco="usuarios.db"):
        self.conn = sqlite3.connect(nome_banco)
        self.cursor = self.conn.cursor()
        self.criar_tabela() 

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def fechar(self):
        self.conn.close()

class SistemaRegistro:
    def __init__(self, db):
        self.db = db

    def _hash_senha(self, senha):
        """Cria um hash SHA-256 para segurança."""
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar(self, username, senha, email):
        try:
            senha_hash = self._hash_senha(senha)
            self.db.cursor.execute(
                "INSERT INTO usuarios (username, senha, email) VALUES (?, ?, ?)",
                (username, senha_hash, email)
            )
            self.db.conn.commit()
            print(f"\n[✓] Usuário '{username}' cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            print("\n[!] Erro: Este nome de usuário já existe.")

    def autenticar(self, username, senha):
        senha_hash = self._hash_senha(senha)
        self.db.cursor.execute(
            "SELECT * FROM usuarios WHERE username = ? AND senha = ?",
            (username, senha_hash)
        )
        if self.db.cursor.fetchone():
            print(f"\n[OK] Bem-vindo de volta, {username}!")
            return True
        print("\n[X] Erro: Usuário ou senha incorretos.")
        return False

    def listar_usuarios(self):
        self.db.cursor.execute("SELECT id, username, email FROM usuarios")
        usuarios = self.db.cursor.fetchall()
        print("\n--- Lista de Usuários ---")
        for user in usuarios:
            print(f"ID: {user[0]} | Usuário: {user[1]} | Email: {user[2]}")

def menu():
    db = BancoDados()
    sistema = SistemaRegistro(db)

    while True:
        print("\n=== SISTEMA DE REGISTRO PYTHON ===")
        print("1. Cadastrar Usuário")
        print("2. Fazer Login")
        print("3. Listar Usuários")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            user = input("Nome de usuário: ")
            mail = input("E-mail: ")
            pw = input("Senha: ")
            sistema.cadastrar(user, pw, mail)
        
        elif opcao == '2':
            user = input("Usuário: ")
            pw = input("Senha: ")
            sistema.autenticar(user, pw)
            
        elif opcao == '3':
            sistema.listar_usuarios()
            
        elif opcao == '4':
            db.fechar()
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()