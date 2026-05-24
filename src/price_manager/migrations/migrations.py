import csv
import os

from sqlalchemy import text

from price_manager.database.connection import ConexionDB


CARPETA_CSV = (
  "/content/price_manager/"
  "src/price_manager/migrations/csv"
)

CARPETA_SQL = (
  "/content/price_manager/"
  "src/price_manager/migrations/sql"
)


def guardar_sql(nombre_archivo: str, sentencias: list[str]) -> None:
  """
      Crea un archivo sql con un conjunto de sentencias en la ruta especificada.
      Args:
          nombre_archivo:
              El nombre del archivo a crear.

          sentencias:
              Una lista con las sentencias a copiar.
  """
  os.makedirs(CARPETA_SQL, exist_ok=True)

  ruta = os.path.join(CARPETA_SQL, nombre_archivo)

  with open(ruta, mode="w", encoding="utf-8") as archivo:
    archivo.write("\n".join(sentencias))


def formatear_valor(valor):
  if isinstance(valor, str):
    return f"'{valor}'"

  return str(valor)


def generar_insert_sql(tabla: str, columnas: list[str], valores: list) -> str:
  """
      Devuelve una cadena con el query para realizar una insercion.
      Args:
          tabla:
              El nombre de la tabla.

          columnas:
              Una lista con los nombres de los campos.

          valores:
              Una lista con los valores a colocar en el insert.
  """
  columnas_sql = ", ".join(columnas)
  valores_sql = ", ".join([formatear_valor(valor) for valor in valores])

  return f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({valores_sql});"


