from typing import List
from model.tarea import TareaMantenimiento


class Equipo:
    """
    Representa un equipo de la planta industrial.

    Atributos:
        id (str): Identificador único del equipo.
        nombre (str): Nombre del equipo.
        ubicacion (str): Ubicación del equipo dentro de la planta.
        tareas (List[TareaMantenimiento]): Lista de tareas de mantenimiento asociadas al equipo.
    """

    def __init__(self, id: str, nombre: str, ubicacion: str):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.tareas: List[TareaMantenimiento] = []

    def agregar_tarea(self, tarea: TareaMantenimiento):
        self.tareas.append(tarea)
