
# Importaciones necesarias
from __future__ import annotations

import datetime


class EntidadBase:
  """
  Clase base para las entidades del sistema.
  """

  def __init__(self, id: int):
    self.__id = id

  @property
  def id(self) -> int:
    return self.__id

  @id.setter
  def id(self, nuevo_id: int) -> None:
    self.__id = nuevo_id


class Categoria(EntidadBase):
  """
  Representa una categoría de productos.
  """

  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.__nombre = nombre

  @property
  def nombre(self) -> str:
    return self.__nombre

  @nombre.setter
  def nombre(self, nuevo_nombre: str) -> None:
    self.__nombre = nuevo_nombre


class Proveedor(EntidadBase):
  """
  Representa un proveedor del sistema.
  """

  def __init__(
    self,
    id: int,
    nombre: str,
    contacto: str
  ):
    super().__init__(id)

    self.__nombre = nombre
    self.__contacto = contacto

  @property
  def nombre(self) -> str:
    return self.__nombre

  @nombre.setter
  def nombre(self, nuevo_nombre: str) -> None:
    self.__nombre = nuevo_nombre

  @property
  def contacto(self) -> str:
    return self.__contacto

  @contacto.setter
  def contacto(self, nuevo_contacto: str) -> None:
    self.__contacto = nuevo_contacto


class Moneda(EntidadBase):
  """
  Representa una moneda del sistema.
  """

  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.__nombre = nombre

  @property
  def nombre(self) -> str:
    return self.__nombre

  @nombre.setter
  def nombre(self, nuevo_nombre: str) -> None:
    self.__nombre = nuevo_nombre


class TipoCotizacion(EntidadBase):
  """
  Representa un tipo de cotización.
  """

  def __init__(self, id: int, nombre: str):
    super().__init__(id)
    self.__nombre = nombre

  @property
  def nombre(self) -> str:
    return self.__nombre

  @nombre.setter
  def nombre(self, nuevo_nombre: str) -> None:
    self.__nombre = nuevo_nombre


class Precio:
  """
  Representa el precio de un producto.
  """

  def __init__(
    self,
    valor: float,
    moneda: Moneda,
    fecha: datetime.date
  ):

    if valor < 0:
      raise ValueError(
        "El valor del precio no puede ser negativo."
      )

    self.__valor = valor
    self.__moneda = moneda
    self.__fecha = fecha

  @property
  def valor(self) -> float:
    return self.__valor

  @valor.setter
  def valor(self, nuevo_valor: float) -> None:

    if nuevo_valor < 0:
      raise ValueError(
        "El valor del precio no puede ser negativo."
      )

    self.__valor = nuevo_valor

  @property
  def moneda(self) -> Moneda:
    return self.__moneda

  @property
  def fecha(self) -> datetime.date:
    return self.__fecha


class CotizacionDolar:
  """
  Representa una cotización del dólar.
  """

  def __init__(
    self,
    valor: float,
    fecha: datetime.date,
    tipo: TipoCotizacion
  ):

    if valor <= 0:
      raise ValueError(
        "La cotización debe ser positiva."
      )

    self.__valor = valor
    self.__fecha = fecha
    self.__tipo = tipo

  @property
  def valor(self) -> float:
    return self.__valor

  @property
  def fecha(self) -> datetime.date:
    return self.__fecha

  @property
  def tipo(self) -> TipoCotizacion:
    return self.__tipo


class Producto(EntidadBase):
  """
  Representa un producto del sistema.
  """

  def __init__(
    self,
    id: int,
    nombre: str,
    descripcion: str,
    precio: Precio,
    categoria: Categoria,
    proveedor: Proveedor
  ):

    super().__init__(id)

    self.__nombre = nombre
    self.__descripcion = descripcion
    self.__precio = precio
    self.__categoria = categoria
    self.__proveedor = proveedor

  @property
  def nombre(self) -> str:
    return self.__nombre

  @nombre.setter
  def nombre(self, nuevo_nombre: str) -> None:
    self.__nombre = nuevo_nombre

  @property
  def descripcion(self) -> str:
    return self.__descripcion

  @property
  def precio(self) -> Precio:
    return self.__precio

  @property
  def categoria(self) -> Categoria:
    return self.__categoria

  @property
  def proveedor(self) -> Proveedor:
    return self.__proveedor


class Stock:
  """
  Representa el stock de un producto.
  """

  def __init__(
    self,
    producto: Producto,
    cantidad: int
  ):

    if cantidad < 0:
      raise ValueError(
        "La cantidad de stock no puede ser negativa."
      )

    self.__producto = producto
    self.__cantidad = cantidad

  @property
  def producto(self) -> Producto:
    return self.__producto

  @property
  def cantidad(self) -> int:
    return self.__cantidad

  @cantidad.setter
  def cantidad(self, nueva_cantidad: int) -> None:

    if nueva_cantidad < 0:
      raise ValueError(
        "La cantidad de stock no puede ser negativa."
      )

    self.__cantidad = nueva_cantidad
