from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Inscripcion, Estudiante, Curso, Instructor
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

inscripciones = (
    session.query(Inscripcion)
    .join(Inscripcion.estudiante)
    .join(Inscripcion.curso)
    .join(Curso.instructor)
    .filter(Curso.departamento.has(nombre='Ciencias de la Computación'))
    .all()
)

print('Inscripciones del departamento de Ciencias de la Computación')
for inscripcion in inscripciones:
    estudiante = inscripcion.estudiante
    curso = inscripcion.curso
    profesor = curso.instructor
    print(f'Estudiante: {estudiante.nombre} - Curso: {curso.titulo} - Profesor: {profesor.nombre}')
    print('---------')
