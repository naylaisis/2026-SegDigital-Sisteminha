import argparse
from importlib.metadata import version

from sisteminha.database.main import DatabaseService
from sisteminha.usuarios import UsuarioService, UsuarioDAO

DB_PATH = "sisteminha.db"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sisteminha",
        description="SedDigital Sisteminha CLI",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('sisteminha')}",
    )
    parser.add_argument(
        "--db",
        default=DB_PATH,
        metavar="ARQUIVO",
        help=f"Caminho para o arquivo do banco de dados (padrão: {DB_PATH})",
    )
    args = parser.parse_args()

    db = DatabaseService(args.db)
    db.connect()
    db.inicializar()

    dao = UsuarioDAO(db)
    service = UsuarioService(dao)

    print("Bem vindo!")
    print("=" * 60)

    while True:
        print()
        print("Escolha uma opção")
        print("[1] Criar usuário")
        print("[2] Listar usuários")
        print("[3] Alterar nome de usuário")
        print("[4] Mudar senha")
        print("[5] Remover usuário")
        print("[6] Login")
        print("[0] Sair")
        try:
            opcao = int(input())
        except ValueError:
            print("Apenas números")
            continue
        match opcao:
            case 1:
                service.novo_usuario()
            case 2:
                service.listar_usuarios()
            case 3:
                service.alterar_usuario()
            case 4:
                service.mudar_senha()
            case 5:
                service.remover_usuario()
            case 6:
                service.login()
            case 0:
                break
            case _:
                print("Opção inválida!")

    db.disconnect()


if __name__ == "__main__":
    main()
