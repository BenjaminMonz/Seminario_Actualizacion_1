import scrapy


class StarComputacionItem(scrapy.Item):
  """Representa un producto obtenido desde Star Computación."""

  producto_interno_id = scrapy.Field()
  producto_interno = scrapy.Field()
  precio_interno = scrapy.Field()
  moneda_interna = scrapy.Field()
  busqueda = scrapy.Field()
  titulo_web = scrapy.Field()
  precio_web = scrapy.Field()
  url_producto = scrapy.Field()
  url_imagen = scrapy.Field()
  formas_pago = scrapy.Field()
  descripcion_detallada = scrapy.Field()
  fecha_extraccion = scrapy.Field()
