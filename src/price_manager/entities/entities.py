
import datetime


class EntidadBase:
  def __init__(self, id: int):
    self.id = id


class Categoria(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre

  def __str__(self) -> str:
    return (
      f"Categoria("
      f"id={self.id}, "
      f"nombre='{self.nombre}'"
      f")"
    )


class Proveedor(EntidadBase):
  def __init__(self, id: int, nombre: str, contacto: str):
    super().__init__(id)
    self.nombre = nombre
    self.contacto = contacto

  def __str__(self) -> str:
    return (
      f"Proveedor("
      f"id={self.id}, "
      f"nombre='{self.nombre}', "
      f"contacto='{self.contacto}'"
      f")"
    )


class Moneda(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre

  def __str__(self) -> str:
    return (
      f"Moneda("
      f"id={self.id}, "
      f"nombre='{self.nombre}'"
      f")"
    )

class TipoCotizacion(EntidadBase):
  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.nombre = nombre

  def __str__(self) -> str:
    return (
      f"TipoCotizacion("
      f"id={self.id}, "
      f"nombre='{self.nombre}'"
      f")"
    )

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

  def __str__(self) -> str:
    return (
      f"Precio("
      f"valor={self.valor}, "
      f"moneda='{self.moneda.nombre}', "
      f"fecha='{self.fecha}'"
      f")"
    )

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

  def __str__(self) -> str:
    return (
      f"Producto("
      f"id={self.id}, "
      f"nombre='{self.nombre}', "
      f"precio={self.precio.valor} "
      f"{self.precio.moneda.nombre}, "
      f"categoria='{self.categoria.nombre}', "
      f"proveedor='{self.proveedor.nombre}'"
      f")"
    )

class Stock:
  def __init__(self, producto: Producto, cantidad: int):
    if cantidad < 0:
      raise ValueError("El stock no puede ser negativo.")

    self.producto = producto
    self.cantidad = cantidad


  def __str__(self) -> str:
    return (
      f"Stock("
      f"producto='{self.producto.nombre}', "
      f"cantidad={self.cantidad}"
      f")"
    )

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

  def __str__(self) -> str:
    return (
      f"CotizacionDolar("
      f"tipo='{self.tipo.nombre}', "
      f"valor={self.valor}, "
      f"fecha='{self.fecha}'"
      f")"
    )
