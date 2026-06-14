import datetime
from typing import List, Optional

from sqlalchemy import text

from price_manager.database.connection import ConexionDB
from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  Moneda,
  Precio,
  Producto,
  Proveedor,
  Stock,
  TipoCotizacion,
)


class RepositorioCategoria:

  def crear(self, categoria: Categoria) -> Categoria:
    """
      Ejecuta un query de insercion.

      Args:
          categoria:
              Objeto de tipo Categoria a insertar.

      Retorna:
              Categoría insertada.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Categoria (Id, Nombre)
          VALUES (:id, :nombre)
          """
        ),
        {
          "id": categoria.id,
          "nombre": categoria.nombre,
        },
      )

    return categoria

  def leer_por_id(self, id: int) -> Optional[Categoria]:
    """
      Busca una categoría por su identificador.

      Args:
          id:
              Identificador de la categoría.

      Retorna:
              Categoría encontrada o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Categoria
          WHERE Id = :id
          """
        ),
        {"id": id},
      ).mappings().first()

    if fila is None:
      return None

    return Categoria(fila["Id"], fila["Nombre"])

  def leer_todos(self) -> List[Categoria]:
    """
      Ejecuta un query de seleccion.

      Retorna:
              Lista de Categorías existentes.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Categoria
          """
        )
      ).mappings().all()

    return [
      Categoria(fila["Id"], fila["Nombre"])
      for fila in filas
    ]

  def actualizar(self, categoria: Categoria) -> Categoria:
    """
      Ejecuta un query de actualización.

      Args:
          categoria:
              Objeto de tipo Categoria a actualizar.

      Retorna:
              Categoría actualizada.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Categoria
          SET Nombre = :nombre
          WHERE Id = :id
          """
        ),
        {
          "id": categoria.id,
          "nombre": categoria.nombre,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe una categoría con ese ID.")

    return categoria

  def eliminar(self, id: int) -> bool:
    """
      Ejecuta un query de eliminación / baja física.

      Args:
           id:
              entero que representa categoría a eliminar.

      Retorna:
              Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Categoria
          WHERE Id = :id
          """
        ),
        {"id": id},
      )

    return resultado.rowcount > 0


class RepositorioProveedor:

  def crear(self, proveedor: Proveedor) -> Proveedor:
    """
      Ejecuta un query de inserción de proveedor.

      Args:
          proveedor:
              Objeto Proveedor a insertar.

      Retorna:
              Proveedor insertado.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Proveedor (Id, Nombre, Contacto)
          VALUES (:id, :nombre, :contacto)
          """
        ),
        {
          "id": proveedor.id,
          "nombre": proveedor.nombre,
          "contacto": proveedor.contacto,
        },
      )

    return proveedor

  def leer_por_id(self, id: int) -> Optional[Proveedor]:
    """
    Busca en tabla algún registro asociado al id dado.

    Args:
        id:
            Entero que representa el id del proveedor a buscar.

    Retorna:
            Proveedor encontrado o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT Id, Nombre, Contacto
          FROM Proveedor
          WHERE Id = :id
          """
        ),
        {"id": id},
      ).mappings().first()

    if fila is None:
      return None

    return Proveedor(
      fila["Id"],
      fila["Nombre"],
      fila["Contacto"],
    )

  def leer_todos(self) -> List[Proveedor]:
    """
      Recupera todos los proveedores registrados.

      Retorna:
              Lista de proveedores.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Id, Nombre, Contacto
          FROM Proveedor
          """
        )
      ).mappings().all()

    return [
      Proveedor(fila["Id"], fila["Nombre"], fila["Contacto"])
      for fila in filas
    ]

  def actualizar(self, proveedor: Proveedor) -> Proveedor:
    """
      Actualiza los datos de un proveedor existente.

      Args:
          proveedor:
              Proveedor con los datos actualizados.

      Retorna:
              Proveedor actualizado.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Proveedor
          SET Nombre = :nombre,
              Contacto = :contacto
          WHERE Id = :id
          """
        ),
        {
          "id": proveedor.id,
          "nombre": proveedor.nombre,
          "contacto": proveedor.contacto,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe un proveedor con ese ID.")

    return proveedor

  def eliminar(self, id: int) -> bool:
    """
      Elimina un proveedor por su identificador.

      Args:
          id:
              Identificador del proveedor.

      Retorna:
              True si se eliminó correctamente.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Proveedor
          WHERE Id = :id
          """
        ),
        {"id": id},
      )

    return resultado.rowcount > 0


