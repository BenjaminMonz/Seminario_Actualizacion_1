import csv
import os


class StarComputacionPipeline:
  """Guarda los productos scrapeados en un archivo CSV."""

  def open_spider(self, spider):
    self.items = []
    self.ruta_salida = getattr(
      spider,
      "archivo_salida",
      "/content/price_manager/exports/star_computacion.csv",
    )

  def process_item(self, item, spider):
    self.items.append(dict(item))
    return item

  def close_spider(self, spider):
    os.makedirs(
      os.path.dirname(self.ruta_salida),
      exist_ok=True,
    )

    columnas = [
      "producto_interno_id",
      "producto_interno",
      "precio_interno",
      "moneda_interna",
      "busqueda",
      "titulo_web",
      "precio_web",
      "url_producto",
      "url_imagen",
      "formas_pago",
      "descripcion_detallada",
      "fecha_extraccion",
    ]

    with open(
      self.ruta_salida,
      mode="w",
      newline="",
      encoding="utf-8",
    ) as archivo:
      writer = csv.DictWriter(archivo, fieldnames=columnas)
      writer.writeheader()
      writer.writerows(self.items)
