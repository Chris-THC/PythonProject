import json
import os
from datetime import datetime

from model.equipo import Equipo
from model.tarea import MantenimientoPreventivo, MantenimientoCorrectivo
from model.tecnico import Tecnico


class Persistencia:
    @staticmethod
    def guardar_equipos(equipos: list, ruta="data/equipos.json"):
        # Asegura que la carpeta 'data' exista en la raíz del proyecto
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        datos = [{"id": e.id, "nombre": e.nombre, "ubicacion": e.ubicacion} for e in equipos]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    @staticmethod
    def cargar_equipos(ruta="data/equipos.json"):
        equipos = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for e in datos:
                    equipos.append(Equipo(e["id"], e["nombre"], e["ubicacion"]))
        except FileNotFoundError:
            # Log de que el archivo no se encontró, útil para depuración
            print(f"Advertencia: El archivo '{ruta}' no fue encontrado. Se devolverá una lista de equipos vacía.")
        return equipos

    @staticmethod
    def guardar_tecnicos(tecnicos: list, ruta="data/tecnicos.json"):
        # Asegura que la carpeta 'data' exista en la raíz del proyecto
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        datos = [{"id": t.id, "nombre": t.nombre, "especialidad": t.especialidad} for t in tecnicos]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    @staticmethod
    def cargar_tecnicos(ruta="data/tecnicos.json"):
        tecnicos = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for t in datos:
                    tecnicos.append(Tecnico(t["id"], t["nombre"], t["especialidad"]))
        except FileNotFoundError:
            # Log de que el archivo no se encontró, útil para depuración
            print(f"Advertencia: El archivo '{ruta}' no fue encontrado. Se devolverá una lista de técnicos vacía.")
        return tecnicos

    @staticmethod
    def guardar_tareas(tareas: list, ruta="data/tareas.json"):
        # Asegura que la carpeta 'data' exista en la raíz del proyecto
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        datos = []
        for t in tareas:
            datos.append({
                "id": t.id,
                "tipo": t.tipo(),
                "equipo_id": t.equipo_id,
                "tecnico_id": t.tecnico_id,
                "fecha": t.fecha.strftime("%Y-%m-%d"),
                "observaciones": t.observaciones
            })
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    @staticmethod
    def cargar_tareas(ruta="data/tareas.json"):
        tareas = []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for t in datos:
                    clase = MantenimientoPreventivo if t["tipo"] == "Preventivo" else MantenimientoCorrectivo
                    fecha = datetime.strptime(t["fecha"], "%Y-%m-%d")
                    tareas.append(clase(t["id"], t["equipo_id"], t["tecnico_id"], fecha, t["observaciones"]))
        except FileNotFoundError:
            # Log de que el archivo no se encontró, útil para depuración
            print(f"Advertencia: El archivo '{ruta}' no fue encontrado. Se devolverá una lista de tareas vacía.")
        return tareas
