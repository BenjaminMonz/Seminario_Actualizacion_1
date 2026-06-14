import os

from sqlalchemy import text

from price_manager.database.connection import ConexionDB
from price_manager.services.audit_service import auditar_operacion


CARPETA_SQL = (
  "/content/price_manager/"
  "src/price_manager/migrations/sql"
)


def leer_sentencias_sql(ruta_archivo: str) -> list[str]:
  """
  Lee un archivo SQL y devuelve sus sentencias individuales.

  Args:
      ruta_archivo:
          Ruta completa del archivo SQL a procesar.

  Retorna:
      Lista de sentencias SQL encontradas.
  """
  with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
    contenido = archivo.read()

  sentencias = [
    sentencia.strip()
    for sentencia in contenido.split(";")
    if sentencia.strip()
  ]

  return sentencias


def cargar_sql(nombre_archivo: str) -> int:
  """
  Ejecuta las sentencias de un archivo SQL sobre la base de datos.

  Args:
      nombre_archivo:
          Nombre del archivo SQL ubicado en la carpeta de migraciones.

  Retorna:
      Cantidad de sentencias ejecutadas.
  """
  ruta_archivo = os.path.join(CARPETA_SQL, nombre_archivo)

  if not os.path.exists(ruta_archivo):
    raise FileNotFoundError(
      f"No existe el archivo SQL: {ruta_archivo}"
    )

  sentencias = leer_sentencias_sql(ruta_archivo)

  with ConexionDB() as cn:
    for sentencia in sentencias:
      cn.execute(text(sentencia))

  return len(sentencias)


@auditar_operacion("CARGA_DATOS_SQL")
def cargar_datos_desde_sql() -> dict[str, int]:
  """
  Ejecuta los archivos SQL de carga inicial en un orden seguro.

  Retorna:
      Diccionario con el nombre del archivo y la cantidad de sentencias
      ejecutadas por cada script.
  """
  orden_archivos = [
    "tipos_cotizacion.sql",
    "categorias.sql",
    "monedas.sql",
    "proveedores.sql",
    "productos.sql",
    "precio_historico.sql",
    "stock.sql",
    "cotizaciones.sql",
  ]

  resultado = {}

  for nombre_archivo in orden_archivos:
    resultado[nombre_archivo] = cargar_sql(nombre_archivo)

  return resultado
