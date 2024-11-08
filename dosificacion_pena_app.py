import tkinter as tk
from tkinter import ttk

from dosificacion_pena import DosificacionPena

class DosificacionPenaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Dosificación Punitiva")
        self.geometry("400x300")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Etiquetas e inputs
        tk.Label(self, text="Pena Mínima (meses):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.pena_minima_entry = tk.Entry(self)
        self.pena_minima_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Pena Máxima (meses):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.pena_maxima_entry = tk.Entry(self)
        self.pena_maxima_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="¿Tiene Agravantes?").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.tiene_agravantes = tk.BooleanVar()
        self.agravantes_checkbox = tk.Checkbutton(self, variable=self.tiene_agravantes)
        self.agravantes_checkbox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="¿Tiene Atenuantes?").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.tiene_atenuantes = tk.BooleanVar()
        self.atenuantes_checkbox = tk.Checkbutton(self, variable=self.tiene_atenuantes)
        self.atenuantes_checkbox.grid(row=3, column=1, padx=10, pady=10)

        # Botón de Cálculo
        self.calcular_button = tk.Button(self, text="Calcular Pena", command=self.calcular_pena)
        self.calcular_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Resultados
        self.resultado_label = tk.Label(self, text="")
        self.resultado_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def calcular_pena(self):
        try:
            pena_minima = float(self.pena_minima_entry.get())
            pena_maxima = float(self.pena_maxima_entry.get())

            dosificacion = DosificacionPena(pena_minima, pena_maxima)

            tiene_agravantes = self.tiene_agravantes.get()
            tiene_atenuantes = self.tiene_atenuantes.get()

            resultado = dosificacion.calcular_pena(tiene_agravantes, tiene_atenuantes, factores_especificos=0.5)

            self.resultado_label.config(text=f"Pena Final: {resultado['pena_final']} meses\nCuarto Aplicable: {resultado['cuarto_aplicable']}")

        except ValueError:
            self.resultado_label.config(text="Por favor, ingresa valores numéricos válidos.")

if __name__ == "__main__":
    app = DosificacionPenaApp()
    app.mainloop()