class RepositorioMoneda:

  def crear(self, moneda: Moneda) -> Moneda:
    """
    Ejecuta un query de inserción.

    Args:
        moneda:
            Objeto de tipo Moneda a insertar.

    Retorna:
            Moneda insertada.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Moneda (Id, Nombre)
          VALUES (:id, :nombre)
          """
        ),
        {
          "id": moneda.id,
          "nombre": moneda.nombre,
        },
      )

    return moneda

  def leer_por_id(self, id: int) -> Optional[Moneda]:
    """
    Busca en tabla algún registro asociado al id dado.

    Args:
        id:
            Entero que representa el id de la moneda a buscar.

    Retorna:
            Moneda encontrada o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Moneda
          WHERE Id = :id
          """
        ),
        {"id": id},
      ).mappings().first()

    if fila is None:
      return None

    return Moneda(fila["Id"], fila["Nombre"])

  def leer_todos(self) -> List[Moneda]:
    """
    Ejecuta un query de selección.

    Retorna:
            Lista de monedas existentes.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Moneda
          """
        )
      ).mappings().all()

    return [
      Moneda(fila["Id"], fila["Nombre"])
      for fila in filas
    ]

  def actualizar(self, moneda: Moneda) -> Moneda:
    """
    Ejecuta un query de actualización.

    Args:
        moneda:
            Objeto de tipo Moneda a actualizar.

    Retorna:
            Moneda actualizada.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Moneda
          SET Nombre = :nombre
          WHERE Id = :id
          """
        ),
        {
          "id": moneda.id,
          "nombre": moneda.nombre,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe una moneda con ese ID.")

    return moneda

  def eliminar(self, id: int) -> bool:
    """
    Ejecuta un query de eliminación / baja física.

    Args:
        id:
            Entero que representa la moneda a eliminar.

    Retorna:
            Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Moneda
          WHERE Id = :id
          """
        ),
        {"id": id},
      )

    return resultado.rowcount > 0


class RepositorioTipoCotizacion:

  def crear(self, tipo: TipoCotizacion) -> TipoCotizacion:
    """
    Ejecuta un query de inserción.

    Args:
        tipo:
            Objeto de tipo TipoCotizacion a insertar.

    Retorna:
            Tipo de cotización insertado.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Tipo_Cotizacion (Id, Nombre)
          VALUES (:id, :nombre)
          """
        ),
        {
          "id": tipo.id,
          "nombre": tipo.nombre,
        },
      )

    return tipo

  def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
    """
    Busca en tabla algún registro asociado al id dado.

    Args:
        id:
            Entero que representa el id del tipo de cotización.

    Retorna:
            Tipo de cotización encontrado o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Tipo_Cotizacion
          WHERE Id = :id
          """
        ),
        {"id": id},
      ).mappings().first()

    if fila is None:
      return None

    return TipoCotizacion(fila["Id"], fila["Nombre"])

  def leer_todos(self) -> List[TipoCotizacion]:
    """
    Ejecuta un query de selección.

    Retorna:
            Lista de tipos de cotización existentes.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Id, Nombre
          FROM Tipo_Cotizacion
          """
        )
      ).mappings().all()

    return [
      TipoCotizacion(fila["Id"], fila["Nombre"])
      for fila in filas
    ]

  def actualizar(self, tipo: TipoCotizacion) -> TipoCotizacion:
    """
    Ejecuta un query de actualización.

    Args:
        tipo:
            Objeto de tipo TipoCotizacion a actualizar.

    Retorna:
            Tipo de cotización actualizado.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Tipo_Cotizacion
          SET Nombre = :nombre
          WHERE Id = :id
          """
        ),
        {
          "id": tipo.id,
          "nombre": tipo.nombre,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe un tipo de cotización con ese ID.")

    return tipo

  def eliminar(self, id: int) -> bool:
    """
    Ejecuta un query de eliminación / baja física.

    Args:
        id:
            Entero que representa el tipo de cotización a eliminar.

    Retorna:
            Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Tipo_Cotizacion
          WHERE Id = :id
          """
        ),
        {"id": id},
      )

    return resultado.rowcount > 0


