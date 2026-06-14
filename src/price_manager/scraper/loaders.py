import re

from itemloaders.processors import Identity, Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def limpiar_texto(valor: str) -> str:
  """Limpia espacios innecesarios de un texto."""
  return " ".join(valor.split())


def convertir_precio(valor: str) -> float | None:
  """Convierte un precio textual a número decimal."""
  if valor is None:
    return None

  texto = re.sub(r"[^0-9,\.]", "", valor)

  if texto == "":
    return None

  texto = texto.replace(".", "").replace(",", ".")

  try:
    return float(texto)
  except ValueError:
    return None


class StarComputacionLoader(ItemLoader):
  """Normaliza los datos extraídos por el spider."""

  default_output_processor = TakeFirst()

  producto_interno_id_in = Identity()
  precio_interno_in = Identity()
  precio_web_in = MapCompose(limpiar_texto, convertir_precio)

  producto_interno_in = MapCompose(limpiar_texto)
  moneda_interna_in = MapCompose(limpiar_texto)
  busqueda_in = MapCompose(limpiar_texto)
  titulo_web_in = MapCompose(limpiar_texto)
  url_producto_in = MapCompose(limpiar_texto)
  url_imagen_in = MapCompose(limpiar_texto)
  fecha_extraccion_in = MapCompose(limpiar_texto)

  formas_pago_in = MapCompose(limpiar_texto)
  formas_pago_out = Join(" | ")

  descripcion_detallada_in = MapCompose(limpiar_texto)
  descripcion_detallada_out = Join(" ")
