
import abc
from typing import TypeVar, Generic, List, Optional
from price_manager.entities.entities import (
    Categoria, Proveedor, Moneda, TipoCotizacion,
    Precio, Producto, CotizacionDolar, Stock
)
import datetime
import csv

class EntidadBase:
    pass

T = TypeVar('T', bound=EntidadBase)

class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una nueva entidad en el repositorio.

    Args:
        entidad (T): La entidad a crear.

    Returns:
        T: La entidad creada.

    Raises:
        ValueError: Si ya existe una entidad con el mismo ID.
    """
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    """Lee una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a leer.

    Returns:
        Optional[T]: La entidad si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    """Lee todas las entidades del repositorio.

    Returns:
        List[T]: Una lista de todas las entidades.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente en el repositorio.

    Args:
        entidad (T): La entidad a actualizar (debe tener un ID existente).

    Returns:
        T: La entidad actualizada.

    Raises:
        ValueError: Si no se encuentra la entidad para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    """Elimina una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a eliminar.

    Returns:
        bool: True si la entidad fue eliminada, False si no se encontró.
    """
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para repositorios del tipo Stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un nuevo registro de stock.

    Args:
        stock (Stock): El objeto Stock a crear.

    Returns:
        Stock: El objeto Stock creado.

    Raises:
        ValueError: Si ya existe un registro de stock para el mismo producto.
    """
    pass

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional['Stock']:
    """Lee un registro de stock por ID de producto.

    Args:
        producto_id (int): El ID del producto asociado al stock.

    Returns:
        Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, stock: 'Stock') -> 'Stock':
    """Actualiza un registro de stock existente.

    Args:
        stock (Stock): El objeto Stock a actualizar (debe tener un producto_id existente).

    Returns:
        Stock: El objeto Stock actualizado.

    Raises:
        ValueError: Si no se encuentra el stock para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool:
    """Elimina un registro de stock por ID de producto.

    Args:
        producto_id (int): El ID del producto asociado al stock a eliminar.

    Returns:
        bool: True si el stock fue eliminado, False si no se encontró.
    """
    pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

  @abc.abstractmethod
  def crear(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    """Crea una nueva cotización de dólar.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar creado.

    Raises:
        ValueError: Si ya existe una cotización para el mismo tipo y fecha.
    """
    pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional['CotizacionDolar']:
    """Lee una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
        fecha (datetime.date): La fecha de la cotización.

    Returns:
        Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List['CotizacionDolar']:
    """Lee el histórico de cotizaciones para un tipo específico.

    Args:
        tipo_id (int): El ID del tipo de cotización.

    Returns:
        List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    """Actualiza una cotización de dólar existente.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar actualizado.

    Raises:
        ValueError: Si no se encuentra la cotización para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización.
        fecha (datetime.date): La fecha de la cotización a eliminar.

    Returns:
        bool: True si la cotización fue eliminada, False si no se encontró.
    """
    pass

### CRUD BASICO ###
# PROVEEDOR

# Creacion de la clase repositorio para Proveedor.
class RepositorioProveedor(IRepositorio[Proveedor]):

  # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  # Creacion del constructor.
  def __init__(self, archivo="proveedores.csv"):
        self.archivo = self.ruta_base + archivo

  # Funcion genérica, devuelve lista de proveedores.
  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
    except FileNotFoundError:
      return []

  # Función genérica, graba una lista de proveedores.
  def grabar_archivo(self, proveedores:List[dict]):
     with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "contacto"])
            writer.writeheader()
            writer.writerows(proveedores)

  # Crea un proveedor.
  def crear(self, proveedor: Proveedor) -> Proveedor:

        proveedores = self.leer_archivo()

        # Validacion de existencia.
        for p in proveedores:
            if int(p["id"]) == proveedor.id:
                raise ValueError("Ya existe un proveedor con el ID ingresado.")

        # Insercion de proveedor a lista.
        proveedores.append({
            "id": proveedor.id,
            "nombre": proveedor.nombre,
            "contacto": proveedor.contacto
        })

        self.grabar_archivo(proveedores)

        return proveedor

  # Obtiene lista de proveedores buscando por ID.
  def leer_por_id(self, id:int) -> Optional[Proveedor]:

        proveedores = self.leer_archivo()

        # Busqueda de proveedor por id.
        for p in proveedores:
            if int(p["id"]) == id:
              return Proveedor(int(p['id']),p['nombre'],p['contacto'])
        return None

  # Obtiene lista de proveedores.
  def leer_todos(self) -> List[Proveedor]:
    proveedores = self.leer_archivo()

    return [
        Proveedor(
            int(p["id"]),
            p["nombre"],
            p["contacto"]
        )
        for p in proveedores
    ]

  # Actualiza lista de proveedores
  def actualizar(self, proveedor: Proveedor) -> Proveedor:
    proveedores = self.leer_archivo()
    proveedor_existente:bool = False

    for p in proveedores:
      if int(p['id']) == proveedor.id:
        proveedor_existente = True
        p['nombre'] = proveedor.nombre
        p['contacto'] = proveedor.contacto
        break

    if not proveedor_existente:
      raise ValueError("Error, no existe el proveedor ingresado.")

    self.grabar_archivo(proveedores)
    return proveedor

  # Genera nueva lista de proveedores.
  def eliminar(self, proveedor_id: int) -> bool:
    proveedores = self.leer_archivo()
    proveedores_actualizados = []

    for p in proveedores:
      if int(p['id']) != proveedor_id:
        proveedores_actualizados.append({
            'id' : p['id'],
            'nombre' : p['nombre'],
            'contacto' : p['contacto']
        })

    if len(proveedores) == len(proveedores_actualizados):
      return False

    self.grabar_archivo(proveedores_actualizados)
    return True

