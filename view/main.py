import tkinter as tk
from tkinter import ttk, messagebox
from controller.gestor import GestorMantenimientos


class Aplicacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Mantenimiento Industrial")
        self.root.geometry("800x600")

        self.gestor = GestorMantenimientos()

        self._aplicar_estilos()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self._crear_tab_equipos()
        self._crear_tab_tecnicos()
        self._crear_tab_tareas()

        self.root.mainloop()

    def _aplicar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#f8f9fa",
                        foreground="#212529",
                        rowheight=28,
                        fieldbackground="#f8f9fa",
                        font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#dee2e6",
                        foreground="#343a40")

        style.map("Treeview",
                  background=[("selected", "#0d6efd")],
                  foreground=[("selected", "#ffffff")])

    def _crear_tab_equipos(self):
        self.tab_equipos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_equipos, text="Equipos")

        btn = tk.Button(self.tab_equipos, text="Registrar equipo", command=self.mostrar_formulario_equipo)
        btn.pack(pady=10)

        self.tree_equipos = ttk.Treeview(self.tab_equipos, columns=("ID", "Nombre", "Ubicación"), show="headings")
        for col in self.tree_equipos["columns"]:
            self.tree_equipos.heading(col, text=col)
            self.tree_equipos.column(col, width=200)
        self.tree_equipos.pack(expand=True, fill="both", padx=20, pady=10)

    def _crear_tab_tecnicos(self):
        self.tab_tecnicos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tecnicos, text="Técnicos")

        btn = tk.Button(self.tab_tecnicos, text="Registrar técnico", command=self.mostrar_formulario_tecnico)
        btn.pack(pady=10)

        self.tree_tecnicos = ttk.Treeview(self.tab_tecnicos, columns=("ID", "Nombre", "Especialidad"), show="headings")
        for col in self.tree_tecnicos["columns"]:
            self.tree_tecnicos.heading(col, text=col)
            self.tree_tecnicos.column(col, width=200)
        self.tree_tecnicos.pack(expand=True, fill="both", padx=20, pady=10)

    def _crear_tab_tareas(self):
        self.tab_tareas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tareas, text="Tareas")

        btn = tk.Button(self.tab_tareas, text="Registrar tarea", command=self.mostrar_formulario_tarea)
        btn.pack(pady=10)

        self.tree_tareas = ttk.Treeview(
            self.tab_tareas,
            columns=("ID", "Tipo", "Equipo", "Técnico", "Fecha", "Observaciones"),
            show="headings"
        )
        for col in self.tree_tareas["columns"]:
            self.tree_tareas.heading(col, text=col)
            self.tree_tareas.column(col, width=150)
        self.tree_tareas.pack(expand=True, fill="both", padx=20, pady=10)

    def mostrar_formulario_equipo(self):
        self._crear_formulario_generico(
            "Registrar equipo",
            ["ID", "Nombre", "Ubicación"],
            lambda datos: self._guardar_equipo(*datos)
        )

    def mostrar_formulario_tecnico(self):
        self._crear_formulario_generico(
            "Registrar técnico",
            ["ID", "Nombre", "Especialidad"],
            lambda datos: self._guardar_tecnico(*datos)
        )

    def mostrar_formulario_tarea(self):
        ventana = tk.Toplevel()
        ventana.title("Registrar tarea de mantenimiento")
        ventana.geometry("400x400")

        labels = ["ID tarea", "ID equipo", "ID técnico", "Fecha (YYYY-MM-DD)", "Observaciones", "Tipo"]
        entradas = {}

        for idx, campo in enumerate(labels[:-1]):
            tk.Label(ventana, text=campo).grid(row=idx, column=0, pady=5, sticky="e")
            entrada = tk.Entry(ventana, width=30)
            entrada.grid(row=idx, column=1, pady=5)
            entradas[campo] = entrada

        tipo_var = tk.StringVar(value="preventivo")
        tipo_combo = ttk.Combobox(ventana, textvariable=tipo_var, values=["preventivo", "correctivo"])
        tipo_combo.grid(row=len(labels) - 1, column=1, pady=5)
        entradas["Tipo"] = tipo_var

        def guardar():
            equipo_id = entradas["ID equipo"].get()
            tecnico_id = entradas["ID técnico"].get()

            if not any(e.id == equipo_id for e in self.gestor.equipos):
                messagebox.showwarning("Equipo no encontrado", f"El equipo con ID '{equipo_id}' no existe.")
                return

            if not any(t.id == tecnico_id for t in self.gestor.tecnicos):
                messagebox.showwarning("Técnico no encontrado", f"El técnico con ID '{tecnico_id}' no existe.")
                return

            try:
                self.gestor.planificar_mantenimiento(
                    entradas["Tipo"].get(),
                    entradas["ID tarea"].get(),
                    equipo_id,
                    tecnico_id,
                    entradas["Fecha (YYYY-MM-DD)"].get(),
                    entradas["Observaciones"].get()
                )
                self.tree_tareas.insert("", "end", values=(
                    entradas["ID tarea"].get(),
                    entradas["Tipo"].get().capitalize(),
                    equipo_id,
                    tecnico_id,
                    entradas["Fecha (YYYY-MM-DD)"].get(),
                    entradas["Observaciones"].get()
                ))
                messagebox.showinfo("Éxito", "Tarea registrada.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        tk.Button(ventana, text="Registrar", command=guardar).grid(columnspan=2, row=len(labels)+1, pady=15)

    def _crear_formulario_generico(self, titulo, campos, callback_guardar):
        ventana = tk.Toplevel()
        ventana.title(titulo)
        ventana.geometry("400x300")

        entradas = []
        for idx, campo in enumerate(campos):
            tk.Label(ventana, text=campo).grid(row=idx, column=0, pady=5, sticky="e")
            entrada = tk.Entry(ventana, width=30)
            entrada.grid(row=idx, column=1, pady=5)
            entradas.append(entrada)

        def guardar():
            datos = [e.get() for e in entradas]
            if all(datos):
                callback_guardar(datos)
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Completa todos los campos")

        tk.Button(ventana, text="Guardar", command=guardar).grid(columnspan=2, row=len(campos)+1, pady=15)

    def _guardar_equipo(self, id_, nombre, ubicacion):
        self.gestor.registrar_equipo(id_, nombre, ubicacion)
        self.tree_equipos.insert("", "end", values=(id_, nombre, ubicacion))
        messagebox.showinfo("Éxito", "Equipo registrado correctamente")

    def _guardar_tecnico(self, id_, nombre, especialidad):
        self.gestor.registrar_tecnico(id_, nombre, especialidad)
        self.tree_tecnicos.insert("", "end", values=(id_, nombre, especialidad))
        messagebox.showinfo("Éxito", "Técnico registrado correctamente")


if __name__ == "__main__":
    Aplicacion()
