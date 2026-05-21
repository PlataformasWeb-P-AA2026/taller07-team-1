from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Curso
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

cursos = session.query(Curso).all()

print('Cursos y sus tareas asociadas')
for curso in cursos:
    print(f'Curso: {curso.titulo}')
    for tarea in curso.tareas:
        print(f'  Tarea: {tarea.titulo} - Fecha entrega: {tarea.fecha_entrega}')
    print('---------')
