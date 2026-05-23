
import datetime


class EntidadBase:
  def __init__(self, id: int):
    self.id = id


class Categoria(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre


class Proveedor(EntidadBase):
  def __init__(self, id: int, nombre: str, contacto: str):
    super().__init__(id)
    self.nombre = nombre
    self.contacto = contacto


class Moneda(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre


class TipoCotizacion(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre


class Precio:
  def __init__(
    self,
    valor: float,
    moneda: Moneda,
    fecha: datetime.date,
  ):
    if valor < 0:
      raise ValueError("El precio no puede ser negativo.")

    self.valor = valor
    self.moneda = moneda
    self.fecha = fecha


class Producto(EntidadBase):
  def __init__(
    self,
    id: int,
    nombre: str,
    descripcion: str,
    precio: Precio,
    categoria: Categoria,
    proveedor: Proveedor,
  ):
    super().__init__(id)
    self.nombre = nombre
    self.descripcion = descripcion
    self.precio = precio
    self.categoria = categoria
    self.proveedor = proveedor


class Stock:
  def __init__(self, producto: Producto, cantidad: int):
    if cantidad < 0:
      raise ValueError("El stock no puede ser negativo.")

    self.producto = producto
    self.cantidad = cantidad


class CotizacionDolar:
  def __init__(
    self,
    valor: float,
    fecha: datetime.date,
    tipo: TipoCotizacion,
  ):
    if valor <= 0:
      raise ValueError("La cotización debe ser positiva.")

    self.valor = valor
    self.fecha = fecha
    self.tipo = tipo