def migrar_datos() -> None:
  """
      Utilizando la conexion, ejecuta las sentencias necesarias para migrar los
      datos a SQL.
  """

  with ConexionDB() as cn:

    # =========================
    # CATEGORIAS
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "categorias.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Categoria (Id, Nombre)
            VALUES (:id, :nombre)
            """
          ),
          {
            "id": int(fila["id"]),
            "nombre": fila["nombre"]
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Categoria",
            ["Id", "Nombre"],
            [fila["id"], fila["nombre"]]
          )
        )

    guardar_sql("categorias.sql", sentencias)

    # =========================
    # PROVEEDORES
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "proveedores.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Proveedor (Id, Nombre, Contacto)
            VALUES (:id, :nombre, :contacto)
            """
          ),
          {
            "id": int(fila["id"]),
            "nombre": fila["nombre"],
            "contacto": fila["contacto"]
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Proveedor",
            ["Id", "Nombre", "Contacto"],
            [fila["id"], fila["nombre"], fila["contacto"]]
          )
        )

    guardar_sql("proveedores.sql", sentencias)

    # =========================
    # MONEDAS
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "monedas.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Moneda (Id, Nombre)
            VALUES (:id, :nombre)
            """
          ),
          {
            "id": int(fila["id"]),
            "nombre": fila["nombre"]
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Moneda",
            ["Id", "Nombre"],
            [fila["id"], fila["nombre"]]
          )
        )

    guardar_sql("monedas.sql", sentencias)

    # =========================
    # TIPOS COTIZACION
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "tiposCotizacion.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Tipo_Cotizacion (Id, Nombre)
            VALUES (:id, :nombre)
            """
          ),
          {
            "id": int(fila["id"]),
            "nombre": fila["nombre"]
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Tipo_Cotizacion",
            ["Id", "Nombre"],
            [fila["id"], fila["nombre"]]
          )
        )

    guardar_sql("tiposCotizacion.sql", sentencias)

    # =========================
    # PRODUCTOS
    # =========================
    sentencias_producto = []

    ruta = os.path.join(CARPETA_CSV, "productos.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:

        cn.execute(
          text(
            """
            INSERT INTO Producto
            (
              Id,
              Nombre,
              Descripcion,
              Precio,
              Id_Moneda,
              Id_Categoria,
              Id_Proveedor
            )
            VALUES
            (
              :id,
              :nombre,
              :descripcion,
              :precio,
              :id_moneda,
              :id_categoria,
              :id_proveedor
            )
            """
          ),
          {
            "id": int(fila["id"]),
            "nombre": fila["nombre"],
            "descripcion": fila["descripcion"],
            "precio": fila["precio"],
            "id_moneda": int(fila["id_moneda"]),
            "id_categoria": int(fila["categoria_id"]),
            "id_proveedor": int(fila["proveedor_id"])
          }
        )

        sentencias_producto.append(
          generar_insert_sql(
            "Producto",
            [
              "Id",
              "Nombre",
              "Descripcion",
              "Precio",
              "Id_Moneda",
              "Id_Categoria",
              "Id_Proveedor"
            ],
            [
              fila["id"],
              fila["nombre"],
              fila["descripcion"],
              fila["precio"],
              fila["id_moneda"],
              fila["categoria_id"],
              fila["proveedor_id"]
            ]
          )
        )

    guardar_sql("productos.sql", sentencias_producto)

    # =========================
    # PRECIO HISTORICO
    # =========================

    sentencias = []

    precios_historicos = [
      [1, 1, 135000.0, "2025-10-01", 1],
      [2, 1, 142000.0, "2025-11-01", 1],
      [3, 2, 78000.0, "2025-10-01", 1],
      [4, 2, 82000.0, "2025-11-01", 1],
      [5, 5, 850.0, "2025-10-01", 2],
      [6, 5, 880.0, "2025-11-01", 2],
    ]

    for precio in precios_historicos:
      cn.execute(
        text(
          """
          INSERT INTO Precio_Historico
          (
            Id_Precio,
            Id_Producto,
            Valor,
            Fecha,
            Id_Moneda
          )
          VALUES
          (
            :id_precio,
            :id_producto,
            :valor,
            :fecha,
            :id_moneda
          )
          """
        ),
        {
          "id_precio": precio[0],
          "id_producto": precio[1],
          "valor": precio[2],
          "fecha": precio[3],
          "id_moneda": precio[4],
        }
      )

      sentencias.append(
        generar_insert_sql(
          "Precio_Historico",
          [
            "Id_Precio",
            "Id_Producto",
            "Valor",
            "Fecha",
            "Id_Moneda",
          ],
          precio,
        )
      )

    guardar_sql("precio_historico.sql", sentencias)

    # =========================
    # STOCK
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "stock.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Stock (Id_Producto, Cantidad)
            VALUES (:id_producto, :cantidad)
            """
          ),
          {
            "id_producto": int(fila["id_producto"]),
            "cantidad": int(fila["cantidad"])
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Stock",
            ["Id_Producto", "Cantidad"],
            [fila["id_producto"], fila["cantidad"]]
          )
        )

    guardar_sql("stock.sql", sentencias)

    # =========================
    # COTIZACION DOLAR
    # =========================
    sentencias = []
    ruta = os.path.join(CARPETA_CSV, "cotizacion.csv")

    with open(ruta, mode="r", encoding="utf-8") as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        cn.execute(
          text(
            """
            INSERT INTO Cotizacion_Dolar
            (
              Valor,
              Id_Tipo_Cotizacion,
              Fecha
            )
            VALUES
            (
              :valor,
              :id_tipo,
              :fecha
            )
            """
          ),
          {
            "valor": float(fila["valor"]),
            "id_tipo": int(fila["id_tipo"]),
            "fecha": fila["fecha"]
          }
        )

        sentencias.append(
          generar_insert_sql(
            "Cotizacion_Dolar",
            ["Valor", "Id_Tipo_Cotizacion", "Fecha"],
            [fila["valor"], fila["id_tipo"], fila["fecha"]]
          )
        )

    guardar_sql("cotizacion_dolar.sql", sentencias)

  print("Migración finalizada correctamente.")
