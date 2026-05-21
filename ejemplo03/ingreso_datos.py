from pathlib import Path
import csv
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clases import (
    Departamento,
    Instructor,
    Curso,
    Estudiante,
    Inscripcion,
    Tarea,
    Entrega,
)
from configuracion import cadena_base_datos

engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

base_dir = Path(__file__).resolve().parent


def parse_datetime(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


def cargar_csv(ruta):
    with open(ruta, encoding='utf-8', newline='') as archivo:
        return list(csv.DictReader(archivo, delimiter=','))


def main():
    departamentos = {}
    instructores = {}
    cursos = {}
    estudiantes = {}

    # Departamentos
    for fila in cargar_csv(base_dir / '01_departamento.csv'):
        departamento = Departamento(
            id=int(fila['id']),
            nombre=fila['nombre'],
        )
        session.add(departamento)
        departamentos[departamento.id] = departamento

    # Instructores
    for fila in cargar_csv(base_dir / '02_instructor.csv'):
        instructor = Instructor(
            id=int(fila['id']),
            nombre=fila['nombre'],
        )
        session.add(instructor)
        instructores[instructor.id] = instructor

    # Cursos
    for fila in cargar_csv(base_dir / '03_curso.csv'):
        curso = Curso(
            id=int(fila['id']),
            titulo=fila['titulo'],
            departamento_id=int(fila['departamento_id']),
            instructor_id=int(fila['instructor_id']),
        )
        session.add(curso)
        cursos[curso.id] = curso

    # Estudiantes
    for fila in cargar_csv(base_dir / '04_estudiante.csv'):
        estudiante = Estudiante(
            id=int(fila['id']),
            nombre=fila['nombre'],
        )
        session.add(estudiante)
        estudiantes[estudiante.id] = estudiante

    # Inscripciones
    for fila in cargar_csv(base_dir / '05_inscripcion.csv'):
        inscripcion = Inscripcion(
            estudiante_id=int(fila['estudiante_id']),
            curso_id=int(fila['curso_id']),
            fecha_inscripcion=parse_datetime(fila['fecha_inscripcion']),
        )
        session.add(inscripcion)

    # Tareas
    for fila in cargar_csv(base_dir / '06_tarea.csv'):
        tarea = Tarea(
            id=int(fila['id']),
            curso_id=int(fila['curso_id']),
            titulo=fila['titulo'],
            fecha_entrega=parse_datetime(fila['fecha_entrega']),
        )
        session.add(tarea)

    # Entregas
    for fila in cargar_csv(base_dir / '07_entrega.csv'):
        entrega = Entrega(
            id=int(fila['id']),
            tarea_id=int(fila['tarea_id']),
            estudiante_id=int(fila['estudiante_id']),
            fecha_envio=parse_datetime(fila['fecha_envio']),
            calificacion=float(fila['calificacion']),
        )
        session.add(entrega)

    session.commit()
    print('Carga de datos finalizada.')


if __name__ == '__main__':
    main()
