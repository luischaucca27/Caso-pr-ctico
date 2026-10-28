from abc import ABC, abstractmethod


# ==========================================================
# 1. CLASE CONSTRUCTOR Y ENCAPSULAMIENTO
# ==========================================================

class Matricula:
    """Representa la matrícula general de un estudiante."""

    def __init__(self, nombre, semestre="2026-II"):
        self.nombre = nombre
        self.__semestre = semestre
        self.__costo_base = 60.00

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self.__nombre = valor.strip()

    @property
    def semestre(self):
        return self.__semestre

    @property
    def costo_base(self):
        return self.__costo_base

    def calcular_costo(self):
        """Devuelve el derecho base de matrícula."""
        return self.costo_base

    def mostrar_resumen(self):
        print(f"Estudiante : {self.nombre}")
        print(f"Semestre   : {self.semestre}")
        print(f"Total      : S/ {self.calcular_costo():.2f}")


# ==========================================================
# 2. HERENCIA SIMPLE Y SOBRESCRITURA CON SUPER()
# ==========================================================

class MatriculaBecada(Matricula):
    """Reduce a la mitad el monto recibido."""

    def calcular_costo(self):
        return super().calcular_costo() / 2


class MatriculaDesaprobatoria(Matricula):
    """Agrega S/ 15.00 por índice académico desaprobatorio."""

    def calcular_costo(self):
        return super().calcular_costo() + 15.00


class MatriculaExtemporanea(Matricula):
    """Agrega S/ 15.00 por matrícula fuera de fecha."""

    def calcular_costo(self):
        return super().calcular_costo() + 15.00


# ==========================================================
# 3. HERENCIA MÚLTIPLE: VERSIONES DE LOS PROGRAMADORES
# ==========================================================

class MatriculaCombinada1(
    MatriculaBecada,
    MatriculaDesaprobatoria,
    MatriculaExtemporanea
):
    """Primera versión: beca, desaprobación y extemporánea."""
    pass


class MatriculaCombinada2(
    MatriculaDesaprobatoria,
    MatriculaExtemporanea,
    MatriculaBecada
):
    """Segunda versión: desaprobación, extemporánea y beca."""
    pass


def mostrar_mro(clase):
    """Muestra el orden de resolución de métodos."""
    print(" -> ".join(
        elemento.__name__ for elemento in clase.mro()
    ))


def demostrar_herencia_multiple():
    print("\n=== HERENCIA MÚLTIPLE: PROBLEMA ORIGINAL ===")

    # El enunciado no indica qué versión usó cada estudiante.
    # Para demostrar el caso, asignamos la primera a Luis
    # y la segunda a Rosa.
    luis = MatriculaCombinada1("Luis Huamaní Cárdenas")
    rosa = MatriculaCombinada2("Rosa Ccahuana Prado")

    print("\nPRIMERA VERSIÓN")
    luis.mostrar_resumen()
    print("MRO:")
    mostrar_mro(MatriculaCombinada1)
    print("Cálculo: (60 + 15 + 15) / 2 = S/ 45.00")

    print("\nSEGUNDA VERSIÓN")
    rosa.mostrar_resumen()
    print("MRO:")
    mostrar_mro(MatriculaCombinada2)
    print("Cálculo: (60 / 2) + 15 + 15 = S/ 60.00")

    diferencia = abs(
        luis.calcular_costo() - rosa.calcular_costo()
    )
    print(f"\nDiferencia de cobro: S/ {diferencia:.2f}")

    print("\nRELACIÓN 'ES UN'")
    print("¿Luis tiene una matrícula general?",
          isinstance(luis, Matricula))
    print("¿Luis tiene una matrícula becada?",
          isinstance(luis, MatriculaBecada))

    print("\nCAUSA DE LA DIFERENCIA")
    print("super() continúa por el MRO del objeto.")
    print("Cada modificación se aplica cuando retorna super().")
    print("En la versión 1, la beca se aplica al final.")
    print("En la versión 2, la beca se aplica antes de los recargos.")
    print("Ambas definiciones son válidas: no hay error de sintaxis.")


# ==========================================================
# 4. COMBINACIÓN INCORRECTA: GENERAL ANTES DE ESPECIALIZACIÓN
# ==========================================================

