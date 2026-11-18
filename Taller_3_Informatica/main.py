"""
Taller 3 - Informática 1

"""

import csv
import json
import logging
import os
import random
import re
from pathlib import Path

#rutas y config.

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TXT_DIR = DATA_DIR / "txt"
CSV_DIR = DATA_DIR / "csv"
JSON_DIR = DATA_DIR / "json"
LOG_FILE = BASE_DIR / "log.txt"

for carpeta in (TXT_DIR, CSV_DIR, JSON_DIR):
    carpeta.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

CAMPOS = ["id", "fr", "fc", "spo2"]

#patrones
PATRONES = {
    "id": re.compile(r"^ID-\d{3}$"),
    "fr": re.compile(r"^\d{1,3}\sAños$"),
    "fc": re.compile(r"^\d{3}ppm$"),
    "spo2": re.compile(r"^\d{2,3}%$")
}


#procesamiento de datos

def generar_registros(cantidad=50):
    """Genera registros biomédicos aleatorios con los campos del taller."""
    registros = []

    for numero in range(1, cantidad + 1):
        edad = random.randint(18, 90)
        frecuencia = random.randint(50, 130)
        saturacion = random.randint(90, 100)

        registro = {
            "id": f"ID-{numero:03d}",
            "fr": f"{edad} Años",
            "fc": f"{frecuencia:03d}ppm",
            "spo2": f"{saturacion}%"
        }
        registros.append(registro)

    logging.info("Se generaron %s registros biomédicos.", cantidad)
    return registros


def valor_numerico(texto, sufijo):
    """Extrae la parte numérica de un campo como '090ppm' o '95%'."""
    return int(texto.replace(sufijo, "").strip())


def ordenar_por_fc(registros):
    """Ordena los registros de menor a mayor frecuencia cardíaca."""
    ordenados = sorted(
        registros,
        key=lambda registro: valor_numerico(registro["fc"], "ppm")
    )
    logging.info("Los registros se ordenaron por frecuencia cardíaca.")
    return ordenados


# validaciones-

def validar_registro(registro):
    """Comprueba que estén los cuatro campos y que cumplan sus patrones."""
    errores = []

    for campo in CAMPOS:
        if campo not in registro:
            errores.append(f"Falta el campo {campo}.")
        elif not isinstance(registro[campo], str):
            errores.append(f"El campo {campo} debe ser texto.")
        elif not PATRONES[campo].fullmatch(registro[campo]):
            errores.append(f"Formato incorrecto en {campo}: {registro[campo]}")

    return errores


def validar_registros(registros):
    """Muestra el resultado de validar una lista de registros."""
    validos = []
    invalidos = []

    for registro in registros:
        errores = validar_registro(registro)
        if errores:
            invalidos.append((registro, errores))
        else:
            validos.append(registro)

    print(f"\nRegistros válidos: {len(validos)}")
    print(f"Registros inválidos: {len(invalidos)}")

    for registro, errores in invalidos:
        print(f"\n{registro.get('id', 'Sin ID')}:")
        for error in errores:
            print(f"  - {error}")

    logging.info(
        "Validación realizada: %s válidos y %s inválidos.",
        len(validos), len(invalidos)
    )
    return validos, invalidos


#exp. e imp. de arch.

def exportar_txt(registros):
    ruta = TXT_DIR / "registros.txt"
    with ruta.open("w", encoding="utf-8") as archivo:
        for r in registros:
            archivo.write(
                f"ID: {r['id']} | Edad: {r['fr']} | "
                f"Frecuencia cardíaca: {r['fc']} | SpO2: {r['spo2']}\n"
            )
    logging.info("Archivo TXT exportado: %s", ruta)
    print(f"Archivo TXT guardado en: {ruta}")


def exportar_csv(registros):
    ruta = CSV_DIR / "registros.csv"
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(registros)
    logging.info("Archivo CSV exportado: %s", ruta)
    print(f"Archivo CSV guardado en: {ruta}")


def exportar_json(registros):
    ruta = JSON_DIR / "registros.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=4)
    logging.info("Archivo JSON exportado: %s", ruta)
    print(f"Archivo JSON guardado en: {ruta}")


def importar_json():
    ruta = JSON_DIR / "registros.json"

    if not ruta.exists():
        print("No existe data/json/registros.json. Primero exporta o copia un JSON allí.")
        logging.warning("Se intentó importar un JSON que no existe.")
        return []

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El JSON debe contener una lista de registros.")

        validos, invalidos = validar_registros(datos)
        logging.info("Se importaron %s registros válidos desde JSON.", len(validos))
        return validos

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"No fue posible importar el JSON: {error}")
        logging.exception("Error al importar JSON.")
        return []


def exportar_todos_los_formatos(registros):
    try:
        exportar_txt(registros)
        exportar_csv(registros)
        exportar_json(registros)
    except OSError as error:
        print(f"Error al guardar los archivos: {error}")
        logging.exception("Error durante la exportación.")


#conectar mongo

def conectar_mongodb():
    """
    La URI se lee de la variable de entorno MONGODB_URI.
    No escribas la contraseña directamente en este archivo.
    """
    try:
        from pymongo import MongoClient
    except ImportError:
        print("Falta instalar PyMongo. En la consola de Spyder ejecuta: %pip install pymongo")
        logging.exception("PyMongo no está instalado.")
        return None

    uri = os.getenv("MONGODB_URI")

    if not uri:
        print("\nNo se encontró la variable MONGODB_URI.")
        print("Configúrala con la cadena de conexión de MongoDB Atlas.")
        logging.warning("Conexión a MongoDB no realizada: falta MONGODB_URI.")
        return None

    try:
        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        cliente.admin.command("ping")
        base_datos = cliente["taller_informatica"]
        coleccion = base_datos["signos vitales"]
        print("Conexión exitosa con MongoDB Atlas.")
        logging.info("Conexión exitosa con MongoDB Atlas.")
        return cliente, coleccion

    except Exception as error:
        print(f"No se pudo conectar con MongoDB: {error}")
        logging.exception("Error de conexión con MongoDB.")
        return None


