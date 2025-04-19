from abc import ABC, abstractmethod
from datetime import datetime


class TareaMantenimiento(ABC):
    """
    Clase abstracta para tareas de mantenimiento.

    Atributos:
        id (str): ID único de la tarea.
        equipo_id (str): ID del equipo a mantener.
        tecnico_id (str): ID del técnico asignado.
        fecha (datetime): Fecha de realización o programación.
        observaciones (str): Observaciones relevantes.
    """

    def __init__(self, id: str, equipo_id: str, tecnico_id: str, fecha: datetime, observaciones: str = ""):
        self.id = id
        self.equipo_id = equipo_id
        self.tecnico_id = tecnico_id
        self.fecha = fecha
        self.observaciones = observaciones

    @abstractmethod
    def tipo(self) -> str:
        """Devuelve el tipo de mantenimiento."""
        pass


class MantenimientoPreventivo(TareaMantenimiento):
    def tipo(self) -> str:
        return "Preventivo"


class MantenimientoCorrectivo(TareaMantenimiento):
    def tipo(self) -> str:
        return "Correctivo"
