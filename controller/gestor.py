from datetime import datetime
from controller.persistencia import Persistencia
from model.equipo import Equipo
from model.tarea import MantenimientoPreventivo, MantenimientoCorrectivo
from model.tecnico import Tecnico


class GestorMantenimientos:
    def __init__(self):
        self.equipos = Persistencia.cargar_equipos()
        self.tecnicos = Persistencia.cargar_tecnicos()
        self.tareas = Persistencia.cargar_tareas()

    def registrar_equipo(self, id, nombre, ubicacion):
        self.equipos.append(Equipo(id, nombre, ubicacion))
        Persistencia.guardar_equipos(self.equipos)

    def registrar_tecnico(self, id, nombre, especialidad):
        self.tecnicos.append(Tecnico(id, nombre, especialidad))
        Persistencia.guardar_tecnicos(self.tecnicos)

    def planificar_mantenimiento(self, tipo, id, equipo_id, tecnico_id, fecha_str, observaciones=""):
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        tarea = MantenimientoPreventivo(id, equipo_id, tecnico_id, fecha, observaciones) if tipo == "preventivo" \
            else MantenimientoCorrectivo(id, equipo_id, tecnico_id, fecha, observaciones)
        self.tareas.append(tarea)
        Persistencia.guardar_tareas(self.tareas)
