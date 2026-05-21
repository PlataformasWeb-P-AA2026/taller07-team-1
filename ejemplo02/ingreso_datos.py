from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tablas import Club, Jugador

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# carpeta donde están los archivos de texto
base_dir = Path(__file__).resolve().parent
archivo_clubs = base_dir / 'data' / 'datos_clubs.txt'
archivo_jugadores = base_dir / 'data' / 'datos_jugadores.txt'

# se crea un diccionario para guardar los clubs
clubs = {}

with open(archivo_clubs, encoding='utf-8') as archivo:
    for linea in archivo:
        linea = linea.strip()

        partes = [parte.strip() for parte in linea.split(';')]
        if len(partes) != 3:
            print(f"Línea de club inválida: {linea}")
            continue

        nombre, deporte, fundacion_texto = partes
        try:
            fundacion = int(fundacion_texto)
        except ValueError:
            print(f"Fundación inválida para club {nombre}: {fundacion_texto}")
            continue

        club = Club(nombre=nombre, deporte=deporte, fundacion=fundacion)
        session.add(club)
        clubs[nombre] = club

# se confirma los clubs antes de crear jugadores
session.commit()

with open(archivo_jugadores, encoding='utf-8') as archivo:
    for linea in archivo:
        linea = linea.strip()

        partes = [parte.strip() for parte in linea.split(';')]
        if len(partes) == 4:
            club_nombre, posicion, dorsal_texto, nombre = partes
            try:
                dorsal = int(dorsal_texto)
            except ValueError:
                dorsal = None
        elif len(partes) == 3:
            club_nombre, posicion, nombre = partes
            dorsal = None
        else:
            print(f"Línea de jugador inválida: {linea}")
            continue

        club = clubs.get(club_nombre)
        if club is None:
            print(f"Club no encontrado para jugador {nombre}: {club_nombre}")
            continue

        jugador = Jugador(nombre=nombre, dorsal=dorsal, posicion=posicion, club=club)
        session.add(jugador)

# se confirma las transacciones
session.commit()

print('Carga de datos finalizada.')
