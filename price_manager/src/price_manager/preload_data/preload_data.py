
import csv
import os


BASE_PATH = "/content/price_manager/src/price_manager/migrations/csv"


def crear_directorio() -> None:
  """Crea el directorio donde se almacenan los archivos CSV."""
  os.makedirs(BASE_PATH, exist_ok=True)


def escribir_csv(
  nombre_archivo: str,
  campos: list[str],
  registros: list[dict],
) -> None:
  """Escribe registros en un archivo CSV."""
  ruta = os.path.join(BASE_PATH, nombre_archivo)

  with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
    writer = csv.DictWriter(archivo, fieldnames=campos)
    writer.writeheader()
    writer.writerows(registros)


def precargar_datos() -> None:
  """Genera archivos CSV iniciales con 10 registros por entidad."""
  crear_directorio()

  escribir_csv(
    "categorias.csv",
    ["id", "nombre"],
    [
      {"id": 1, "nombre": "Monitores"},
      {"id": 2, "nombre": "Teclados"},
      {"id": 3, "nombre": "Mouse"},
      {"id": 4, "nombre": "Auriculares"},
      {"id": 5, "nombre": "Notebooks"},
      {"id": 6, "nombre": "Procesadores"},
      {"id": 7, "nombre": "Placas de video"},
      {"id": 8, "nombre": "Memorias RAM"},
      {"id": 9, "nombre": "Discos SSD"},
      {"id": 10, "nombre": "Fuentes"},
    ],
  )

  escribir_csv(
    "proveedores.csv",
    ["id", "nombre", "contacto"],
    [
      {"id": 1, "nombre": "TechCorp", "contacto": "ventas@techcorp.com"},
      {"id": 2, "nombre": "HardPlus", "contacto": "info@hardplus.com"},
      {"id": 3, "nombre": "CompuMax", "contacto": "contacto@compumax.com"},
      {"id": 4, "nombre": "DigitalStore", "contacto": "ventas@digital.com"},
      {"id": 5, "nombre": "PC Mayorista", "contacto": "mayorista@pc.com"},
      {"id": 6, "nombre": "InsumosNet", "contacto": "info@insumosnet.com"},
      {"id": 7, "nombre": "TecnoWorld", "contacto": "ventas@tecnoworld.com"},
      {"id": 8, "nombre": "Hardware SA", "contacto": "contacto@hardware.com"},
      {"id": 9, "nombre": "ElectroParts", "contacto": "ventas@eparts.com"},
      {"id": 10, "nombre": "MegaTech", "contacto": "info@megatech.com"},
    ],
  )

  escribir_csv(
    "monedas.csv",
    ["id", "nombre"],
    [
      {"id": 1, "nombre": "ARS"},
      {"id": 2, "nombre": "USD"},
      {"id": 3, "nombre": "EUR"},
      {"id": 4, "nombre": "BRL"},
      {"id": 5, "nombre": "CLP"},
      {"id": 6, "nombre": "UYU"},
      {"id": 7, "nombre": "GBP"},
      {"id": 8, "nombre": "JPY"},
      {"id": 9, "nombre": "CNY"},
      {"id": 10, "nombre": "MXN"},
    ],
  )

  escribir_csv(
    "tipos_cotizacion.csv",
    ["id", "nombre"],
    [
      {"id": 1, "nombre": "Oficial"},
      {"id": 2, "nombre": "Blue"},
      {"id": 3, "nombre": "Bolsa"},
      {"id": 4, "nombre": "CCL"},
      {"id": 5, "nombre": "Cripto"},
      {"id": 6, "nombre": "Tarjeta"},
      {"id": 7, "nombre": "Mayorista"},
      {"id": 8, "nombre": "MEP"},
      {"id": 9, "nombre": "Ahorro"},
      {"id": 10, "nombre": "Turista"},
    ],
  )

  escribir_csv(
    "productos.csv",
    [
      "id",
      "nombre",
      "descripcion",
      "precio_valor",
      "moneda_id",
      "moneda_nombre",
      "precio_fecha",
      "categoria_id",
      "categoria_nombre",
      "proveedor_id",
      "proveedor_nombre",
      "proveedor_contacto",
    ],
    [
      {
        "id": 1,
        "nombre": "Monitor 24",
        "descripcion": "Monitor Full HD",
        "precio_valor": 150000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 1,
        "categoria_nombre": "Monitores",
        "proveedor_id": 1,
        "proveedor_nombre": "TechCorp",
        "proveedor_contacto": "ventas@techcorp.com",
      },
      {
        "id": 2,
        "nombre": "Teclado Mecánico",
        "descripcion": "Teclado switch blue",
        "precio_valor": 85000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 2,
        "categoria_nombre": "Teclados",
        "proveedor_id": 2,
        "proveedor_nombre": "HardPlus",
        "proveedor_contacto": "info@hardplus.com",
      },
      {
        "id": 3,
        "nombre": "Mouse Gamer",
        "descripcion": "Mouse RGB",
        "precio_valor": 45000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 3,
        "categoria_nombre": "Mouse",
        "proveedor_id": 3,
        "proveedor_nombre": "CompuMax",
        "proveedor_contacto": "contacto@compumax.com",
      },
      {
        "id": 4,
        "nombre": "Auricular USB",
        "descripcion": "Auricular con micrófono",
        "precio_valor": 60000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 4,
        "categoria_nombre": "Auriculares",
        "proveedor_id": 4,
        "proveedor_nombre": "DigitalStore",
        "proveedor_contacto": "ventas@digital.com",
      },
      {
        "id": 5,
        "nombre": "Notebook i5",
        "descripcion": "Notebook 8GB RAM",
        "precio_valor": 900,
        "moneda_id": 2,
        "moneda_nombre": "USD",
        "precio_fecha": "2026-04-01",
        "categoria_id": 5,
        "categoria_nombre": "Notebooks",
        "proveedor_id": 5,
        "proveedor_nombre": "PC Mayorista",
        "proveedor_contacto": "mayorista@pc.com",
      },
      {
        "id": 6,
        "nombre": "Ryzen 5",
        "descripcion": "Procesador AM4",
        "precio_valor": 250,
        "moneda_id": 2,
        "moneda_nombre": "USD",
        "precio_fecha": "2026-04-01",
        "categoria_id": 6,
        "categoria_nombre": "Procesadores",
        "proveedor_id": 6,
        "proveedor_nombre": "InsumosNet",
        "proveedor_contacto": "info@insumosnet.com",
      },
      {
        "id": 7,
        "nombre": "RTX 4060",
        "descripcion": "Placa de video 8GB",
        "precio_valor": 450,
        "moneda_id": 2,
        "moneda_nombre": "USD",
        "precio_fecha": "2026-04-01",
        "categoria_id": 7,
        "categoria_nombre": "Placas de video",
        "proveedor_id": 7,
        "proveedor_nombre": "TecnoWorld",
        "proveedor_contacto": "ventas@tecnoworld.com",
      },
      {
        "id": 8,
        "nombre": "RAM 16GB",
        "descripcion": "Memoria DDR4",
        "precio_valor": 70000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 8,
        "categoria_nombre": "Memorias RAM",
        "proveedor_id": 8,
        "proveedor_nombre": "Hardware SA",
        "proveedor_contacto": "contacto@hardware.com",
      },
      {
        "id": 9,
        "nombre": "SSD 1TB",
        "descripcion": "Disco NVMe",
        "precio_valor": 120000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 9,
        "categoria_nombre": "Discos SSD",
        "proveedor_id": 9,
        "proveedor_nombre": "ElectroParts",
        "proveedor_contacto": "ventas@eparts.com",
      },
      {
        "id": 10,
        "nombre": "Fuente 650W",
        "descripcion": "80 Plus Bronze",
        "precio_valor": 95000,
        "moneda_id": 1,
        "moneda_nombre": "ARS",
        "precio_fecha": "2026-04-01",
        "categoria_id": 10,
        "categoria_nombre": "Fuentes",
        "proveedor_id": 10,
        "proveedor_nombre": "MegaTech",
        "proveedor_contacto": "info@megatech.com",
      },
    ],
  )

  escribir_csv(
    "stock.csv",
    ["producto_id", "producto_nombre", "producto_descripcion", "cantidad"],
    [
      {"producto_id": 1, "producto_nombre": "Monitor 24",
       "producto_descripcion": "Monitor Full HD", "cantidad": 15},
      {"producto_id": 2, "producto_nombre": "Teclado Mecánico",
       "producto_descripcion": "Teclado switch blue", "cantidad": 20},
      {"producto_id": 3, "producto_nombre": "Mouse Gamer",
       "producto_descripcion": "Mouse RGB", "cantidad": 35},
      {"producto_id": 4, "producto_nombre": "Auricular USB",
       "producto_descripcion": "Auricular con micrófono", "cantidad": 18},
      {"producto_id": 5, "producto_nombre": "Notebook i5",
       "producto_descripcion": "Notebook 8GB RAM", "cantidad": 7},
      {"producto_id": 6, "producto_nombre": "Ryzen 5",
       "producto_descripcion": "Procesador AM4", "cantidad": 12},
      {"producto_id": 7, "producto_nombre": "RTX 4060",
       "producto_descripcion": "Placa de video 8GB", "cantidad": 5},
      {"producto_id": 8, "producto_nombre": "RAM 16GB",
       "producto_descripcion": "Memoria DDR4", "cantidad": 40},
      {"producto_id": 9, "producto_nombre": "SSD 1TB",
       "producto_descripcion": "Disco NVMe", "cantidad": 22},
      {"producto_id": 10, "producto_nombre": "Fuente 650W",
       "producto_descripcion": "80 Plus Bronze", "cantidad": 14},
    ],
  )

  escribir_csv(
    "cotizaciones.csv",
    ["valor", "fecha", "tipo_id", "tipo_nombre"],
    [
      {"valor": 980, "fecha": "2026-04-01",
       "tipo_id": 1, "tipo_nombre": "Oficial"},
      {"valor": 1020, "fecha": "2026-04-01",
       "tipo_id": 2, "tipo_nombre": "Blue"},
      {"valor": 1005, "fecha": "2026-04-02",
       "tipo_id": 3, "tipo_nombre": "Bolsa"},
      {"valor": 1015, "fecha": "2026-04-02",
       "tipo_id": 4, "tipo_nombre": "CCL"},
      {"valor": 1030, "fecha": "2026-04-03",
       "tipo_id": 5, "tipo_nombre": "Cripto"},
      {"valor": 1100, "fecha": "2026-04-03",
       "tipo_id": 6, "tipo_nombre": "Tarjeta"},
      {"valor": 975, "fecha": "2026-04-04",
       "tipo_id": 7, "tipo_nombre": "Mayorista"},
      {"valor": 1010, "fecha": "2026-04-04",
       "tipo_id": 8, "tipo_nombre": "MEP"},
      {"valor": 1080, "fecha": "2026-04-05",
       "tipo_id": 9, "tipo_nombre": "Ahorro"},
      {"valor": 1150, "fecha": "2026-04-05",
       "tipo_id": 10, "tipo_nombre": "Turista"},
    ],
  )
