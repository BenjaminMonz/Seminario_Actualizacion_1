
import datetime
from typing import List, Optional

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  Moneda,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)
from price_manager.repositories.repositories import (
  RepositorioCategoria,
  RepositorioCotizacionDolar,
  RepositorioMoneda,
  RepositorioProducto,
  RepositorioProveedor,
  RepositorioStock,
  RepositorioTipoCotizacion,
)


class ServicioBase:
  """Servicio base para operaciones CRUD comunes."""

  def __init__(self, repositorio):
    self.repositorio = repositorio

  def crear(self, entidad):
    return self.repositorio.crear(entidad)

  def obtener(self, id: int):
    entidad = self.repositorio.leer_por_id(id)

    if entidad is None:
      raise ValueError("No existe una entidad con ese ID.")

    return entidad

  def listar_todos(self) -> List:
    return self.repositorio.leer_todos()

  def actualizar(self, entidad):
    return self.repositorio.actualizar(entidad)

  def eliminar(self, id: int) -> bool:
    eliminado = self.repositorio.eliminar(id)

    if not eliminado:
      raise ValueError("No existe una entidad con ese ID.")

    return True


class ServicioCategoria(ServicioBase):
  """Servicio para la gestión de categorías."""

  def __init__(self, repositorio: RepositorioCategoria):
    super().__init__(repositorio)


class ServicioProveedor(ServicioBase):
  """Servicio para la gestión de proveedores."""

  def __init__(self, repositorio: RepositorioProveedor):
    super().__init__(repositorio)


class ServicioMoneda(ServicioBase):
  """Servicio para la gestión de monedas."""

  def __init__(self, repositorio: RepositorioMoneda):
    super().__init__(repositorio)


class ServicioTipoCotizacion(ServicioBase):
  """Servicio para la gestión de tipos de cotización."""

  def __init__(self, repositorio: RepositorioTipoCotizacion):
    super().__init__(repositorio)


class ServicioProducto(ServicioBase):
  """Servicio para la gestión de productos."""

  def __init__(
    self,
    repositorio: RepositorioProducto,
    categoria_servicio: ServicioCategoria,
    proveedor_servicio: ServicioProveedor,
  ):
    super().__init__(repositorio)
    self.categoria_servicio = categoria_servicio
    self.proveedor_servicio = proveedor_servicio

  def crear(self, producto: Producto) -> Producto:
    self.categoria_servicio.obtener(producto.categoria.id)
    self.proveedor_servicio.obtener(producto.proveedor.id)

    return self.repositorio.crear(producto)

  def actualizar(self, producto: Producto) -> Producto:
    self.categoria_servicio.obtener(producto.categoria.id)
    self.proveedor_servicio.obtener(producto.proveedor.id)

    return self.repositorio.actualizar(producto)


class ServicioStock:
  """Servicio para la gestión del stock de productos."""

  def __init__(
    self,
    repositorio: RepositorioStock,
    producto_servicio: ServicioProducto,
  ):
    self.repositorio = repositorio
    self.producto_servicio = producto_servicio

  def crear(self, stock: Stock) -> Stock:
    self.producto_servicio.obtener(stock.producto.id)

    if stock.cantidad < 0:
      raise ValueError("La cantidad de stock no puede ser negativa.")

    return self.repositorio.crear(stock)

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    return self.repositorio.leer_por_producto(producto_id)

  def actualizar(self, stock: Stock) -> Stock:
    self.producto_servicio.obtener(stock.producto.id)

    if stock.cantidad < 0:
      raise ValueError("La cantidad de stock no puede ser negativa.")

    return self.repositorio.actualizar(stock)

  def eliminar(self, producto_id: int) -> bool:
    eliminado = self.repositorio.eliminar(producto_id)

    if not eliminado:
      raise ValueError("No existe stock para ese producto.")

    return True

  def obtener_stock(self, producto_id: int) -> int:
    self.producto_servicio.obtener(producto_id)
    stock = self.repositorio.leer_por_producto(producto_id)

    if stock is None:
      return 0

    return stock.cantidad

  def registrar_movimiento(
    self,
    producto_id: int,
    cantidad: int,
  ) -> int:
    producto = self.producto_servicio.obtener(producto_id)
    stock_actual = self.repositorio.leer_por_producto(producto_id)

    if stock_actual is None:
      nuevo_stock = cantidad
    else:
      nuevo_stock = stock_actual.cantidad + cantidad

    if nuevo_stock < 0:
      raise ValueError("No se permite stock negativo.")

    stock = Stock(producto=producto, cantidad=nuevo_stock)

    if stock_actual is None:
      self.repositorio.crear(stock)
    else:
      self.repositorio.actualizar(stock)

    return nuevo_stock


class ServicioCotizacionDolar:
  """Servicio para la gestión de cotizaciones del dólar."""

  def __init__(
    self,
    repositorio: RepositorioCotizacionDolar,
    tipo_servicio: ServicioTipoCotizacion,
  ):
    self.repositorio = repositorio
    self.tipo_servicio = tipo_servicio

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    self.tipo_servicio.obtener(cotizacion.tipo.id)

    if cotizacion.valor <= 0:
      raise ValueError("La cotización debe ser positiva.")

    return self.repositorio.crear(cotizacion)

  def registrar_cotizacion(
    self,
    cotizacion: CotizacionDolar,
  ) -> CotizacionDolar:
    return self.crear(cotizacion)

  def obtener(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> CotizacionDolar:
    cotizacion = self.repositorio.leer_por_tipo_y_fecha(tipo_id, fecha)

    if cotizacion is None:
      raise ValueError("No existe cotización para ese tipo y fecha.")

    return cotizacion

  def leer(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    return self.repositorio.leer_por_tipo_y_fecha(tipo_id, fecha)

  def obtener_historico(
    self,
    tipo_id: int,
  ) -> List[CotizacionDolar]:
    self.tipo_servicio.obtener(tipo_id)
    return self.repositorio.leer_historico_por_tipo(tipo_id)

  def leer_historico(
    self,
    tipo_id: int,
  ) -> List[CotizacionDolar]:
    return self.obtener_historico(tipo_id)

  def actualizar(
    self,
    cotizacion: CotizacionDolar,
  ) -> CotizacionDolar:
    self.tipo_servicio.obtener(cotizacion.tipo.id)

    if cotizacion.valor <= 0:
      raise ValueError("La cotización debe ser positiva.")

    return self.repositorio.actualizar(cotizacion)

  def eliminar(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> bool:
    eliminado = self.repositorio.eliminar(tipo_id, fecha)

    if not eliminado:
      raise ValueError("No existe cotización para ese tipo y fecha.")

    return True