# ------------------------------------

# CATEGORIA
# Creacion de la clase repositorio para Categoria.
class RepositorioCategoria(IRepositorio[Categoria]):

  archivo: str
  # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  # Creacion del constructor.
  def __init__(self, archivo="categorias.csv"):
        self.archivo = self.ruta_base + archivo

  # Funcion genérica, devuelve lista de categorias.
  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
    except FileNotFoundError:
      return []

  # Función genérica, graba una lista de categorias.
  def grabar_archivo(self, categorias:List[dict]):
     with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre"])
            writer.writeheader()
            writer.writerows(categorias)

  # Crea una categoria.
  def crear(self, categoria: Categoria) -> Categoria:

        categorias = self.leer_archivo()

        # Validacion de existencia.
        for c in categorias:
            if int(c["id"]) == categoria.id:
                raise ValueError("Ya existe una categoria con el ID ingresado.")

        # Insercion de moneda a lista.
        categorias.append({
            "id": categoria.id,
            "nombre": categoria.nombre
        })

        self.grabar_archivo(categorias)

        return categoria

  # Obtiene una categoria por ID.
  def leer_por_id(self, id:int) -> Optional[Categoria]:

        categorias = self.leer_archivo()

        # Busqueda de categoria por id.
        for c in categorias:
            if int(c["id"]) == id:
              return Categoria(int(c['id']),c['nombre'])
        return None

  # Obtiene lista de categorias.
  def leer_todos(self) -> List[Categoria]:
    categorias = self.leer_archivo()

    return [
        Categoria(
            int(c["id"]),
            c["nombre"]
        )
        for c in categorias
    ]

  # Actualiza lista de categorias
  def actualizar(self, categoria: Categoria) -> Categoria:
    categorias = self.leer_archivo()
    categoria_existente:bool = False

    for c in categorias:
      if c['id'] == categoria.id:
        categoria_existente = True
        c['nombre'] = categoria.nombre
        break

    if not categoria_existente:
      raise ValueError("Error, no existe la categoria ingresada.")

    self.grabar_archivo(categorias)
    return categoria

  # Genera nueva lista de categorias.
  def eliminar(self, categoria_id: int) -> bool:
    categorias = self.leer_archivo()
    categorias_actualizadas = []

    for c in categorias:
      if int(c['id']) != categoria_id:
        categorias_actualizadas.append({
            'id' : c['id'],
            'nombre' : c['nombre'],
        })

    if len(categorias) == len(categorias_actualizadas):
      return False

    self.grabar_archivo(categorias_actualizadas)
    return True

