import datetime
import subprocess

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
from price_manager.services.export_service import ServicioExportacion
from price_manager.services.alert_service import ServicioAlertasPrecio
from price_manager.reports.report_service import ServicioReportePrecios
from price_manager.services.audit_service import RepositorioAuditoria
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

# Cada repositorio encapsula el acceso a datos
# de una entidad específica dentro de SQLite.
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
srv_exportacion = ServicioExportacion()


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
  print("8 - Obtener cotizaciones por API")
  print("9 - Ver lista de precios bimonetaria")
  print("10 - Exportar precios a CSV")
  print("11 - Ejecutar scraping")
  print("12 - Generar reporte")
  print("13 - Ver historial de auditoría")
  print("14 - Salir")

  return leer_opcion("\nSeleccione una opción: ", [
    "1", "2", "3", "4", "5", "6",
    "7", "8", "9", "10", "11", "12", "13", "14",
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


def ejecutar_api_cotizaciones() -> None:
  """
  Ejecuta la obtención de cotizaciones desde la API
  y muestra los resultados obtenidos.
  """
  cotizaciones = srv_cotizacion.obtener_cotizaciones()

  print("Cotizaciones obtenidas y registradas:")

  for cotizacion in cotizaciones:
    print(
      cotizacion.tipo.nombre,
      cotizacion.valor,
      cotizacion.fecha,
    )


def mostrar_lista_bimonetaria() -> None:
  """Muestra precios en ARS y USD usando cotización registrada."""

  monedas_permitidas = ["ARS", "USD"]

  print("Monedas disponibles para lista bimonetaria:")
  print(", ".join(monedas_permitidas))

  while True:
    moneda_destino = leer_texto(
      "Ingrese moneda destino: "
    ).upper()

    if moneda_destino in monedas_permitidas:
      break

    print(
      "Moneda inválida. Para esta opción solo se permite ARS o USD."
    )

  historico = srv_cotizacion.obtener_historico(1)

  if len(historico) == 0:
    print("No hay cotización USD registrada.")
    return

  ultima_cotizacion = sorted(
    historico,
    key=lambda item: item.fecha,
  )[-1]

  cotizacion_usd = ultima_cotizacion.valor

  print(
    f"Cotización USD utilizada: "
    f"{cotizacion_usd:.2f} ARS"
  )

  productos = srv_producto.listar_todos()

  print("\nLista bimonetaria:\n")

  for producto in productos:
    precio_original = producto.precio.valor
    moneda_original = producto.precio.moneda.nombre.upper()

    if moneda_original == "ARS":
      precio_ars = precio_original
      precio_usd = precio_original / cotizacion_usd

    elif moneda_original == "USD":
      precio_usd = precio_original
      precio_ars = precio_original * cotizacion_usd

    else:
      print(
        f"{producto.id} - {producto.nombre}: "
        f"moneda {moneda_original} no soportada."
      )
      continue

    if moneda_destino == "ARS":
      print(
        f"{producto.id} - "
        f"{producto.nombre} | "
        f"{precio_usd:.2f} USD | "
        f"{precio_ars:.2f} ARS"
      )

    else:
      print(
        f"{producto.id} - "
        f"{producto.nombre} | "
        f"{precio_ars:.2f} ARS | "
        f"{precio_usd:.2f} USD"
      )


def exportar_precios_csv() -> None:
  """Exporta la lista de precios a un archivo CSV."""

  productos = srv_producto.listar_todos()

  ruta_archivo = (
    "/content/price_manager/"
    "exports/precios_productos.csv"
  )

  srv_exportacion.exportar_productos(
    productos,
    ruta_archivo,
  )

  print("Archivo CSV exportado correctamente.")
  print(ruta_archivo)


def ejecutar_scraping() -> None:
  """Ejecuta el scraper de Star Computación."""

  ruta_salida = (
    "/content/price_manager/"
    "exports/star_computacion.csv"
  )

  comando = [
    "python",
    "-m",
    "scrapy",
    "crawl",
    "star_computacion",
    "-a",
    "limite=10",
    "-a",
    "resultados_por_busqueda=10",
    "-a",
    f"archivo_salida={ruta_salida}",
  ]

  subprocess.run(
    comando,
    cwd="/content/price_manager",
    check=True,
  )

  print("Scraping ejecutado correctamente.")
  print(ruta_salida)


def generar_reporte() -> None:
  """Genera alertas CSV y reporte Excel de precios."""

  ruta_scraper = (
    "/content/price_manager/"
    "exports/star_computacion.csv"
  )
  ruta_alertas = (
    "/content/price_manager/"
    "exports/alertas_precios.csv"
  )
  ruta_reporte = (
    "/content/price_manager/"
    "exports/reporte_precios.xlsx"
  )

  diferencia_minima = leer_float(
    "Ingrese diferencia mínima para generar alertas: "
  )

  alertas = ServicioAlertasPrecio().generar_alertas(
    ruta_scraper=ruta_scraper,
    ruta_alertas=ruta_alertas,
    diferencia_minima=diferencia_minima,
  )

  ServicioReportePrecios().generar_reporte_excel(
    ruta_alertas=ruta_alertas,
    ruta_reporte=ruta_reporte,
  )

  print(f"Alertas generadas: {len(alertas)}")
  print("Reporte generado correctamente.")
  print(ruta_reporte)


def ver_historial_auditoria() -> None:
  """Muestra el historial de auditoría del sistema."""

  auditorias = RepositorioAuditoria().listar_todos()

  if len(auditorias) == 0:
    print("No hay registros de auditoría.")
    return

  for auditoria in auditorias:
    print(
      f"{auditoria.id} | "
      f"{auditoria.accion} | "
      f"{auditoria.fecha} | "
      f"{auditoria.detalles}"
    )


def main() -> None:
  """Ejecuta el menú principal del sistema."""
  while True:
    opcion_inicio = menu_inicio()

    if opcion_inicio == "2":
      print("Sistema finalizado.")
      break

    while True:
      opcion = menu_entidades()

      if opcion == "14":
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
      elif opcion == "8":
        ejecutar_api_cotizaciones()
        pausar()
      elif opcion == "9":
        mostrar_lista_bimonetaria()
        pausar()
      elif opcion == "10":
        exportar_precios_csv()
        pausar()
      elif opcion == "11":
        ejecutar_scraping()
        pausar()
      elif opcion == "12":
        generar_reporte()
        pausar()
      elif opcion == "13":
        ver_historial_auditoria()
        pausar()
