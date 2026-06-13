
import datetime

from IPython.display import clear_output

from price_manager.entities.entities import (
  Categoria,
  CotizacionDolar,
  Moneda,
  Precio,
  Producto,
  Proveedor,
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
from price_manager.services.services import (
  ServicioCategoria,
  ServicioCotizacionDolar,
  ServicioMoneda,
  ServicioProducto,
  ServicioProveedor,
  ServicioStock,
  ServicioTipoCotizacion,
)


def limpiar_consola() -> None:
  """Limpia la salida de consola."""
  clear_output()


def leer_entero(mensaje: str) -> int:
  """Solicita un número entero válido."""
  while True:
    valor = input(mensaje)

    try:
      return int(valor)
    except ValueError:
      print("Debe ingresar un número entero válido.")


def leer_float(mensaje: str) -> float:
  """Solicita un número decimal válido."""
  while True:
    valor = input(mensaje)

    try:
      numero = float(valor)

      if numero < 0:
        print("El valor no puede ser negativo.")
        continue

      return numero
    except ValueError:
      print("Debe ingresar un número válido.")


def leer_texto(mensaje: str) -> str:
  """Solicita texto no vacío."""
  while True:
    valor = input(mensaje).strip()

    if valor:
      return valor

    print("El texto ingresado no puede estar vacío.")


def leer_fecha(mensaje: str) -> datetime.date:
  """Solicita una fecha válida con formato ISO."""
  while True:
    valor = input(mensaje).strip()

    try:
      return datetime.date.fromisoformat(valor)
    except ValueError:
      print("Debe ingresar una fecha válida con formato YYYY-MM-DD.")


def leer_opcion(mensaje: str, opciones: list[str]) -> str:
  """Solicita una opción válida dentro de una lista."""
  while True:
    opcion = input(mensaje).strip()

    if opcion in opciones:
      return opcion

    print("Opción inválida.")


def pausar() -> None:
  """Pausa la ejecución hasta que el usuario presione Enter."""
  input("\nPresione Enter para continuar...")


def mostrar_titulo() -> None:
  """Muestra el encabezado del sistema."""
  print("=" * 45)
  print("Sistema de Gestión de Inventarios")
  print("=" * 45)


repo_categoria = RepositorioCategoria()
repo_proveedor = RepositorioProveedor()
repo_moneda = RepositorioMoneda()
repo_tipo = RepositorioTipoCotizacion()
repo_producto = RepositorioProducto()
repo_stock = RepositorioStock()
repo_cotizacion = RepositorioCotizacionDolar()

srv_categoria = ServicioCategoria(repo_categoria)
srv_proveedor = ServicioProveedor(repo_proveedor)
srv_moneda = ServicioMoneda(repo_moneda)
srv_tipo = ServicioTipoCotizacion(repo_tipo)
srv_producto = ServicioProducto(
  repo_producto,
  srv_categoria,
  srv_proveedor,
)
srv_stock = ServicioStock(repo_stock, srv_producto)
srv_cotizacion = ServicioCotizacionDolar(
  repo_cotizacion,
  srv_tipo,
)


def menu_inicio() -> str:
  """Muestra el menú inicial."""
  limpiar_consola()
  mostrar_titulo()

  print("1 - Menú principal")
  print("2 - Salir")

  return leer_opcion("\nSeleccione una opción: ", ["1", "2"])


def menu_entidades() -> str:
  """Muestra el menú de entidades."""
  limpiar_consola()
  mostrar_titulo()

  print("1 - Categorías")
  print("2 - Proveedores")
  print("3 - Monedas")
  print("4 - Tipos de cotización")
  print("5 - Productos")
  print("6 - Stock")
  print("7 - Cotización dólar")
  print("8 - Salir")

  return leer_opcion("\nSeleccione una opción: ", [
    "1", "2", "3", "4", "5", "6", "7", "8"
  ])


def menu_crud_basico(nombre: str) -> str:
  """Muestra el menú CRUD para entidades básicas."""
  limpiar_consola()
  mostrar_titulo()

  print(f"Gestión de {nombre}")
  print("1 - Crear")
  print("2 - Obtener por ID")
  print("3 - Listar")
  print("4 - Actualizar")
  print("5 - Eliminar")
  print("0 - Volver")

  return leer_opcion("\nSeleccione una opción: ", [
    "0", "1", "2", "3", "4", "5"
  ])


def crear_entidad_basica(nombre: str, servicio) -> None:
  """Crea una entidad básica según el tipo indicado."""
  id_entidad = leer_entero("ID: ")

  if nombre == "categoría":
    nombre_entidad = leer_texto("Nombre: ")
    entidad = Categoria(id_entidad, nombre_entidad)

  elif nombre == "proveedor":
    nombre_entidad = leer_texto("Nombre: ")
    contacto = leer_texto("Contacto: ")
    entidad = Proveedor(id_entidad, nombre_entidad, contacto)

  elif nombre == "moneda":
    nombre_entidad = leer_texto("Código moneda: ").upper()
    entidad = Moneda(id_entidad, nombre_entidad)

  else:
    nombre_entidad = leer_texto("Nombre: ")
    entidad = TipoCotizacion(id_entidad, nombre_entidad)

  servicio.crear(entidad)
  print("Registro creado correctamente.")


def actualizar_entidad_basica(nombre: str, servicio) -> None:
  """Actualiza una entidad básica según el tipo indicado."""
  id_entidad = leer_entero("ID a actualizar: ")

  if nombre == "categoría":
    nombre_entidad = leer_texto("Nuevo nombre: ")
    entidad = Categoria(id_entidad, nombre_entidad)

  elif nombre == "proveedor":
    nombre_entidad = leer_texto("Nuevo nombre: ")
    contacto = leer_texto("Nuevo contacto: ")
    entidad = Proveedor(id_entidad, nombre_entidad, contacto)

  elif nombre == "moneda":
    nombre_entidad = leer_texto("Nuevo código moneda: ").upper()
    entidad = Moneda(id_entidad, nombre_entidad)

  else:
    nombre_entidad = leer_texto("Nuevo nombre: ")
    entidad = TipoCotizacion(id_entidad, nombre_entidad)

  servicio.actualizar(entidad)
  print("Registro actualizado correctamente.")


def ejecutar_crud_basico(nombre: str, servicio) -> None:
  """Ejecuta operaciones CRUD para entidades básicas."""
  while True:
    opcion = menu_crud_basico(nombre)

    if opcion == "0":
      break

    try:
      if opcion == "1":
        crear_entidad_basica(nombre, servicio)

      elif opcion == "2":
        id_entidad = leer_entero("ID: ")
        print(servicio.obtener(id_entidad))

      elif opcion == "3":
        for entidad in servicio.listar_todos():
          print(entidad)

      elif opcion == "4":
        actualizar_entidad_basica(nombre, servicio)

      elif opcion == "5":
        id_entidad = leer_entero("ID a eliminar: ")
        servicio.eliminar(id_entidad)
        print("Registro eliminado correctamente.")

    except ValueError as error:
      print(f"Error: {error}")

    pausar()


def menu_producto() -> str:
  """Muestra el menú CRUD de productos."""
  limpiar_consola()
  mostrar_titulo()

  print("Gestión de productos")
  print("1 - Crear")
  print("2 - Obtener por ID")
  print("3 - Listar")
  print("4 - Actualizar")
  print("5 - Eliminar")
  print("0 - Volver")

  return leer_opcion("\nSeleccione una opción: ", [
    "0", "1", "2", "3", "4", "5"
  ])


def solicitar_producto() -> Producto:
  """Solicita los datos necesarios para construir un producto."""
  id_producto = leer_entero("ID producto: ")
  nombre = leer_texto("Nombre: ")
  descripcion = leer_texto("Descripción: ")
  valor = leer_float("Precio: ")
  moneda_id = leer_entero("ID moneda: ")
  categoria_id = leer_entero("ID categoría: ")
  proveedor_id = leer_entero("ID proveedor: ")

  moneda = srv_moneda.obtener(moneda_id)
  categoria = srv_categoria.obtener(categoria_id)
  proveedor = srv_proveedor.obtener(proveedor_id)

  precio = Precio(valor, moneda, datetime.date.today())

  return Producto(
    id_producto,
    nombre,
    descripcion,
    precio,
    categoria,
    proveedor,
  )


def ejecutar_productos() -> None:
  """Ejecuta operaciones CRUD para productos."""
  while True:
    opcion = menu_producto()

    if opcion == "0":
      break

    try:
      if opcion == "1":
        producto = solicitar_producto()
        srv_producto.crear(producto)
        print("Producto creado correctamente.")

      elif opcion == "2":
        id_producto = leer_entero("ID producto: ")
        print(srv_producto.obtener(id_producto))

      elif opcion == "3":
        for producto in srv_producto.listar_todos():
          print(producto)

      elif opcion == "4":
        producto = solicitar_producto()
        srv_producto.actualizar(producto)
        print("Producto actualizado correctamente.")

      elif opcion == "5":
        id_producto = leer_entero("ID producto: ")
        srv_producto.eliminar(id_producto)
        print("Producto eliminado correctamente.")

    except ValueError as error:
      print(f"Error: {error}")

    pausar()


def menu_stock() -> str:
  """Muestra el menú de stock."""
  limpiar_consola()
  mostrar_titulo()

  print("Gestión de stock")
  print("1 - Registrar movimiento")
  print("2 - Consultar stock")
  print("3 - Eliminar stock")
  print("0 - Volver")

  return leer_opcion("\nSeleccione una opción: ", [
    "0", "1", "2", "3"
  ])


def ejecutar_stock() -> None:
  """Ejecuta operaciones de stock."""
  while True:
    opcion = menu_stock()

    if opcion == "0":
      break

    try:
      producto_id = leer_entero("ID producto: ")

      if opcion == "1":
        cantidad = leer_entero("Cantidad (+ ingreso / - egreso): ")
        nuevo_stock = srv_stock.registrar_movimiento(
          producto_id,
          cantidad,
        )
        print(f"Movimiento registrado. Stock actual: {nuevo_stock}")

      elif opcion == "2":
        stock = srv_stock.obtener_stock(producto_id)
        print(f"Stock actual: {stock}")

      elif opcion == "3":
        srv_stock.eliminar(producto_id)
        print("Stock eliminado correctamente.")

    except ValueError as error:
      print(f"Error: {error}")

    pausar()


def menu_cotizacion() -> str:
  """Muestra el menú de cotizaciones."""
  limpiar_consola()
  mostrar_titulo()

  print("Gestión de cotizaciones")
  print("1 - Registrar cotización")
  print("2 - Obtener por tipo y fecha")
  print("3 - Histórico por tipo")
  print("4 - Actualizar cotización")
  print("5 - Eliminar cotización")
  print("0 - Volver")

  return leer_opcion("\nSeleccione una opción: ", [
    "0", "1", "2", "3", "4", "5"
  ])


def solicitar_cotizacion() -> CotizacionDolar:
  """Solicita los datos necesarios para construir una cotización."""
  valor = leer_float("Valor cotización: ")
  tipo_id = leer_entero("ID tipo cotización: ")
  fecha = leer_fecha("Fecha (YYYY-MM-DD): ")
  tipo = srv_tipo.obtener(tipo_id)

  return CotizacionDolar(valor, fecha, tipo)


def ejecutar_cotizaciones() -> None:
  """Ejecuta operaciones CRUD para cotizaciones."""
  while True:
    opcion = menu_cotizacion()

    if opcion == "0":
      break

    try:
      if opcion == "1":
        cotizacion = solicitar_cotizacion()
        srv_cotizacion.registrar_cotizacion(cotizacion)
        print("Cotización registrada correctamente.")

      elif opcion == "2":
        tipo_id = leer_entero("ID tipo cotización: ")
        fecha = leer_fecha("Fecha (YYYY-MM-DD): ")
        print(srv_cotizacion.obtener(tipo_id, fecha))

      elif opcion == "3":
        tipo_id = leer_entero("ID tipo cotización: ")
        historico = srv_cotizacion.obtener_historico(tipo_id)

        for cotizacion in historico:
          print(cotizacion)

      elif opcion == "4":
        cotizacion = solicitar_cotizacion()
        srv_cotizacion.actualizar(cotizacion)
        print("Cotización actualizada correctamente.")

      elif opcion == "5":
        tipo_id = leer_entero("ID tipo cotización: ")
        fecha = leer_fecha("Fecha (YYYY-MM-DD): ")
        srv_cotizacion.eliminar(tipo_id, fecha)
        print("Cotización eliminada correctamente.")

    except ValueError as error:
      print(f"Error: {error}")

    pausar()


def main() -> None:
  """Ejecuta el menú principal del sistema."""
  while True:
    opcion_inicio = menu_inicio()

    if opcion_inicio == "2":
      print("Sistema finalizado.")
      break

    while True:
      opcion = menu_entidades()

      if opcion == "8":
        break

      if opcion == "1":
        ejecutar_crud_basico("categoría", srv_categoria)
      elif opcion == "2":
        ejecutar_crud_basico("proveedor", srv_proveedor)
      elif opcion == "3":
        ejecutar_crud_basico("moneda", srv_moneda)
      elif opcion == "4":
        ejecutar_crud_basico("tipo cotización", srv_tipo)
      elif opcion == "5":
        ejecutar_productos()
      elif opcion == "6":
        ejecutar_stock()
      elif opcion == "7":
        ejecutar_cotizaciones()