# ----------------------------------

#TIPO COTIZACION
# Creacion de la clase repositorio para Tipo Cotizacion.
class RepositorioTipoCotizacion(IRepositorio[TipoCotizacion]):

  archivo: str
  # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  # Creacion del constructor.
  def __init__(self, archivo="tiposCotizacion.csv"):
        self.archivo = self.ruta_base + archivo

  # Funcion genérica, devuelve lista de tipos de cotizacion.
  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
    except FileNotFoundError:
      return []

  # Función genérica, graba una lista de tipos de cotizacion.
  def grabar_archivo(self, tCotizacion:List[dict]):
     with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre"])
            writer.writeheader()
            writer.writerows(tCotizacion)

  # Crea un tipo de cotizacion.
  def crear(self, tCotizacion: TipoCotizacion) -> TipoCotizacion:

        tiposCotizacion = self.leer_archivo()

        # Validacion de existencia.
        for t in tiposCotizacion:
            if int(t["id"]) == tCotizacion.id:
                raise ValueError("Ya existe un tipo de cotizacion con el ID ingresado.")

        # Insercion de moneda a lista.
        tiposCotizacion.append({
            "id": tCotizacion.id,
            "nombre": tCotizacion.nombre
        })

        self.grabar_archivo(tiposCotizacion)

        return tCotizacion

  # Obtiene un tipo de cotizacion por ID.
  def leer_por_id(self, id:int) -> Optional[TipoCotizacion]:

        tiposCotizacion = self.leer_archivo()

        # Busqueda de moneda por id.
        for t in tiposCotizacion:
            if int(t["id"]) == id:
              return TipoCotizacion(int(t['id']),t['nombre'])
        return None

  # Obtiene lista de tipos de cotizacion.
  def leer_todos(self) -> List[TipoCotizacion]:
    tiposCotizacion = self.leer_archivo()

    return [
        TipoCotizacion(
            int(t["id"]),
            t["nombre"]
        )
        for t in tiposCotizacion
    ]

  # Actualiza lista de tipos de cotizacion
  def actualizar(self, tCotizacion: TipoCotizacion) -> TipoCotizacion:
    tiposCotizacion = self.leer_archivo()
    tipoCotizacion_existente:bool = False

    for t in tiposCotizacion:
      if int(t['id']) == tCotizacion.id:
        tipoCotizacion_existente = True
        t['nombre'] = tCotizacion.nombre
        break

    if not tipoCotizacion_existente:
      raise ValueError("Error, no existe el tipo de cotizacion ingresado.")

    self.grabar_archivo(tiposCotizacion)
    return tCotizacion

  # Genera nueva lista de tipos de cotizacion.
  def eliminar(self, tCotizacion_id: int) -> bool:
    tiposCotizacion = self.leer_archivo()
    tiposCotizacion_actualizados = []

    for t in tiposCotizacion:
      if int(t['id']) != tCotizacion_id:
        tiposCotizacion_actualizados.append({
            'id' : t['id'],
            'nombre' : t['nombre'],
        })

    if len(tiposCotizacion) == len(tiposCotizacion_actualizados):
      return False

    self.grabar_archivo(tiposCotizacion_actualizados)
    return True