def preparar_documento(registro):
    """Añade campos numéricos para facilitar las consultas en MongoDB."""
    documento = dict(registro)
    documento["edad_valor"] = valor_numerico(registro["fr"], "Años")
    documento["fc_valor"] = valor_numerico(registro["fc"], "ppm")
    documento["spo2_valor"] = valor_numerico(registro["spo2"], "%")
    return documento


def insertar_en_mongodb(registros):
    validos, invalidos = validar_registros(registros)
    if not validos:
        print("No hay registros válidos para insertar.")
        return

    conexion = conectar_mongodb()
    if conexion is None:
        return

    cliente, coleccion = conexion
    try:
        documentos = [preparar_documento(r) for r in validos]
        resultado = coleccion.insert_many(documentos)
        print(f"Se insertaron {len(resultado.inserted_ids)} documentos.")
        logging.info("Se insertaron %s documentos en MongoDB.", len(resultado.inserted_ids))
    except Exception as error:
        print(f"Error al insertar: {error}")
        logging.exception("Error al insertar documentos.")
    finally:
        cliente.close()


def consultar_mongodb():
    conexion = conectar_mongodb()
    if conexion is None:
        return

    cliente, coleccion = conexion
    try:
        # Promedio de frecuencia cardíaca
        resultado_promedio = list(coleccion.aggregate([
            {"$group": {"_id": None, "promedio_fc": {"$avg": "$fc_valor"}}}
        ]))

        if resultado_promedio:
            promedio = resultado_promedio[0]["promedio_fc"]
            print(f"\nPromedio de frecuencia cardíaca: {promedio:.2f} ppm")
        else:
            print("\nNo hay registros en la colección para calcular el promedio.")

        # Registros con SpO2 menor a 94
        bajos = list(coleccion.find(
            {"spo2_valor": {"$lt": 94}},
            {"_id": 0}
        ))

        print(f"\nRegistros con SpO2 menor a 94%: {len(bajos)}")
        for documento in bajos:
            print(documento)

        ruta_resultados = JSON_DIR / "resultados_mongo.json"
        salida = {
            "promedio_frecuencia_cardiaca": (
                resultado_promedio[0]["promedio_fc"] if resultado_promedio else None
            ),
            "registros_spo2_menor_94": bajos
        }

        with ruta_resultados.open("w", encoding="utf-8") as archivo:
            json.dump(salida, archivo, ensure_ascii=False, indent=4, default=str)

        print(f"\nConsultas exportadas en: {ruta_resultados}")
        logging.info("Consultas de MongoDB ejecutadas y exportadas.")

    except Exception as error:
        print(f"Error durante las consultas: {error}")
        logging.exception("Error al consultar MongoDB.")
    finally:
        cliente.close()


def consultar_por_id():
    identificacion = input("Escribe el ID que deseas buscar (ej. ID-001): ").strip()

    if not PATRONES["id"].fullmatch(identificacion):
        print("El ID no tiene el formato ID-001.")
        return

    conexion = conectar_mongodb()
    if conexion is None:
        return

    cliente, coleccion = conexion
    try:
        documento = coleccion.find_one({"id": identificacion}, {"_id": 0})
        if documento:
            print("\nRegistro encontrado:")
            print(json.dumps(documento, ensure_ascii=False, indent=4))
        else:
            print("No se encontró ese ID en MongoDB.")
    except Exception as error:
        print(f"Error al buscar: {error}")
        logging.exception("Error al consultar por ID.")
    finally:
        cliente.close()


# hacer menú

def mostrar_registros(registros):
    if not registros:
        print("Todavía no hay registros cargados.")
        return

    print("\nID       | Edad      | FC       | SpO2")
    print("-" * 43)
    for r in registros:
        print(f"{r['id']:<8} | {r['fr']:<9} | {r['fc']:<8} | {r['spo2']}")


def menu():
    registros = []

    while True:
        print("\nMENÚ:")
        print("1. Generar 50 registros aleatorios")
        print("2. Mostrar registros")
        print("3. Ordenar por frecuencia cardíaca")
        print("4. Validar registros")
        print("5. Exportar archivos TXT, CSV y JSON")
        print("6. Importar registros desde JSON")
        print("7. Insertar registros en MongoDB Atlas")
        print("8. Ejecutar consultas de MongoDB y exportar resultados")
        print("9. Buscar un registro en MongoDB por ID")
        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            registros = generar_registros(50)
            print("Se generaron 50 registros.")
            registros = ordenar_por_fc(registros)

        elif opcion == "2":
            mostrar_registros(registros)

        elif opcion == "3":
            registros = ordenar_por_fc(registros)
            print("Registros ordenados por frecuencia cardíaca.")
            mostrar_registros(registros)

        elif opcion == "4":
            validar_registros(registros)

        elif opcion == "5":
            if registros:
                registros = ordenar_por_fc(registros)
                exportar_todos_los_formatos(registros)
            else:
                print("Primero genera o importa registros.")

        elif opcion == "6":
            importados = importar_json()
            if importados:
                registros = ordenar_por_fc(importados)
                print(f"Se cargaron {len(registros)} registros.")

        elif opcion == "7":
            if registros:
                insertar_en_mongodb(registros)
            else:
                print("Primero genera o importa registros.")

        elif opcion == "8":
            consultar_mongodb()

        elif opcion == "9":
            consultar_por_id()

        elif opcion == "0":
            logging.info("El programa finalizó.")
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()
