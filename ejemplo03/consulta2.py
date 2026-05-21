from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Curso, Instructor
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

cursos = session.query(Curso).join(Curso.instructor).filter(Instructor.nombre.like('%Zam%')).all()

print('Cursos con profesor que contiene "Zam" en su nombre')
for curso in cursos:
    print(f'Curso: {curso.titulo} - Profesor: {curso.instructor.nombre}')
    print('---------')