# -----------------------------------
# MONEDA
# Creacion de la clase repositorio para Moneda.
class RepositorioMoneda(IRepositorio[Moneda]):
  # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  # Creacion del constructor.
  def __init__(self, archivo="monedas.csv"):
        self.archivo = self.ruta_base + archivo

  # Funcion genérica, devuelve lista de monedas.
  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
    except FileNotFoundError:
      return []

  # Función genérica, graba una lista de monedas.
  def grabar_archivo(self, monedas:List[dict]):
     with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre"])
            writer.writeheader()
            writer.writerows(monedas)

  # Crea una moneda.
  def crear(self, moneda: Moneda) -> Moneda:

        monedas = self.leer_archivo()

        # Validacion de existencia.
        for m in monedas:
            if int(m["id"]) == moneda.id:
                raise ValueError("Ya existe una moneda con el ID ingresado.")

        # Insercion de moneda a lista.
        monedas.append({
            "id": moneda.id,
            "nombre": moneda.nombre
        })

        self.grabar_archivo(monedas)

        return moneda

  # Obtiene lista de monedas buscando por ID.
  def leer_por_id(self, id:int) -> Optional[Moneda]:

        monedas = self.leer_archivo()

        # Busqueda de moneda por id.
        for m in monedas:
            if int(m["id"]) == id:
              return Moneda(int(m['id']),m['nombre'])
        return None

  # Obtiene lista de monedas.
  def leer_todos(self) -> List[Moneda]:
    monedas = self.leer_archivo()

    return [
        Moneda(
            int(m["id"]),
            m["nombre"]
        )
        for m in monedas
    ]

  # Actualiza lista de monedas
  def actualizar(self, moneda: Moneda) -> Moneda:
    monedas = self.leer_archivo()
    moneda_existente:bool = False

    for m in monedas:
      if int(m['id']) == moneda.id:
        moneda_existente = True
        m['nombre'] = moneda.nombre
        break

    if not moneda_existente:
      raise ValueError("Error, no existe la moneda ingresada.")

    self.grabar_archivo(monedas)
    return moneda

  # Genera nueva lista de monedas.
  def eliminar(self, moneda_id: int) -> bool:
    monedas = self.leer_archivo()
    monedas_actualizadas = []

    for m in monedas:
      if int(m['id']) != moneda_id:
        monedas_actualizadas.append({
            'id' : m['id'],
            'nombre' : m['nombre'],
        })

    if len(monedas) == len(monedas_actualizadas):
      return False

    self.grabar_archivo(monedas_actualizadas)
    return True

