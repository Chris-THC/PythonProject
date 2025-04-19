import json
from model.equipo import Equipo
from model.tecnico import Tecnico
from model.tarea import MantenimientoPreventivo, MantenimientoCorrectivo
from datetime import datetime
from typing import List


class GestorMantenimientos:
    """
    Clase para gestionar la lógica del sistema de mantenimiento.
    """

    def __init__(self):
        self.equipos: List[Equipo] = []
        self.tecnicos: List[Tecnico] = []
        self.tareas = []

    def registrar_equipo(self, id: str, nombre: str, ubicacion: str):
        equipo = Equipo(id, nombre, ubicacion)
        self.equipos.append(equipo)

    def registrar_tecnico(self, id: str, nombre: str, especialidad: str):
        tecnico = Tecnico(id, nombre, especialidad)
        self.tecnicos.append(tecnico)

    def planificar_mantenimiento(self, tipo: str, id: str, equipo_id: str, tecnico_id: str, fecha_str: str,
                                 observaciones=""):
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        tarea = MantenimientoPreventivo(id, equipo_id, tecnico_id, fecha, observaciones) if tipo == "preventivo" \
            else MantenimientoCorrectivo(id, equipo_id, tecnico_id, fecha, observaciones)
        self.tareas.append(tarea)
