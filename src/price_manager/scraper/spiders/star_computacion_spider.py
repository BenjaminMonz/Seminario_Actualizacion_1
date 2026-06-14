import datetime
import urllib.parse

import scrapy

from price_manager.repositories.repositories import RepositorioProducto
from price_manager.scraper.items import StarComputacionItem
from price_manager.scraper.loaders import StarComputacionLoader


class StarComputacionSpider(scrapy.Spider):
  """Spider para buscar productos propios en Star Computación."""

  name = "star_computacion"
  allowed_domains = ["starcomputacion.com.ar"]
  base_url = "https://www.starcomputacion.com.ar"

  def __init__(
    self,
    limite: str = "10",
    resultados_por_busqueda: str = "10",
    archivo_salida: str = (
      "/content/price_manager/exports/star_computacion.csv"
    ),
    *args,
    **kwargs,
  ):
    super().__init__(*args, **kwargs)
    self.limite = int(limite)
    self.resultados_por_busqueda = int(resultados_por_busqueda)
    self.archivo_salida = archivo_salida

  async def start(self):
    """Genera las solicitudes iniciales en versiones nuevas de Scrapy."""
    for request in self._generar_requests_iniciales():
      yield request

  def start_requests(self):
    """Genera las solicitudes iniciales en versiones previas de Scrapy."""
    yield from self._generar_requests_iniciales()

  def _generar_requests_iniciales(self):
    """Genera búsquedas a partir de los productos internos."""
    productos = RepositorioProducto().leer_todos()[:self.limite]

    self.logger.info(
      "FLAG productos internos encontrados: %s",
      len(productos),
    )

    for producto in productos:
      busqueda = urllib.parse.quote(producto.nombre)
      url = f"{self.base_url}/prods/search/?search={busqueda}"

      self.logger.info(
        "FLAG buscando producto interno: %s",
        producto.nombre,
      )

      yield scrapy.Request(
        url=url,
        callback=self.parse_busqueda,
        errback=self.parse_error,
        meta={
          "producto": producto,
          "busqueda": producto.nombre,
        },
        dont_filter=True,
      )

  def parse_error(self, failure):
    """Registra productos que no pudieron consultarse."""
    request = failure.request
    producto = request.meta["producto"]

    self.logger.info(
      "FLAG error o bloqueo en URL: %s",
      request.url,
    )

    yield self._crear_item_bloqueado(
      producto,
      request.meta["busqueda"],
      request.url,
      "Error de conexión o bloqueo del sitio",
    )

  def parse_busqueda(self, response):
    """Procesa los primeros resultados encontrados para una búsqueda."""
    producto = response.meta["producto"]
    busqueda = response.meta["busqueda"]

    self.logger.info(
      "FLAG respuesta de búsqueda %s: status %s",
      busqueda,
      response.status,
    )

    if response.status == 403:
      yield self._crear_item_bloqueado(
        producto,
        busqueda,
        response.url,
        "Acceso bloqueado por el sitio",
      )
      return

    # Extraemos únicamente fichas reales de producto
    enlaces = response.css(".product::attr(href)").getall()

    enlaces_limpios = []

    for enlace in enlaces:
      if not enlace:
        continue

      url = response.urljoin(enlace)

      if url not in enlaces_limpios:
        enlaces_limpios.append(url)

    self.logger.info(
      "FLAG enlaces útiles encontrados para %s: %s",
      busqueda,
      len(enlaces_limpios),
    )

    if len(enlaces_limpios) == 0:
      yield self._crear_item_bloqueado(
        producto,
        busqueda,
        response.url,
        "No se encontraron productos útiles para la búsqueda",
      )
      return

    for url_producto in enlaces_limpios[:self.resultados_por_busqueda]:
      yield scrapy.Request(
        url=url_producto,
        callback=self.parse_producto,
        errback=self.parse_error,
        meta={
          "producto": producto,
          "busqueda": busqueda,
        },
        dont_filter=True,
      )

  def parse_producto(self, response):
    """Extrae los datos de detalle de un producto web."""
    producto = response.meta["producto"]
    busqueda = response.meta["busqueda"]

    self.logger.info(
      "FLAG procesando detalle: %s",
      response.url,
    )

    if response.status == 403:
      yield self._crear_item_bloqueado(
        producto,
        busqueda,
        response.url,
        "Acceso bloqueado por el sitio",
      )
      return

    loader = StarComputacionLoader(
      item=StarComputacionItem(),
      response=response,
    )

    loader.add_value("producto_interno_id", producto.id)
    loader.add_value("producto_interno", producto.nombre)
    loader.add_value("precio_interno", producto.precio.valor)
    loader.add_value("moneda_interna", producto.precio.moneda.nombre)
    loader.add_value("busqueda", busqueda)

    loader.add_css(
      "titulo_web",
      "#product_details .name::text, "
      ".product .name::text, "
      ".product_name::text, "
      ".title::text",
    )

    loader.add_css(
      "precio_web",
      ".price_regular::text, "
      ".price::text, "
      ".precio::text, "
      "[class*='price']::text, "
      "[class*='precio']::text",
    )

    loader.add_value("url_producto", response.url)

    loader.add_css(
      "url_imagen",
      "img[src*='files/products']::attr(src)",
    )

    loader.add_css(
      "formas_pago",
      ".price_td::text, "
      "[class*='pago'] *::text, "
      "[class*='cuota'] *::text",
    )

    loader.add_css(
      "descripcion_detallada",
      "#product_details *::text, "
      ".product_details *::text, "
      ".description *::text, "
      ".descripcion *::text, "
      "[class*='description'] *::text, "
      "[class*='descripcion'] *::text",
    )

    loader.add_value(
      "fecha_extraccion",
      datetime.date.today().isoformat(),
    )

    yield loader.load_item()

  def _crear_item_bloqueado(
    self,
    producto,
    busqueda: str,
    url: str,
    mensaje: str,
  ) -> StarComputacionItem:
    """Crea un item cuando el sitio no permite obtener datos."""
    item = StarComputacionItem()
    item["producto_interno_id"] = producto.id
    item["producto_interno"] = producto.nombre
    item["precio_interno"] = producto.precio.valor
    item["moneda_interna"] = producto.precio.moneda.nombre
    item["busqueda"] = busqueda
    item["titulo_web"] = mensaje
    item["precio_web"] = None
    item["url_producto"] = url
    item["url_imagen"] = None
    item["formas_pago"] = None
    item["descripcion_detallada"] = mensaje
    item["fecha_extraccion"] = datetime.date.today().isoformat()

    return item
