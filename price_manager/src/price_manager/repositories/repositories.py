
import abc
import csv
import datetime
import os
from typing import Generic, List, Optional, TypeVar

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  EntidadBase,
  Moneda,
  Precio,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)


T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
  """Define las operaciones CRUD básicas para entidades con ID."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    pass


class RepositorioCsvBase(IRepositorio[T]):
  """Implementa operaciones CRUD comunes usando archivos CSV."""

  ruta_base = "/content/price_manager/src/price_manager/migrations/csv"

  def __init__(self, archivo: str, campos: List[str]):
    self.archivo = os.path.join(self.ruta_base, archivo)
    self.campos = campos
    os.makedirs(self.ruta_base, exist_ok=True)

  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    except FileNotFoundError:
      return []

  def grabar_archivo(self, registros: List[dict]) -> None:
    with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=self.campos)
      writer.writeheader()
      writer.writerows(registros)

  @abc.abstractmethod
  def convertir_a_dict(self, entidad: T) -> dict:
    pass

  @abc.abstractmethod
  def convertir_a_entidad(self, registro: dict) -> T:
    pass

  def crear(self, entidad: T) -> T:
    registros = self.leer_archivo()

    for registro in registros:
      if int(registro["id"]) == entidad.id:
        raise ValueError("Ya existe una entidad con ese ID.")

    registros.append(self.convertir_a_dict(entidad))
    self.grabar_archivo(registros)

    return entidad

  def leer_por_id(self, id: int) -> Optional[T]:
    registros = self.leer_archivo()

    for registro in registros:
      if int(registro["id"]) == id:
        return self.convertir_a_entidad(registro)

    return None

  def leer_todos(self) -> List[T]:
    return [
      self.convertir_a_entidad(registro)
      for registro in self.leer_archivo()
    ]

  def actualizar(self, entidad: T) -> T:
    registros = self.leer_archivo()
    encontrado = False

    for indice, registro in enumerate(registros):
      if int(registro["id"]) == entidad.id:
        registros[indice] = self.convertir_a_dict(entidad)
        encontrado = True
        break

    if not encontrado:
      raise ValueError("No existe una entidad con ese ID.")

    self.grabar_archivo(registros)

    return entidad

  def eliminar(self, id: int) -> bool:
    registros = self.leer_archivo()
    filtrados = [
      registro for registro in registros
      if int(registro["id"]) != id
    ]

    if len(registros) == len(filtrados):
      return False

    self.grabar_archivo(filtrados)

    return True


class RepositorioCategoria(RepositorioCsvBase[Categoria]):
  """Repositorio CSV para categorías."""

  def __init__(self):
    super().__init__("categorias.csv", ["id", "nombre"])

  def convertir_a_dict(self, categoria: Categoria) -> dict:
    return {
      "id": categoria.id,
      "nombre": categoria.nombre,
    }

  def convertir_a_entidad(self, registro: dict) -> Categoria:
    return Categoria(
      id=int(registro["id"]),
      nombre=registro["nombre"],
    )


class RepositorioProveedor(RepositorioCsvBase[Proveedor]):
  """Repositorio CSV para proveedores."""

  def __init__(self):
    super().__init__("proveedores.csv", ["id", "nombre", "contacto"])

  def convertir_a_dict(self, proveedor: Proveedor) -> dict:
    return {
      "id": proveedor.id,
      "nombre": proveedor.nombre,
      "contacto": proveedor.contacto,
    }

  def convertir_a_entidad(self, registro: dict) -> Proveedor:
    return Proveedor(
      id=int(registro["id"]),
      nombre=registro["nombre"],
      contacto=registro["contacto"],
    )


class RepositorioMoneda(RepositorioCsvBase[Moneda]):
  """Repositorio CSV para monedas."""

  def __init__(self):
    super().__init__("monedas.csv", ["id", "nombre"])

  def convertir_a_dict(self, moneda: Moneda) -> dict:
    return {
      "id": moneda.id,
      "nombre": moneda.nombre,
    }

  def convertir_a_entidad(self, registro: dict) -> Moneda:
    return Moneda(
      id=int(registro["id"]),
      nombre=registro["nombre"],
    )


class RepositorioTipoCotizacion(
  RepositorioCsvBase[TipoCotizacion]
):
  """Repositorio CSV para tipos de cotización."""

  def __init__(self):
    super().__init__("tipos_cotizacion.csv", ["id", "nombre"])

  def convertir_a_dict(self, tipo: TipoCotizacion) -> dict:
    return {
      "id": tipo.id,
      "nombre": tipo.nombre,
    }

  def convertir_a_entidad(self, registro: dict) -> TipoCotizacion:
    return TipoCotizacion(
      id=int(registro["id"]),
      nombre=registro["nombre"],
    )


class RepositorioProducto(RepositorioCsvBase[Producto]):
  """Repositorio CSV para productos."""

  def __init__(self):
    super().__init__(
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
    )

  def convertir_a_dict(self, producto: Producto) -> dict:
    return {
      "id": producto.id,
      "nombre": producto.nombre,
      "descripcion": producto.descripcion,
      "precio_valor": producto.precio.valor,
      "moneda_id": producto.precio.moneda.id,
      "moneda_nombre": producto.precio.moneda.nombre,
      "precio_fecha": producto.precio.fecha.isoformat(),
      "categoria_id": producto.categoria.id,
      "categoria_nombre": producto.categoria.nombre,
      "proveedor_id": producto.proveedor.id,
      "proveedor_nombre": producto.proveedor.nombre,
      "proveedor_contacto": producto.proveedor.contacto,
    }

  def convertir_a_entidad(self, registro: dict) -> Producto:
    moneda = Moneda(
      id=int(registro["moneda_id"]),
      nombre=registro["moneda_nombre"],
    )

    precio = Precio(
      valor=float(registro["precio_valor"]),
      moneda=moneda,
      fecha=datetime.date.fromisoformat(registro["precio_fecha"]),
    )

    categoria = Categoria(
      id=int(registro["categoria_id"]),
      nombre=registro["categoria_nombre"],
    )

    proveedor = Proveedor(
      id=int(registro["proveedor_id"]),
      nombre=registro["proveedor_nombre"],
      contacto=registro["proveedor_contacto"],
    )

    return Producto(
      id=int(registro["id"]),
      nombre=registro["nombre"],
      descripcion=registro["descripcion"],
      precio=precio,
      categoria=categoria,
      proveedor=proveedor,
    )


class RepositorioStock:
  """Repositorio CSV para stock."""

  ruta_base = "/content/price_manager/src/price_manager/migrations/csv"

  def __init__(self):
    self.archivo = os.path.join(self.ruta_base, "stock.csv")
    self.campos = [
      "producto_id",
      "producto_nombre",
      "producto_descripcion",
      "cantidad",
    ]
    os.makedirs(self.ruta_base, exist_ok=True)

  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    except FileNotFoundError:
      return []

  def grabar_archivo(self, registros: List[dict]) -> None:
    with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=self.campos)
      writer.writeheader()
      writer.writerows(registros)

  def convertir_a_dict(self, stock: Stock) -> dict:
    return {
      "producto_id": stock.producto.id,
      "producto_nombre": stock.producto.nombre,
      "producto_descripcion": stock.producto.descripcion,
      "cantidad": stock.cantidad,
    }

  def convertir_a_entidad(self, registro: dict) -> Stock:
    producto = Producto(
      id=int(registro["producto_id"]),
      nombre=registro["producto_nombre"],
      descripcion=registro["producto_descripcion"],
      precio=None,
      categoria=None,
      proveedor=None,
    )

    return Stock(
      producto=producto,
      cantidad=int(registro["cantidad"]),
    )

  def crear(self, stock: Stock) -> Stock:
    registros = self.leer_archivo()

    for registro in registros:
      if int(registro["producto_id"]) == stock.producto.id:
        raise ValueError("Ya existe stock para ese producto.")

    registros.append(self.convertir_a_dict(stock))
    self.grabar_archivo(registros)

    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    registros = self.leer_archivo()

    for registro in registros:
      if int(registro["producto_id"]) == producto_id:
        return self.convertir_a_entidad(registro)

    return None

  def actualizar(self, stock: Stock) -> Stock:
    registros = self.leer_archivo()
    encontrado = False

    for indice, registro in enumerate(registros):
      if int(registro["producto_id"]) == stock.producto.id:
        registros[indice] = self.convertir_a_dict(stock)
        encontrado = True
        break

    if not encontrado:
      raise ValueError("No existe stock para ese producto.")

    self.grabar_archivo(registros)

    return stock

  def eliminar(self, producto_id: int) -> bool:
    registros = self.leer_archivo()
    filtrados = [
      registro for registro in registros
      if int(registro["producto_id"]) != producto_id
    ]

    if len(registros) == len(filtrados):
      return False

    self.grabar_archivo(filtrados)

    return True


class RepositorioCotizacionDolar:
  """Repositorio CSV para cotizaciones del dólar."""

  ruta_base = "/content/price_manager/src/price_manager/migrations/csv"

  def __init__(self):
    self.archivo = os.path.join(self.ruta_base, "cotizaciones.csv")
    self.campos = ["valor", "fecha", "tipo_id", "tipo_nombre"]
    os.makedirs(self.ruta_base, exist_ok=True)

  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
    except FileNotFoundError:
      return []

  def grabar_archivo(self, registros: List[dict]) -> None:
    with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=self.campos)
      writer.writeheader()
      writer.writerows(registros)

  def convertir_a_dict(self, cotizacion: CotizacionDolar) -> dict:
    return {
      "valor": cotizacion.valor,
      "fecha": cotizacion.fecha.isoformat(),
      "tipo_id": cotizacion.tipo.id,
      "tipo_nombre": cotizacion.tipo.nombre,
    }

  def convertir_a_entidad(self, registro: dict) -> CotizacionDolar:
    tipo = TipoCotizacion(
      id=int(registro["tipo_id"]),
      nombre=registro["tipo_nombre"],
    )

    return CotizacionDolar(
      valor=float(registro["valor"]),
      fecha=datetime.date.fromisoformat(registro["fecha"]),
      tipo=tipo,
    )

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    registros = self.leer_archivo()

    for registro in registros:
      misma_fecha = registro["fecha"] == cotizacion.fecha.isoformat()
      mismo_tipo = int(registro["tipo_id"]) == cotizacion.tipo.id

      if misma_fecha and mismo_tipo:
        raise ValueError(
          "Ya existe una cotización para ese tipo y fecha."
        )

    registros.append(self.convertir_a_dict(cotizacion))
    self.grabar_archivo(registros)

    return cotizacion

  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date,
  ) -> Optional[CotizacionDolar]:
    registros = self.leer_archivo()

    for registro in registros:
      misma_fecha = registro["fecha"] == fecha.isoformat()
      mismo_tipo = int(registro["tipo_id"]) == tipo_id

      if misma_fecha and mismo_tipo:
        return self.convertir_a_entidad(registro)

    return None

  def leer_historico_por_tipo(
    self,
    tipo_id: int,
  ) -> List[CotizacionDolar]:
    return [
      self.convertir_a_entidad(registro)
      for registro in self.leer_archivo()
      if int(registro["tipo_id"]) == tipo_id
    ]

  def actualizar(
    self,
    cotizacion: CotizacionDolar,
  ) -> CotizacionDolar:
    registros = self.leer_archivo()
    encontrado = False

    for indice, registro in enumerate(registros):
      misma_fecha = registro["fecha"] == cotizacion.fecha.isoformat()
      mismo_tipo = int(registro["tipo_id"]) == cotizacion.tipo.id

      if misma_fecha and mismo_tipo:
        registros[indice] = self.convertir_a_dict(cotizacion)
        encontrado = True
        break

    if not encontrado:
      raise ValueError(
        "No existe cotización para ese tipo y fecha."
      )

    self.grabar_archivo(registros)

    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    registros = self.leer_archivo()

    filtrados = [
      registro for registro in registros
      if not (
        int(registro["tipo_id"]) == tipo_id
        and registro["fecha"] == fecha.isoformat()
      )
    ]

    if len(registros) == len(filtrados):
      return False

    self.grabar_archivo(filtrados)

    return True
