
import abc
from typing import TypeVar, Generic, List, Optional
from price_manager.repositories.repositories import (
    RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
    RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock,
    RepositorioCotizacionDolar,
)
import datetime
from price_manager.entities.entities import (
    Categoria, Proveedor, Moneda, TipoCotizacion, Precio, Producto, CotizacionDolar, Stock
)

### PROVEEDORES
class ServicioProveedor:
    def __init__(self, proveedor_repo: RepositorioProveedor):
        self.proveedor_repo = proveedor_repo

    def crear(self, proveedor: Proveedor) -> Proveedor:
        return self.proveedor_repo.crear(proveedor)

    def obtener(self, id: int) -> Optional[Proveedor]:
        proveedor = self.proveedor_repo.leer_por_id(id)

        if proveedor is None:
          raise ValueError("No existe el proveedor.")

        return proveedor

    def listar_todos(self) -> List[Proveedor]:
        return self.proveedor_repo.leer_todos()

    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        return self.proveedor_repo.actualizar(proveedor)

    def eliminar(self, id: int) -> bool:
        eliminado = self.proveedor_repo.eliminar(id)

        if not eliminado:
            raise ValueError("No existe el proveedor ingresado.")

        return True

# --------------------------
### CATEGORIAS

class ServicioCategoria:
    def __init__(self, categoria_repo: RepositorioCategoria):
        self.categoria_repo = categoria_repo

    def crear(self, categoria: Categoria) -> Categoria:
        return self.categoria_repo.crear(categoria)

    def obtener(self, id: int) -> Optional[Categoria]:
        categoria = self.categoria_repo.leer_por_id(id)

        if categoria is None:
          raise ValueError("No existe la categoria.")

        return categoria

    def listar_todos(self) -> List[Categoria]:
        return self.categoria_repo.leer_todos()

    def actualizar(self, categoria: Categoria) -> Categoria:
        return self.categoria_repo.actualizar(categoria)

    def eliminar(self, id: int) -> bool:
        eliminado = self.categoria_repo.eliminar(id)

        if not eliminado:
          raise ValueError("No existe la categoria.")

        return True

# --------------------------
### MONEDAS

class ServicioMoneda:
    def __init__(self, moneda_repo: RepositorioMoneda):
        self.moneda_repo = moneda_repo

    def crear(self, moneda: Moneda) -> Moneda:
        return self.moneda_repo.crear(moneda)

    def obtener(self, id: int) -> Optional[Moneda]:
        moneda = self.moneda_repo.leer_por_id(id)

        if moneda is None:
          raise ValueError("No existe la moneda ingresada.")

        return moneda

    def listar_todos(self) -> List[Moneda]:
        return self.moneda_repo.leer_todos()

    def actualizar(self, moneda: Moneda) -> Moneda:
        return self.moneda_repo.actualizar(moneda)

    def eliminar(self, id: int) -> bool:
        eliminado = self.moneda_repo.eliminar(id)

        if not eliminado:
          raise ValueError("No existe la moneda ingresada.")

        return True

#-------------------------------------
### TIPO COTIZACION

class ServicioTipoCotizacion:
    def __init__(self, tipo_repo: RepositorioTipoCotizacion):
        self.tipo_repo = tipo_repo

    def crear(self, tipo: TipoCotizacion) -> TipoCotizacion:
        return self.tipo_repo.crear(tipo)

    def obtener(self, id: int) -> Optional[TipoCotizacion]:
        tipo = self.tipo_repo.leer_por_id(id)

        if tipo is None:
          raise ValueError("No existe el tipo de cotización.")

        return tipo

    def listar_todos(self) -> List[TipoCotizacion]:
        return self.tipo_repo.leer_todos()

    def actualizar(self, tipo: TipoCotizacion) -> TipoCotizacion:
        return self.tipo_repo.actualizar(tipo)

    def eliminar(self, id: int) -> bool:
        eliminado = self.tipo_repo.eliminar(id)

        if not eliminado:
          raise ValueError("No existe el tipo de cotizacion ingresado.")

        return True

#--------------------------------------
### PRODUCTO

class ServicioProducto:
    def __init__(
        self,
        producto_repo: RepositorioProducto,
        categoria_servicio: ServicioCategoria,
        proveedor_servicio: ServicioProveedor
    ):
        self.producto_repositorio = producto_repo
        self.categoria_servicio = categoria_servicio
        self.proveedor_servicio = proveedor_servicio

    def crear(self,producto: Producto) -> Producto:
        proveedor = self.proveedor_servicio.obtener(producto.proveedor.id)
        if proveedor is None:
            raise ValueError("El proveedor ingresado no existe.")

        categoria = self.categoria_servicio.obtener(producto.categoria.id)
        if categoria is None:
            raise ValueError("La categoría ingresada no existe.")

        return self.producto_repositorio.crear(producto)

    def obtener(self, id: int) -> Optional[Producto]:
        producto = self.producto_repositorio.leer_por_id(id)

        if producto is None:
          raise ValueError("No existe el producto.")

        return producto

    def listar_todos(self) -> List[Producto]:
        return self.producto_repositorio.leer_todos()

    def actualizar(self,producto: Producto) -> Producto:
        proveedor = self.proveedor_servicio.obtener(producto.proveedor.id)
        if proveedor is None:
            raise ValueError("El proveedor ingresado no existe.")

        categoria = self.categoria_servicio.obtener(producto.categoria.id)
        if categoria is None:
            raise ValueError("La categoría ingresada no existe.")

        return self.producto_repositorio.actualizar(producto)

    def eliminar(self, id: int) -> bool:
        eliminado = self.producto_repositorio.eliminar(id)

        if not eliminado:
          raise ValueError("No existe el producto.")

        return True

