class Tecnico:
    """
    Representa a un técnico de mantenimiento.

    Atributos:
        id (str): Identificador único del técnico.
        nombre (str): Nombre completo del técnico.
        especialidad (str): Área de especialidad del técnico.
    """

    def __init__(self, id: str, nombre: str, especialidad: str):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
