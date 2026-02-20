import argparse
from importlib.metadata import version


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
    parser.parse_args()


if __name__ == "__main__":
    main()