# ------------------------------------
# PRODUCTO
class RepositorioProducto(IRepositorio[Producto]):
    # Ruta base en donde guardar archivos csv
    ruta_base:str="price_manager/migrations/csv/"

    archivo: str

    def __init__(self, archivo="productos.csv"):
        self.archivo = self.ruta_base + archivo

    def leer_archivo(self) -> List[dict]:
        try:
            with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []

    def grabar_archivo(self, productos: List[dict]):
        with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id", "nombre", "descripcion",
                    "precio_valor", "moneda_id", "moneda_nombre", "precio_fecha",
                    "categoria_id", "categoria_nombre",
                    "proveedor_id", "proveedor_nombre", "proveedor_contacto"
                ]
            )
            writer.writeheader()
            writer.writerows(productos)

    def crear(self, producto: Producto) -> Producto:
        productos = self.leer_archivo()

        for p in productos:
            if int(p["id"]) == producto.id:
                raise ValueError("El producto ya existe.")

        productos.append({
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
            "proveedor_contacto": producto.proveedor.contacto
        })

        self.grabar_archivo(productos)
        return producto

    def leer_por_id(self, id: int) -> Optional[Producto]:
        productos = self.leer_archivo()

        for p in productos:
            if int(p["id"]) == id:
                moneda = Moneda(
                    int(p["moneda_id"]),
                    p["moneda_nombre"]
                )

                precio = Precio(
                    float(p["precio_valor"]),
                    moneda,
                    datetime.date.fromisoformat(p["precio_fecha"])
                )

                categoria = Categoria(
                    int(p["categoria_id"]),
                    p["categoria_nombre"]
                )

                proveedor = Proveedor(
                    int(p["proveedor_id"]),
                    p["proveedor_nombre"],
                    p["proveedor_contacto"]
                )

                return Producto(
                    int(p["id"]),
                    p["nombre"],
                    p["descripcion"],
                    precio,
                    categoria,
                    proveedor
                )

        return None

    def leer_todos(self) -> List[Producto]:
        productos = self.leer_archivo()
        lista_productos = []

        for p in productos:
            moneda = Moneda(
                int(p["moneda_id"]),
                p["moneda_nombre"]
            )

            precio = Precio(
                float(p["precio_valor"]),
                moneda,
                datetime.date.fromisoformat(p["precio_fecha"])
            )

            categoria = Categoria(
                int(p["categoria_id"]),
                p["categoria_nombre"]
            )

            proveedor = Proveedor(
                int(p["proveedor_id"]),
                p["proveedor_nombre"],
                p["proveedor_contacto"]
            )

            producto = Producto(
                int(p["id"]),
                p["nombre"],
                p["descripcion"],
                precio,
                categoria,
                proveedor
            )

            lista_productos.append(producto)

        return lista_productos

    def actualizar(self, producto: Producto) -> Producto:
        productos = self.leer_archivo()
        producto_encontrado = False

        for p in productos:
            if int(p["id"]) == producto.id:
                p["nombre"] = producto.nombre
                p["descripcion"] = producto.descripcion
                p["precio_valor"] = producto.precio.valor
                p["moneda_id"] = producto.precio.moneda.id
                p["moneda_nombre"] = producto.precio.moneda.nombre
                p["precio_fecha"] = producto.precio.fecha.isoformat()
                p["categoria_id"] = producto.categoria.id
                p["categoria_nombre"] = producto.categoria.nombre
                p["proveedor_id"] = producto.proveedor.id
                p["proveedor_nombre"] = producto.proveedor.nombre
                p["proveedor_contacto"] = producto.proveedor.contacto
                producto_encontrado = True
                break

        if not producto_encontrado:
            raise ValueError("No existe un producto con ese id.")

        self.grabar_archivo(productos)
        return producto

    def eliminar(self, producto_id: int) -> bool:
        productos = self.leer_archivo()

        productos_actualizados = [
            p for p in productos
            if int(p["id"]) != producto_id
        ]

        if len(productos) == len(productos_actualizados):
            return False

        self.grabar_archivo(productos_actualizados)
        return True

# --------------------------------------------------------
### CRUD STOCK
class RepositorioStock(IRepositorioStock):

 # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  def __init__(self, archivo="stock.csv"):
    self.archivo = self.ruta_base + archivo

  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
    except FileNotFoundError:
      return []

  def grabar_archivo(self, stock: List[dict]):
    with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f,fieldnames=["id_producto", "producto_nombre",
                                            "producto_descripcion","cantidad"])
      writer.writeheader()
      writer.writerows(stock)

  def crear(self, stock: Stock) -> Stock:
    stock_ = self.leer_archivo()

    for s in stock_:
      if int(s["id_producto"]) == stock.producto.id:
        raise ValueError("Ya existe stock para el producto ingresado.")

    stock_.append({
      "id_producto": stock.producto.id,
      "producto_nombre": stock.producto.nombre,
      "producto_descripcion": stock.producto.descripcion,
      "cantidad": stock.cantidad
    })

    self.grabar_archivo(stock_)
    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    stock_ = self.leer_archivo()

    for s in stock_:
      if int(s["id_producto"]) == producto_id:

        # Producto auxiliar, suficiente para Stock.
        producto = Producto(
          int(s["id_producto"]),
          s["producto_nombre"],
          s["producto_descripcion"],
          None,
          None,
          None
        )

        return Stock(
          producto,
          int(s["cantidad"])
        )

    return None

  def actualizar(self, stock: Stock) -> Stock:
    stock_ = self.leer_archivo()
    stock_encontrado = False

    for s in stock_:
      if int(s["id_producto"]) == stock.producto.id:
        s["producto_nombre"] = stock.producto.nombre
        s["producto_descripcion"] = stock.producto.descripcion
        s["cantidad"] = stock.cantidad
        stock_encontrado = True
        break

    if not stock_encontrado:
      raise ValueError("No se ha encontrado stock para el producto.")

    self.grabar_archivo(stock_)
    return stock

  def eliminar(self, producto_id: int) -> bool:
    stock_ = self.leer_archivo()

    stock_actualizado = [
      s for s in stock_
      if int(s["id_producto"]) != producto_id
    ]

    if len(stock_) == len(stock_actualizado):
      return False

    self.grabar_archivo(stock_actualizado)
    return True