def demostrar_mro_inconsistente():
    print("\n=== CLASE GENERAL ANTES DE LA ESPECIALIZACIÓN ===")

    try:
        class MatriculaIncorrecta(Matricula, MatriculaBecada):
            pass

    except TypeError as error:
        print(f"TypeError: {error}")
        print(
            "No puede construirse un MRO consistente: "
            "MatriculaBecada debe preceder a Matricula, "
            "pero la declaración exige el orden contrario."
        )


# ==========================================================
# 5. REDISEÑO: CLASE ABSTRACTA PARA LAS REGLAS
# ==========================================================

class ReglaCobro(ABC):
    """Define el contrato de una regla de cobro."""

    @property
    @abstractmethod
    def descripcion(self):
        pass

    @abstractmethod
    def aplicar(self, monto):
        pass


class RecargoExtemporaneo(ReglaCobro):
    @property
    def descripcion(self):
        return "Recargo por matrícula extemporánea"

    def aplicar(self, monto):
        return monto + 15.00


class RecargoDesaprobatorio(ReglaCobro):
    @property
    def descripcion(self):
        return "Recargo por índice desaprobatorio"

    def aplicar(self, monto):
        return monto + 15.00


class BecaViolenciaSociopolitica(ReglaCobro):
    @property
    def descripcion(self):
        return "Beca: reducción del 50 %"

    def aplicar(self, monto):
        return monto / 2


# ==========================================================
# 6. COMPOSICIÓN: LA MATRÍCULA TIENE REGLAS ORDENADAS
# ==========================================================

class MatriculaConReglas(Matricula):
    """Aplica reglas en el orden en que se agregan."""

    def __init__(self, nombre, semestre="2026-II"):
        super().__init__(nombre, semestre)
        self.__reglas = []

    def agregar_regla(self, regla):
        if not isinstance(regla, ReglaCobro):
            raise TypeError("Debe proporcionar una regla de cobro.")
        self.__reglas.append(regla)

    def calcular_costo(self):
        monto = super().calcular_costo()

        for regla in self.__reglas:
            monto = regla.aplicar(monto)

        return monto

    def mostrar_detalle(self):
        print(f"\nEstudiante: {self.nombre}")
        print(f"Semestre: {self.semestre}")

        monto = self.costo_base
        print(f"  Derecho base: S/ {monto:.2f}")

        for regla in self.__reglas:
            monto = regla.aplicar(monto)
            print(f"  {regla.descripcion}: S/ {monto:.2f}")

        print(f"TOTAL: S/ {monto:.2f}")


def configurar_reglas(
    matricula,
    fuera_de_fecha,
    indice_desaprobatorio,
    es_becario,
    beca_al_final=True
):
    """Selecciona las reglas según la situación del estudiante."""

    if es_becario and not beca_al_final:
        matricula.agregar_regla(BecaViolenciaSociopolitica())

    if fuera_de_fecha:
        matricula.agregar_regla(RecargoExtemporaneo())

    if indice_desaprobatorio:
        matricula.agregar_regla(RecargoDesaprobatorio())

    if es_becario and beca_al_final:
        matricula.agregar_regla(BecaViolenciaSociopolitica())


def demostrar_rediseno():
    print("\n=== REDISEÑO: ORDEN EXPLÍCITO DE LAS REGLAS ===")

    # Política elegida: la beca reduce el total con recargos.
    # Se aplica la misma política a ambos estudiantes.
    for nombre in ("Luis Huamaní Cárdenas", "Rosa Ccahuana Prado"):
        matricula = MatriculaConReglas(nombre)

        configurar_reglas(
            matricula,
            fuera_de_fecha=True,
            indice_desaprobatorio=True,
            es_becario=True,
            beca_al_final=True
        )

        matricula.mostrar_detalle()

    # Ejemplo de la otra política posible.
    print("\n=== EJEMPLO: BECA ANTES DE LOS RECARGOS ===")
    alternativa = MatriculaConReglas("Estudiante de ejemplo")

    configurar_reglas(
        alternativa,
        fuera_de_fecha=True,
        indice_desaprobatorio=True,
        es_becario=True,
        beca_al_final=False
    )

    alternativa.mostrar_detalle()


# ==========================================================
# 7. PROGRAMA PRINCIPAL
# ==========================================================

if __name__ == "__main__":
    demostrar_herencia_multiple()
    demostrar_mro_inconsistente()
    demostrar_rediseno()
