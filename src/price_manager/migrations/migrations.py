import csv
import os
from typing import Any

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
  """Guarda sentencias SQL en la carpeta de migraciones."""
  os.makedirs(CARPETA_SQL, exist_ok=True)

  ruta = os.path.join(CARPETA_SQL, nombre_archivo)

  with open(ruta, mode="w", encoding="utf-8") as archivo:
    archivo.write("\n".join(sentencias))


def formatear_valor(valor: Any) -> str:
  """Convierte valores de Python a formato válido para SQL."""
  if isinstance(valor, str):
    valor_limpio = valor.replace("'", "''")
    return f"'{valor_limpio}'"

  return str(valor)


def generar_insert_sql(
  tabla: str,
  columnas: list[str],
  valores: list[Any],
) -> str:
  """Genera una sentencia INSERT para registrar la migración."""
  columnas_sql = ", ".join(columnas)
  valores_sql = ", ".join([
    formatear_valor(valor)
    for valor in valores
  ])

  return (
    f"INSERT INTO {tabla} "
    f"({columnas_sql}) VALUES ({valores_sql});"
  )


def leer_csv(nombre_archivo: str) -> list[dict]:
  """Lee un archivo CSV proveniente del Sprint 1."""
  ruta = os.path.join(CARPETA_CSV, nombre_archivo)

  with open(ruta, mode="r", encoding="utf-8") as archivo:
    return list(csv.DictReader(archivo))


def migrar_categorias(cn) -> None:
  """Migra categorías desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("categorias.csv"):
    cn.execute(
      text("""
        INSERT INTO Categoria (Id, Nombre)
        VALUES (:id, :nombre)
      """),
      {
        "id": int(fila["id"]),
        "nombre": fila["nombre"],
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Categoria",
        ["Id", "Nombre"],
        [fila["id"], fila["nombre"]],
      )
    )

  guardar_sql("categorias.sql", sentencias)


def migrar_proveedores(cn) -> None:
  """Migra proveedores desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("proveedores.csv"):
    cn.execute(
      text("""
        INSERT INTO Proveedor (Id, Nombre, Contacto)
        VALUES (:id, :nombre, :contacto)
      """),
      {
        "id": int(fila["id"]),
        "nombre": fila["nombre"],
        "contacto": fila["contacto"],
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Proveedor",
        ["Id", "Nombre", "Contacto"],
        [fila["id"], fila["nombre"], fila["contacto"]],
      )
    )

  guardar_sql("proveedores.sql", sentencias)


def migrar_monedas(cn) -> None:
  """Migra monedas desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("monedas.csv"):
    cn.execute(
      text("""
        INSERT INTO Moneda (Id, Nombre)
        VALUES (:id, :nombre)
      """),
      {
        "id": int(fila["id"]),
        "nombre": fila["nombre"],
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Moneda",
        ["Id", "Nombre"],
        [fila["id"], fila["nombre"]],
      )
    )

  guardar_sql("monedas.sql", sentencias)


def migrar_tipos_cotizacion(cn) -> None:
  """Migra tipos de cotización desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("tipos_cotizacion.csv"):
    cn.execute(
      text("""
        INSERT INTO Tipo_Cotizacion (Id, Nombre)
        VALUES (:id, :nombre)
      """),
      {
        "id": int(fila["id"]),
        "nombre": fila["nombre"],
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Tipo_Cotizacion",
        ["Id", "Nombre"],
        [fila["id"], fila["nombre"]],
      )
    )

  guardar_sql("tipos_cotizacion.sql", sentencias)


def migrar_productos(cn) -> None:
  """Migra productos desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("productos.csv"):
    cn.execute(
      text("""
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
      """),
      {
        "id": int(fila["id"]),
        "nombre": fila["nombre"],
        "descripcion": fila["descripcion"],
        "precio": float(fila["precio_valor"]),
        "id_moneda": int(fila["moneda_id"]),
        "id_categoria": int(fila["categoria_id"]),
        "id_proveedor": int(fila["proveedor_id"]),
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Producto",
        [
          "Id",
          "Nombre",
          "Descripcion",
          "Precio",
          "Id_Moneda",
          "Id_Categoria",
          "Id_Proveedor",
        ],
        [
          fila["id"],
          fila["nombre"],
          fila["descripcion"],
          fila["precio_valor"],
          fila["moneda_id"],
          fila["categoria_id"],
          fila["proveedor_id"],
        ],
      )
    )

  guardar_sql("productos.sql", sentencias)


def migrar_precio_historico(cn) -> None:
  """Migra precios históricos usando los precios del Sprint 1."""
  sentencias = []

  for fila in leer_csv("productos.csv"):
    cn.execute(
      text("""
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
      """),
      {
        "id_precio": int(fila["id"]),
        "id_producto": int(fila["id"]),
        "valor": float(fila["precio_valor"]),
        "fecha": fila["precio_fecha"],
        "id_moneda": int(fila["moneda_id"]),
      },
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
        [
          fila["id"],
          fila["id"],
          fila["precio_valor"],
          fila["precio_fecha"],
          fila["moneda_id"],
        ],
      )
    )

  guardar_sql("precio_historico.sql", sentencias)


def migrar_stock(cn) -> None:
  """Migra stock desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("stock.csv"):
    cn.execute(
      text("""
        INSERT INTO Stock (Id_Producto, Cantidad)
        VALUES (:id_producto, :cantidad)
      """),
      {
        "id_producto": int(fila["producto_id"]),
        "cantidad": int(fila["cantidad"]),
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Stock",
        ["Id_Producto", "Cantidad"],
        [fila["producto_id"], fila["cantidad"]],
      )
    )

  guardar_sql("stock.sql", sentencias)


def migrar_cotizaciones(cn) -> None:
  """Migra cotizaciones del dólar desde CSV hacia SQLite."""
  sentencias = []

  for fila in leer_csv("cotizaciones.csv"):
    cn.execute(
      text("""
        INSERT INTO Cotizacion_Dolar
        (
          Valor,
          Fecha,
          Id_Tipo_Cotizacion
        )
        VALUES
        (
          :valor,
          :fecha,
          :id_tipo
        )
      """),
      {
        "valor": float(fila["valor"]),
        "fecha": fila["fecha"],
        "id_tipo": int(fila["tipo_id"]),
      },
    )

    sentencias.append(
      generar_insert_sql(
        "Cotizacion_Dolar",
        ["Valor", "Fecha", "Id_Tipo_Cotizacion"],
        [fila["valor"], fila["fecha"], fila["tipo_id"]],
      )
    )

  guardar_sql("cotizaciones.sql", sentencias)


def migrar_datos() -> None:
  """Ejecuta la migración completa desde CSV hacia SQLite."""
  with ConexionDB() as cn:
    migrar_tipos_cotizacion(cn)
    migrar_categorias(cn)
    migrar_monedas(cn)
    migrar_proveedores(cn)
    migrar_productos(cn)
    migrar_precio_historico(cn)
    migrar_stock(cn)
    migrar_cotizaciones(cn)

  print("Migración finalizada correctamente.")