# ----------------------------------
### STOCK

class ServicioStock:
    def __init__(
        self,
        stock_repo: RepositorioStock,
        producto_servicio: ServicioProducto
    ):
        self.stock_repo = stock_repo
        self.producto_servicio = producto_servicio

    def crear(self, stock: Stock) -> Stock:
        producto = self.producto_servicio.obtener(stock.producto.id)

        if producto is None:
            raise ValueError("El producto no existe.")

        if stock.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return self.stock_repo.crear(stock)

    def actualizar(self, stock: Stock) -> Stock:
        producto = self.producto_servicio.obtener(stock.producto_id)

        if producto is None:
            raise ValueError("El producto no existe.")

        if stock.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        return self.stock_repo.actualizar(stock)

    def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
        return self.stock_repo.leer_por_producto(producto_id)

    def eliminar(self, producto_id: int) -> bool:
        return self.stock_repo.eliminar(producto_id)

    def obtener_stock(self, producto_id: int) -> int:
        """Obtiene el stock de un producto.

        Args:
            producto_id (int): el id del producto a consultar stock.

        Returns:
            un entero con el stock correspondiente.
        """
        stock = self.stock_repo.leer_por_producto(producto_id)

        if stock is None:
            return 0

        return stock.cantidad

    def registrar_movimiento(self, producto_id: int, cantidad: int) -> int:
        """Registra un movimiento de stock para un producto.

        Args:
            producto_id (int): el id del producto a registrar movimiento.
            cantidad (int): cantidad a registrar.
        Returns:
            un entero con el stock actualizado.

        Raises:
            Producto inexsistente, Stock negativo.
        """
        producto = self.producto_servicio.obtener(producto_id)

        if producto is None:
          raise ValueError("El producto no existe.")

        stock_actual = self.obtener_stock(producto_id)
        nuevo_stock = stock_actual + cantidad

        if nuevo_stock < 0:
            raise ValueError("No se permite stock negativo.")

        stock_existente = self.stock_repo.leer_por_producto(producto_id)

        nuevo_stock_obj = Stock(producto, nuevo_stock)

        if stock_existente is None:
            self.stock_repo.crear(nuevo_stock_obj)
        else:
            self.stock_repo.actualizar(nuevo_stock_obj)

        return nuevo_stock

# --------------------------------------
### COTIZACION DOLAR

class ServicioCotizacionDolar:
    def __init__(
        self,
        cotizacion_repo: RepositorioCotizacionDolar,
        tipo_servicio: ServicioTipoCotizacion
    ):
        self.cotizacion_repo = cotizacion_repo
        self.tipo_servicio = tipo_servicio

    def crear(
        self,
        cotizacion: CotizacionDolar
    ) -> CotizacionDolar:

        tipo = self.tipo_servicio.obtener(cotizacion.tipo.id)

        if tipo is None:
            raise ValueError("El tipo de cotización no existe.")

        if cotizacion.valor <= 0:
            raise ValueError("El valor debe ser mayor a 0.")

        cotizacion = CotizacionDolar(cotizacion.valor, cotizacion.fecha, tipo)

        return self.cotizacion_repo.crear(cotizacion)

    def leer(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]:
        return self.cotizacion_repo.leer_por_tipo_y_fecha(tipo_id, fecha)

    def leer_historico(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee historico de registros de cotizaciones para un tipo de cot.

        Args:
            tipo_id (int): el id del tipo a consultar historico.

        Returns:
            Lista de cotizaciones.
        """
        return self.cotizacion_repo.leer_historico_por_tipo(tipo_id)

    def actualizar(self,cotizacion: CotizacionDolar) -> CotizacionDolar:
        tipo = self.tipo_servicio.obtener(cotizacion.tipo.id)

        if tipo is None:
            raise ValueError("El tipo de cotización no existe.")

        return self.cotizacion_repo.actualizar(cotizacion)

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        eliminado = self.cotizacion_repo.eliminar(tipo_id, fecha)

        if not eliminado:
            raise ValueError("No existe cotización para ese tipo y fecha.")

        return True

    def registrar_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Registra una cotizacion.

        Args:
            cotizacion (CotizacionDolar): objeto de tipo CotizacionDolar.

        Returns:
            La cotizacion creada.

        Raises:
            Tipo de cotizacion inexistente.
        """
        tipo = self.tipo_servicio.obtener(cotizacion.tipo.id)

        if tipo is None:
            raise ValueError("El tipo de cotización no existe.")

        return self.cotizacion_repo.crear(cotizacion)

    def obtener_historico(self, tipo_id: int) -> List[CotizacionDolar]:
        tipo = self.tipo_servicio.obtener(tipo_id)

        if tipo is None:
            raise ValueError("El tipo de cotización no existe.")

        return self.cotizacion_repo.leer_historico_por_tipo(tipo_id)

    def obtener(self,tipo_id: int,fecha: datetime.date) -> CotizacionDolar:
        cotizacion = self.cotizacion_repo.leer_por_tipo_y_fecha(tipo_id,fecha)

        if cotizacion is None:
            raise ValueError("No existe cotización para ese tipo y fecha.")

        return cotizacion
