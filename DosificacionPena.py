class DosificacionPena:
    def __init__(self, pena_minima, pena_maxima):
        """
        Inicializa la calculadora con los límites básicos de la pena
        """
        self.pena_minima = pena_minima
        self.pena_maxima = pena_maxima
        self.cuartos = self._calcular_cuartos()

    def _calcular_cuartos(self):
        """
        Calcula los rangos de los cuartos
        """
        ambito_movilidad = self.pena_maxima - self.pena_minima
        tamano_cuarto = ambito_movilidad / 4

        return {
            'minimo': (self.pena_minima, self.pena_minima + tamano_cuarto),
            'medio_inferior': (self.pena_minima + tamano_cuarto, self.pena_minima + (2 * tamano_cuarto)),
            'medio_superior': (self.pena_minima + (2 * tamano_cuarto), self.pena_maxima - tamano_cuarto),
            'maximo': (self.pena_maxima - tamano_cuarto, self.pena_maxima)
        }

    def aplicar_modificador(self, tipo, proporcion):
        """
        Aplica modificadores según el artículo 60
        """
        if tipo == "aumento_determinado":
            self.pena_minima *= (1 + proporcion)
            self.pena_maxima *= (1 + proporcion)
        elif tipo == "aumento_hasta":
            self.pena_maxima *= (1 + proporcion)
        elif tipo == "disminucion_hasta":
            self.pena_minima *= (1 - proporcion)
        
        self.cuartos = self._calcular_cuartos()

    def determinar_cuarto_aplicable(self, tiene_agravantes, tiene_atenuantes):
        """
        Determina el cuarto aplicable según circunstancias
        """
        if not tiene_agravantes and not tiene_atenuantes:
            return 'minimo'
        elif tiene_agravantes and not tiene_atenuantes:
            return 'maximo'
        elif tiene_agravantes and tiene_atenuantes:
            return 'medio_inferior'  # o 'medio_superior' según el caso
        else:  # solo atenuantes
            return 'minimo'

    def calcular_pena(self, tiene_agravantes, tiene_atenuantes, factores_especificos=0.5):
        """
        Calcula la pena final considerando todos los factores
        factores_especificos es un valor entre 0 y 1 que representa la ponderación
        de los factores del inciso 3 del artículo 61
        """
        cuarto_aplicable = self.determinar_cuarto_aplicable(tiene_agravantes, tiene_atenuantes)
        rango_aplicable = self.cuartos[cuarto_aplicable]
        
        # Calcula un punto específico dentro del cuarto aplicable
        pena_final = rango_aplicable[0] + ((rango_aplicable[1] - rango_aplicable[0]) * factores_especificos)
        
        return {
            'pena_final': round(pena_final, 2),
            'cuarto_aplicable': cuarto_aplicable,
            'rango_aplicable': rango_aplicable
        }

# Ejemplo de uso
def ejemplo_practico():
    """
    Ejemplo práctico de dosificación de pena para un delito
    """
    # Ejemplo: Hurto simple (Art 239 CP)
    # Pena base: 32 a 108 meses
    dosificacion = DosificacionPena(32, 108)
    
    # Supongamos un caso con agravante por destreza (art 241.10)
    # Aumenta hasta en la mitad
    dosificacion.aplicar_modificador("aumento_hasta", 0.5)
    
    # Calculamos la pena con agravantes pero sin atenuantes
    # Factores específicos: gravedad media (0.5)
    resultado = dosificacion.calcular_pena(
        tiene_agravantes=True,
        tiene_atenuantes=False,
        factores_especificos=0.5
    )
    
    print("\nEjemplo de Hurto Simple Agravado:")
    print(f"Pena base: 32 a 108 meses")
    print(f"Después de agravante: {dosificacion.pena_minima} a {dosificacion.pena_maxima} meses")
    print(f"Cuarto aplicable: {resultado['cuarto_aplicable']}")
    print(f"Rango del cuarto: {resultado['rango_aplicable'][0]:.2f} a {resultado['rango_aplicable'][1]:.2f} meses")
    print(f"Pena final: {resultado['pena_final']} meses")

if __name__ == "__main__":
    ejemplo_practico()