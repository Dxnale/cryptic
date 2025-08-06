import argparse

def saludar(arg : str) -> str:
    return f"Hola {arg} esta es mi primera funcion importable en python!"

def cli() -> None:
    args = argparse.ArgumentParser(description="Un saludador simple que funciona con un nombre o un fichero de texto.")
    args.add_argument("name", help="Nombre de la persona a saludar")
    args = args.parse_args()
    print(saludar(arg=args.name))