class RepositorioProducto:

  def crear(self, producto: Producto) -> Producto:
    """
    Ejecuta un query de inserción.

    Args:
        producto:
            Objeto de tipo Producto a insertar.

    Retorna:
            Producto insertado.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Producto
          (
            Id,
            Nombre,
            Descripcion,
            Precio,
            Id_Moneda,
            Id_Categoria,
            Id_Proveedor
          )
          VALUES
          (
            :id,
            :nombre,
            :descripcion,
            :precio,
            :id_moneda,
            :id_categoria,
            :id_proveedor
          )
          """
        ),
        {
          "id": producto.id,
          "nombre": producto.nombre,
          "descripcion": producto.descripcion,
          "precio": producto.precio.valor,
          "id_moneda": producto.precio.moneda.id,
          "id_categoria": producto.categoria.id,
          "id_proveedor": producto.proveedor.id,
        },
      )

    return producto

  def leer_por_id(self, id: int) -> Optional[Producto]:
    """
    Busca un producto por su identificador.

    Args:
        id:
            Entero que representa el id del producto.

    Retorna:
            Producto encontrado o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT
            p.Id,
            p.Nombre,
            p.Descripcion,
            p.Precio,
            m.Id AS Moneda_Id,
            m.Nombre AS Moneda_Nombre,
            c.Id AS Categoria_Id,
            c.Nombre AS Categoria_Nombre,
            pv.Id AS Proveedor_Id,
            pv.Nombre AS Proveedor_Nombre,
            pv.Contacto AS Proveedor_Contacto
          FROM Producto p
          INNER JOIN Moneda m
            ON p.Id_Moneda = m.Id
          INNER JOIN Categoria c
            ON p.Id_Categoria = c.Id
          INNER JOIN Proveedor pv
            ON p.Id_Proveedor = pv.Id
          WHERE p.Id = :id
          """
        ),
        {"id": id},
      ).mappings().first()

    if fila is None:
      return None

    moneda = Moneda(fila["Moneda_Id"], fila["Moneda_Nombre"])

    precio = Precio(
      float(fila["Precio"]),
      moneda,
      datetime.date.today(),
    )

    categoria = Categoria(
      fila["Categoria_Id"],
      fila["Categoria_Nombre"],
    )

    proveedor = Proveedor(
      fila["Proveedor_Id"],
      fila["Proveedor_Nombre"],
      fila["Proveedor_Contacto"],
    )

    return Producto(
      fila["Id"],
      fila["Nombre"],
      fila["Descripcion"],
      precio,
      categoria,
      proveedor,
    )

  def leer_todos(self) -> List[Producto]:
    """
    Ejecuta un query de selección.

    Retorna:
            Lista de productos existentes.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Id
          FROM Producto
          """
        )
      ).mappings().all()

    return [
      self.leer_por_id(fila["Id"])
      for fila in filas
    ]

  def actualizar(self, producto: Producto) -> Producto:
    """
    Ejecuta un query de actualización.

    Args:
        producto:
            Objeto de tipo Producto a actualizar.

    Retorna:
            Producto actualizado.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Producto
          SET Nombre = :nombre,
              Descripcion = :descripcion,
              Precio = :precio,
              Id_Moneda = :id_moneda,
              Id_Categoria = :id_categoria,
              Id_Proveedor = :id_proveedor
          WHERE Id = :id
          """
        ),
        {
          "id": producto.id,
          "nombre": producto.nombre,
          "descripcion": producto.descripcion,
          "precio": producto.precio.valor,
          "id_moneda": producto.precio.moneda.id,
          "id_categoria": producto.categoria.id,
          "id_proveedor": producto.proveedor.id,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe un producto con ese ID.")

    return producto

  def eliminar(self, id: int) -> bool:
    """
    Ejecuta un query de eliminación / baja física.

    Args:
        id:
            Entero que representa el producto a eliminar.

    Retorna:
            Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Producto
          WHERE Id = :id
          """
        ),
        {"id": id},
      )

    return resultado.rowcount > 0