# ------------------------------------------
### CRUD COTIZACION DOLAR
class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  archivo: str
  # Ruta base en donde guardar archivos csv
  ruta_base:str="price_manager/migrations/csv/"

  def __init__(self, archivo="cotizacion.csv"):
    self.archivo = self.ruta_base + archivo

  def leer_archivo(self) -> List[dict]:
    try:
      with open(self.archivo, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
    except FileNotFoundError:
      return []

  def grabar_archivo(self, cotizaciones: List[dict]):
    with open(self.archivo, mode="w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f,fieldnames=["valor", "fecha", "id_tipo",
                                            "nombre_tipo"])
      writer.writeheader()
      writer.writerows(cotizaciones)

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    cotizaciones = self.leer_archivo()

    for c in cotizaciones:
      if (
        int(c["id_tipo"]) == cotizacion.tipo.id and
        c["fecha"] == cotizacion.fecha.isoformat()
      ):
        raise ValueError("Ya existe el tipo de cotización para la fecha ingresada.")

    cotizaciones.append({
      "valor": cotizacion.valor,
      "fecha": cotizacion.fecha.isoformat(),
      "id_tipo": cotizacion.tipo.id,
      "nombre_tipo": cotizacion.tipo.nombre
    })

    self.grabar_archivo(cotizaciones)
    return cotizacion

  def leer_por_tipo_y_fecha(
    self,
    tipo_id: int,
    fecha: datetime.date
  ) -> Optional[CotizacionDolar]:

    cotizaciones = self.leer_archivo()

    for c in cotizaciones:
      if (
        int(c["id_tipo"]) == tipo_id and
        c["fecha"] == fecha.isoformat()
      ):
        tipo = TipoCotizacion(
          int(c["id_tipo"]),
          c["nombre_tipo"]
        )

        return CotizacionDolar(
          float(c["valor"]),
          datetime.date.fromisoformat(c["fecha"]),
          tipo
        )

    return None

  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    cotizaciones = self.leer_archivo()
    historico = []

    for c in cotizaciones:
      if int(c["id_tipo"]) == tipo_id:
        tipo = TipoCotizacion(
          int(c["id_tipo"]),
          c["nombre_tipo"]
        )

        historico.append(
          CotizacionDolar(
            float(c["valor"]),
            datetime.date.fromisoformat(c["fecha"]),
            tipo
          )
        )

    return historico

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    cotizaciones = self.leer_archivo()
    cotizacion_encontrada = False

    for c in cotizaciones:
      if (
        int(c["id_tipo"]) == cotizacion.tipo.id and
        c["fecha"] == cotizacion.fecha.isoformat()
      ):
        c["valor"] = cotizacion.valor
        c["nombre_tipo"] = cotizacion.tipo.nombre
        cotizacion_encontrada = True
        break

    if not cotizacion_encontrada:
      raise ValueError("No existe una cotización para ese tipo y fecha.")

    self.grabar_archivo(cotizaciones)
    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    cotizaciones = self.leer_archivo()

    cotizaciones_actualizadas = [
      c for c in cotizaciones
      if not (
        int(c["id_tipo"]) == tipo_id and
        c["fecha"] == fecha.isoformat()
      )
    ]

    if len(cotizaciones_actualizadas) == len(cotizaciones):
      return False

    self.grabar_archivo(cotizaciones_actualizadas)
    return True
