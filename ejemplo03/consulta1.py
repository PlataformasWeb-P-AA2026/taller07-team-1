from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import Entrega, Tarea, Curso, Instructor, Estudiante
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

entregas = session.query(Entrega).join(Entrega.estudiante).join(Entrega.tarea).join(Tarea.curso).join(Curso.instructor).all()

print("Entregas")
for entrega in entregas:
    estudiante = entrega.estudiante
    tarea = entrega.tarea
    curso = tarea.curso
    instructor = curso.instructor
    print(f"Estudiante: {estudiante.nombre} - Título: {tarea.titulo} - Profesor: {instructor.nombre}")
    print("---------")
