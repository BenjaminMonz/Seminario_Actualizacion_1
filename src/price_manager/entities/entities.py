
# Importaciones necesarias para el funcionamiento del módulo
from __future__ import annotations
import datetime

# Definicion de clases

# Clase Categoria: Representa una categoría de productos
class Categoria():

  def __init__(self, id: int, nombre: str):
    self.id = id
    self.nombre = nombre

  def __str__(self):
    return (f"ID: {self.id} - Nombre: {self.nombre}")

# Clase Proveedor: Representa un proveedor de productos
class Proveedor():

  def __init__(self, id: int, nombre: str, contacto: str):
    self.id = id
    self.nombre = nombre
    self.contacto = contacto

  def __str__(self):
    return (f"ID: {self.id} - Nombre: {self.nombre} - Contacto {self.contacto}")
# Clase Moneda: Representa un tipo de moneda
class Moneda():

  def __init__(self, id: int, nombre: str):
      self.id = id

      # Validacion de cantidad de caracteres
      if len(nombre) != 3 or not nombre.isalpha():
        raise ValueError("La moneda debe contener exactamente 3 letras.")

      self.nombre = nombre

  def __str__(self):
    return (f"ID: {self.id} - Nombre: {self.nombre}")

# Clase TipoCotizacion: Representa el tipo de cotización del dólar
class TipoCotizacion():

  def __init__(self, id: int, nombre: str):
    self.id = id
    self.nombre = nombre

  def __str__(self):
    return (f"ID: {self.id} - Nombre: {self.nombre}")

# Clase Precio: Representa el precio de un producto. Incluye validación para evitar valores negativos
class Precio:

  def __init__(
    self,
    valor: float,
    moneda: Moneda,
    fecha: datetime.date
  ):
    # Validación de precio
    if valor < 0:
      raise ValueError("El precio del producto no puede ser negativo")

    self.valor = valor
    self.moneda = moneda
    self.fecha = fecha

  def __str__(self):
    return f"Valor: {self.valor} - Moneda: {self.moneda.nombre} - Fecha: {self.fecha}"

# Clase CotizacionDolar: Representa la cotización del dolar en una fecha y para un tipo de cambio específico
class CotizacionDolar:

  def __init__(
    self,
    valor: float,
    fecha: datetime.date,
    tipo: TipoCotizacion
  ):
    # Validación de cotización
    if valor <= 0:
      raise ValueError("La cotización debe ser positiva")

    self.valor = valor
    self.fecha = fecha
    self.tipo = tipo

  def __str__(self):
    return f"Tipo: {self.tipo.nombre} - Valor: {self.valor} - Fecha: {self.fecha}"

# Clase Producto: Representa un producto del sistema. Se considera la entidad central del negocio
class Producto():

  def __init__(
    self,
    id: int,
    nombre: str,
    descripcion: str,
    precio: Precio,
    categoria: Categoria,
    proveedor: Proveedor
  ):
    self.id = id
    # Atributos principales
    self.nombre = nombre
    self.descripcion = descripcion

    # Relaciones con otras entidades
    self.precio = precio
    self.categoria = categoria
    self.proveedor = proveedor

  def __str__(self):
    return (
        f"ID: {self.id} - {self.nombre}\n"
        f"Descripcion: {self.descripcion}\n"
        f"Precio: {self.precio}\n"
        f"Categoría: {self.categoria.nombre}\n"
        f"Proveedor: {self.proveedor.nombre}\n"
    )

# Clase Stock: Representa el stock con el que se cuenta de un producto. Se realiza validación para evitar numeros negativos
class Stock:

  def __init__(self, producto: Producto, cantidad: int):
    # Validación de stock
    if cantidad < 0:
      raise ValueError("El stock no puede ser negativo")

    self.producto = producto
    self.cantidad = cantidad

  def __str__(self):
    return f"Producto: {self.producto.nombre} | Stock: {self.cantidad}"