class RepositorioStock:

  def crear(self, stock: Stock) -> Stock:
    """
    Ejecuta un query de inserción.

    Args:
        stock:
            Objeto de tipo Stock a insertar.

    Retorna:
            Stock insertado.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Stock (Id_Producto, Cantidad)
          VALUES (:id_producto, :cantidad)
          """
        ),
        {
          "id_producto": stock.producto.id,
          "cantidad": stock.cantidad,
        },
      )

    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    """
    Busca el stock asociado a un producto.

    Args:
        producto_id:
            Identificador del producto.

    Retorna:
            Stock encontrado o None.
    """
    producto = RepositorioProducto().leer_por_id(producto_id)

    if producto is None:
      return None

    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT Id_Producto, Cantidad
          FROM Stock
          WHERE Id_Producto = :id_producto
          """
        ),
        {"id_producto": producto_id},
      ).mappings().first()

    if fila is None:
      return None

    return Stock(producto, fila["Cantidad"])

  def actualizar(self, stock: Stock) -> Stock:
    """
    Ejecuta un query de actualización.

    Args:
        stock:
            Objeto de tipo Stock a actualizar.

    Retorna:
            Stock actualizado.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Stock
          SET Cantidad = :cantidad
          WHERE Id_Producto = :id_producto
          """
        ),
        {
          "id_producto": stock.producto.id,
          "cantidad": stock.cantidad,
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe stock para ese producto.")

    return stock

  def eliminar(self, producto_id: int) -> bool:
    """
    Ejecuta un query de eliminación / baja física.

    Args:
        producto_id:
            Identificador del producto.

    Retorna:
            Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Stock
          WHERE Id_Producto = :id_producto
          """
        ),
        {"id_producto": producto_id},
      )

    return resultado.rowcount > 0


class RepositorioCotizacionDolar:

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    """
    Ejecuta un query de inserción.

    Args:
        cotizacion:
            Objeto de tipo CotizacionDolar a insertar.

    Retorna:
            Cotización insertada.
    """
    with ConexionDB() as cn:
      cn.execute(
        text(
          """
          INSERT INTO Cotizacion_Dolar
          (
            Valor,
            Id_Tipo_Cotizacion,
            Fecha
          )
          VALUES
          (
            :valor,
            :id_tipo,
            :fecha
          )
          """
        ),
        {
          "valor": cotizacion.valor,
          "id_tipo": cotizacion.tipo.id,
          "fecha": cotizacion.fecha.isoformat(),
        },
      )

    return cotizacion

  def leer_por_tipo_y_fecha(self,tipo_id: int,fecha: datetime.date,) -> Optional[CotizacionDolar]:
    """
    Ejecuta un query de selección de cotización por fecha y tipo.

    Args:
        tipo_id:
            Entero que representa el tipo de cotización.

        fecha:
            Fecha de la cotización.

    Retorna:
            Cotización encontrada o None.
    """
    with ConexionDB() as cn:
      fila = cn.execute(
        text(
          """
          SELECT
            c.Valor,
            c.Fecha,
            t.Id AS Tipo_Id,
            t.Nombre AS Tipo_Nombre
          FROM Cotizacion_Dolar c
          INNER JOIN Tipo_Cotizacion t
            ON c.Id_Tipo_Cotizacion = t.Id
          WHERE c.Id_Tipo_Cotizacion = :tipo_id
            AND c.Fecha = :fecha
          """
        ),
        {
          "tipo_id": tipo_id,
          "fecha": fecha.isoformat(),
        },
      ).mappings().first()

    if fila is None:
      return None

    tipo = TipoCotizacion(
      fila["Tipo_Id"],
      fila["Tipo_Nombre"],
    )

    return CotizacionDolar(
      fila["Valor"],
      datetime.date.fromisoformat(fila["Fecha"]),
      tipo,
    )

  def leer_historico_por_tipo(self,tipo_id: int,) -> List[CotizacionDolar]:
    """
      Ejecuta un query de selección de cotizacion por tipo cotizacion.

      Args:
          tipo_id:
              entero que representa id de tipo cotizacion.

      Retorna:
              Lista de cotizaciones.
    """
    with ConexionDB() as cn:
      filas = cn.execute(
        text(
          """
          SELECT Fecha
          FROM Cotizacion_Dolar
          WHERE Id_Tipo_Cotizacion = :tipo_id
          ORDER BY Fecha
          """
        ),
        {"tipo_id": tipo_id},
      ).mappings().all()

    return [
      self.leer_por_tipo_y_fecha(
        tipo_id,
        datetime.date.fromisoformat(fila["Fecha"]),
      )
      for fila in filas
    ]

  def actualizar(self,cotizacion: CotizacionDolar,) -> CotizacionDolar:
    """
    Ejecuta un query de actualización.

    Args:
        cotizacion:
            Objeto de tipo CotizacionDolar a actualizar.

    Retorna:
            Cotización actualizada.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          UPDATE Cotizacion_Dolar
          SET Valor = :valor
          WHERE Id_Tipo_Cotizacion = :id_tipo
            AND Fecha = :fecha
          """
        ),
        {
          "valor": cotizacion.valor,
          "id_tipo": cotizacion.tipo.id,
          "fecha": cotizacion.fecha.isoformat(),
        },
      )

    if resultado.rowcount == 0:
      raise ValueError("No existe cotización para ese tipo y fecha.")

    return cotizacion

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """
    Ejecuta un query de eliminación / baja física.

    Args:
        tipo_id:
            Identificador del tipo de cotización.

        fecha:
            Fecha de la cotización.

    Retorna:
            Booleano que indica si hubo filas afectadas o no.
    """
    with ConexionDB() as cn:
      resultado = cn.execute(
        text(
          """
          DELETE FROM Cotizacion_Dolar
          WHERE Id_Tipo_Cotizacion = :tipo_id
            AND Fecha = :fecha
          """
        ),
        {
          "tipo_id": tipo_id,
          "fecha": fecha.isoformat(),
        },
      )

    return resultado.rowcount > 0
