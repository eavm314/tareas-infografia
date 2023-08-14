estudiantes = [
    {
        'nombre': 'juan',
        'apellido': 'perez',
        'notas': {
            'MAT': 30,
            'QMC': 30,
            'FIS': 30,
            'LAB': 30
        },
        'extras': [2, 3, 1, 1, 1],
        'asistencia': 90
    },
    {
        'nombre': 'ana',
        'apellido': 'rivera',
        'notas': {
            'MAT': 98,
            'QMC': 98,
            'FIS': 98,
            'LAB': 98
        },
        'extras': [1],
        'asistencia': 100
    }
]


class Evaluador:
    """Esta clase implementa diversas funciones para calcular promedios
    de una lista de estudiantes y obtener otros datos adicionales, ademas,
    tambien implementa una funcion para escribir un reporte de notas"""
    def __init__(self, lista_estudiantes, min_asistencia, max_extras):
        self.lista_estudiantes = lista_estudiantes
        self.min_asistencia = min_asistencia
        self.max_extras = max_extras

    def calcular_promedio_estudiante(self, estudiante):
        if "notas" not in estudiante:
            return 0
        if len(estudiante["notas"]) == 0:
            return 0
        if estudiante["asistencia"] < self.min_asistencia:
            return 0
        
        promedio = sum(dict(estudiante["notas"]).values())/len(estudiante["notas"])
        extras = min(sum(estudiante["extras"]), self.max_extras)

        total = min(100, promedio + extras)
        return total
            
    def calcular_promedios(self):
        # IMPLEMENTAR METODO
        self.lista_notas = [{
            "nombre completo": f"{str(e['nombre']).capitalize()} {str(e['apellido']).capitalize()}",
            "promedio": self.calcular_promedio_estudiante(e),
        } for e in self.lista_estudiantes]

        return self.lista_notas

    def obtener_mejor_estudiante(self):
        # IMPLEMENTAR METODO
        return max(self.lista_notas, key=lambda item: item["promedio"])

    def get_estudiante_data(self, estudiante):
        nota_final = self.calcular_promedio_estudiante(estudiante)
        data = {
            "Nombre Completo": f"{str(estudiante['nombre']).capitalize()} {str(estudiante['apellido']).capitalize()}",
            "Asistencia": str(estudiante["asistencia"]),
            "MAT": str(estudiante["notas"]["MAT"]) if "MAT" in estudiante["notas"] else 0,
            "FIS": str(estudiante["notas"]["FIS"]) if "FIS" in estudiante["notas"] else 0,
            "QMC": str(estudiante["notas"]["QMC"]) if "QMC" in estudiante["notas"] else 0,
            "LAB": str(estudiante["notas"]["LAB"]) if "LAB" in estudiante["notas"] else 0,
            "Total Extras": str(min(sum(estudiante["extras"]), self.max_extras)),
            "Promedio Final": str(nota_final),
            "Observacion": "APROBADO" if nota_final > 50 else "REPROBADO",
        }

        return ",".join(data.values())

    def salvar_datos(self, nombre_archivo):
        # IMPLEMENTAR METODO
        contenido = f"Nombre Completo,Asistencia,MAT,FIS,QMC,LAB,Total Extras,Promedio Final,Observacion\n{chr(10).join(self.get_estudiante_data(e) for e in self.lista_estudiantes)}"

        print('salvando datos')

        with open(nombre_archivo, "w") as tabla_notas:
            tabla_notas.write(contenido)
            tabla_notas.close()


# -----------------------------------------#
# ----> NO MODIFICAR DESDE AQUI! <---------#
# -----------------------------------------#
def comparar_archivo_notas(archivo):
    with open('ejemplo_notas.csv', 'r') as archivo_correcto:
        correcto_str = archivo_correcto.read()

    with open(archivo, 'r') as archivo:
        archivo_str = archivo.read()

    return correcto_str == archivo_str


if __name__ == '__main__':
    # datos iniciales
    nombre_archivo = 'notas.csv'
    notas_correcto = [{'nombre completo': 'Juan Perez', 'promedio': 35.0}, {'nombre completo': 'Ana Rivera', 'promedio': 99.0}]
    mejor_correcto = {'nombre completo': 'Ana Rivera', 'promedio': 99.0}

    # Instanciar evaluador
    evaluador = Evaluador(lista_estudiantes=estudiantes, min_asistencia=80, max_extras=5)
    # calcular promedios
    notas = evaluador.calcular_promedios()
    print(f'calcular_promedios: {notas}')
    if notas == notas_correcto:
        print('Calculo de promedios correcto!')
    else:
        print(f'ERROR, lista de promedios esperada: {notas_correcto}')
    # obtener mejor estudiante
    mejor = evaluador.obtener_mejor_estudiante()
    print(f'obtener_mejor_estudiante: {mejor}')
    if mejor == mejor_correcto:
        print('Mejor estudiante correcto!')
    else:
        print(f'ERROR, mejor estudiante esperado: {mejor_correcto}')
    # salvar datos en archivo
    evaluador.salvar_datos(nombre_archivo)
    if comparar_archivo_notas(nombre_archivo):
        print('Generacion de archivo correcta')
    else:
        print('Generacion de archivos incorrecta, ver archivo "ejemplo_notas.csv"')