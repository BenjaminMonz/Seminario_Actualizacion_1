
# Importaciones que necesita el archivo para funcionar
from IPython.display import clear_output
from price_manager.repositories.repositories import (
    RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
    RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock,
    RepositorioCotizacionDolar,
)
from price_manager.services.services import (
    ServicioCategoria, ServicioProveedor, ServicioMoneda,
    ServicioTipoCotizacion, ServicioProducto, ServicioStock,
    ServicioCotizacionDolar,
)
from price_manager.entities.entities import (
    Categoria,
    Proveedor,
    Moneda,
    TipoCotizacion,
    Precio,
    Producto,
    CotizacionDolar
)
import datetime

# Función para limpiar la consola
def limpiar_consola():
    clear_output()

entidades_base: list[str] = ["categorias","proveedores","tipo_cotizacion","monedas"]

# REPOS
repo_cat = RepositorioCategoria()
repo_prov = RepositorioProveedor()
repo_mon = RepositorioMoneda()
repo_tipo = RepositorioTipoCotizacion()
repo_prod = RepositorioProducto()
repo_stock = RepositorioStock()
repo_cot = RepositorioCotizacionDolar()

# SERVICES
srv_cat = ServicioCategoria(repo_cat)
srv_prov = ServicioProveedor(repo_prov)
srv_mon = ServicioMoneda(repo_mon)
srv_tipo = ServicioTipoCotizacion(repo_tipo)
srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)
srv_stock = ServicioStock(repo_stock, srv_prod)
srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo)

#Funcion de print de nombre del sistema
def cartel():
  print("="*40)
  print(" "*2,"Sistema de Gestión de Inventarios")
  print("="*40, end="\n"*2)

#Funcion de menu inicial
def menu_INICIO() -> str:
  """Printea el menu de inicio.
  """
  limpiar_consola()
  cartel()
  opciones_disponibles:list[str] = ["1","2"]
  print("Ingrese la opcion que desea ejecutar:", end ="\n"*2)
  print(" "*2, "1 - Menu principal", end="\n")
  print(" "*2, "2 - Salir", end="\n"*2)

  while True:
    opcion = input("-> ")

    if opcion in opciones_disponibles:
      return opcion

    print("Opción inválida\n")

#Funcion generica de CRUD
def menu_CRUD(entidad:str) -> str:
  """Printea el menu de CRUD para una entidad.

  Args:
    entidad (str): La entidad a mostrar el menu.

  Returns:
    un str con la opcion seleccionada.
  """
  limpiar_consola()
  cartel()
  print(f"-- {entidad.replace('_',' ').title()}",end="\n"*2)
  opciones_disponibles:list[str] = ["0","1","2","3","4","5"]
  if entidad.lower() in entidades_base:
    print(" "*2, "1 - Alta", end="\n")
    print(" "*2, "2 - Obtener por ID", end="\n")
    print(" "*2, "3 - Listar", end="\n")
    print(" "*2, "4 - Actualizar", end="\n")
    print(" "*2, "5 - Baja", end="\n")
    print(" "*2, "0 - Volver", end="\n"*2)
  elif entidad.lower() == "productos":
    print(" "*2, "1 - Alta", end="\n")
    print(" "*2, "2 - Obtener por ID", end="\n")
    print(" "*2, "3 - Listar", end="\n")
    print(" "*2, "4 - Actualizar", end="\n")
    print(" "*2, "5 - Baja", end="\n")
    print(" "*2, "0 - Volver", end="\n"*2)
  elif entidad.lower() == "stock":
      print(" "*2, "1 - Registrar movimiento", end="\n")
      print(" "*2, "2 - Consultar stock de Producto", end="\n")
      print(" "*2, "3 - Eliminar stock de Producto", end="\n")
      print(" "*2, "0 - Volver", end="\n"*2)
      opciones_disponibles = ["0","1","2","3"]
  elif entidad.lower() == "cotizacion_dolar":
      print(" "*2, "1 - Registrar cotización", end="\n")
      print(" "*2, "2 - obtener cotización por tipo y fecha", end="\n")
      print(" "*2, "3 - Obtener histórico por tipo", end="\n")
      print(" "*2, "4 - Actualizar cotización", end="\n")
      print(" "*2, "5 - Eliminar cotización", end="\n")
      print(" "*2, "0 - Volver", end="\n"*2)

  while True:
    opcion = input("-> ")

    if opcion in opciones_disponibles:
      return opcion

    print("Opción inválida\n")

# Menu de entidades
def menu_ENTIDADES() -> str:
  """Printea el menu de entidades.

  Returns:
    un str con la opcion seleccionada.
  """
  limpiar_consola()
  cartel()
  opciones_disponibles: list[str] = ["1","2","3","4","5","6","7","8"]

  print(" "*2, "1 - Categorías", end="\n")
  print(" "*2, "2 - Proveedores", end="\n")
  print(" "*2, "3 - Monedas", end="\n")
  print(" "*2, "4 - Tipos de cotización", end="\n")
  print(" "*2, "5 - Productos", end="\n")
  print(" "*2, "6 - Stock", end="\n")
  print(" "*2, "7 - Cotización dólar", end="\n")
  print(" "*2, "8 - Salir", end="\n"*2)

  while True:
    opcion = input("-> ")

    if opcion in opciones_disponibles:
      return opcion

    print("Opción inválida\n")

# Menu para entidades con CRUD basico
def menu_CRUD_basico(entidad: str, opcion: str, servicio):
  """Printea el menu de CRUD basico.

  Args:
    entidad (str): La entidad seleccionada.
    opcion (str): La opcion seleccionada.
    servicio (service): El servicio para acceder al CRUD.
  """
  limpiar_consola()
  cartel()
  print(f"-- {entidad.replace('_',' ').title()}",end="\n"*2)
  try:
        if opcion == "1":  # ALTA
            print(" "*2, "ALTA", "\n")
            if entidad == "categorias":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                obj = Categoria(id, nombre)

            elif entidad == "proveedores":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                contacto = input("Contacto: ")
                obj = Proveedor(id, nombre, contacto)

            elif entidad == "monedas":
                id = int(input("ID: "))
                nombre = input("Nombre (3 letras): ")
                obj = Moneda(id, nombre)

            elif entidad == "tipo_cotizacion":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                obj = TipoCotizacion(id, nombre)

            servicio.crear(obj)
            print("Registro guardado correctamente.")


        elif opcion == "2":  # OBTENER
            print(" "*2, "OBTENER", "\n")
            id = int(input("ID: "))
            print(servicio.obtener(id))


        elif opcion == "3":  # LISTAR
            print(" "*2, "LISTAR", "\n")
            for obj in servicio.listar_todos():
                print(obj)


        elif opcion == "4":  # ACTUALIZAR
            print(" "*2, "ACTUALIZAR", "\n")
            if entidad == "categorias":
                id = int(input("ID: "))
                nombre = input("Nuevo nombre: ")
                obj = Categoria(id, nombre)

            elif entidad == "proveedores":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                contacto = input("Contacto: ")
                obj = Proveedor(id, nombre, contacto)

            elif entidad == "monedas":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                obj = Moneda(id, nombre)

            elif entidad == "tipo_cotizacion":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                obj = TipoCotizacion(id, nombre)

            servicio.actualizar(obj)
            print("Registro actualizado correctamente")


        elif opcion == "5":  # ELIMINAR
            print(" "*2, "ELIMINAR", "\n")
            id = int(input("ID: "))
            servicio.eliminar(id)
            print("registro eliminado correctamente")


  except Exception as e:
      print(f"Error: {e}")

# Menu para CRUD Productos
def menu_CRUD_Productos(opcion: str):
    """Printea el menu de CRUD Productos.
    Args:
      opcion (str): opcion seleccionada.
    Raises:
      Cualquier excepcion dentro del bloque Try
    """
    try:
        if opcion == "1":  # Alta
            print(" "*2, "ALTA", "\n")
            id = int(input("ID producto: "))
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")

            valor = float(input("Precio: "))
            moneda_id = int(input("ID moneda: "))
            categoria_id = int(input("ID categoría: "))
            proveedor_id = int(input("ID proveedor: "))

            moneda = srv_mon.obtener(moneda_id)
            categoria = srv_cat.obtener(categoria_id)
            proveedor = srv_prov.obtener(proveedor_id)

            precio = Precio(valor, moneda, datetime.date.today())
            producto = Producto(id, nombre, descripcion, precio, categoria, proveedor)

            srv_prod.crear(producto)
            print("Producto creado correctamente.")


        elif opcion == "2":  # Obtener
            print(" "*2, "OBTENER", "\n")
            id = int(input("ID producto: "))
            producto = srv_prod.obtener(id)
            print(producto)


        elif opcion == "3":  # Listar
            print(" "*2, "LISTAR", "\n")
            productos = srv_prod.listar_todos()
            for producto in productos:
                print(producto)


        elif opcion == "4":  # Actualizar
            print(" "*2, "ACTUALIZAR", "\n")
            id = int(input("ID producto: "))
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")

            valor = float(input("Nuevo precio: "))
            moneda_id = int(input("ID moneda: "))
            categoria_id = int(input("ID categoría: "))
            proveedor_id = int(input("ID proveedor: "))

            moneda = srv_mon.obtener(moneda_id)
            categoria = srv_cat.obtener(categoria_id)
            proveedor = srv_prov.obtener(proveedor_id)

            precio = Precio(valor, moneda, datetime.date.today())
            producto = Producto(id, nombre, descripcion, precio, categoria, proveedor)

            srv_prod.actualizar(producto)
            print("Producto actualizado correctamente.")


        elif opcion == "5":  # ELIMINAR
            print(" "*2, "ELIMINAR", "\n")
            id = int(input("ID producto: "))
            srv_prod.eliminar(id)
            print("Producto eliminado correctamente.")


    except Exception as e:
        print(f"Error: {e}")

# Menu para CRUD Stock
def menu_CRUD_Stock(opcion: str):
    """Printea el menu de CRUD Stock.

    Args:
      opcion (str): Opcion seleccionada.

    Raises:
      Cualquier excepcion dentro del bloque Try
    """
    try:
        if opcion == "1":  # Registrar movimiento
            print(" "*2, "REGISTRAR MOVIMIENTO", "\n")
            producto_id = int(input("ID producto: "))
            cantidad = int(input("Cantidad a mover (+ ingreso / - egreso): "))

            nuevo_stock = srv_stock.registrar_movimiento(producto_id, cantidad)
            print(f"Movimiento registrado. Stock actual: {nuevo_stock}")


        elif opcion == "2":  # Consultar stock
            print(" "*2, "CONSULTAR STOCK", "\n")
            producto_id = int(input("ID producto: "))

            stock = srv_stock.obtener_stock(producto_id)
            print(f"Stock actual del producto {producto_id}: {stock}")


        elif opcion == "3":  # Eliminar stock
            print(" "*2, "ELIMINAR STOCK", "\n")
            producto_id = int(input("ID producto: "))
            srv_stock.eliminar(producto_id)
            print("Stock eliminado correctamente.")

    except Exception as e:
        print(f"Error: {e}")

# Menu de CRUD Cotizacion Dolar
def menu_CRUD_Cotizacion_Dolar(opcion: str):
    """Printea el menu de CRUD Cotizacion Dolar.

    Args:
      opcion (str): Opcion seleccionada.

    Raises:
      Cualquier excepcion dentro del bloque Try
    """
    try:
        if opcion == "1":  # Registrar cotización
            print(" "*2, "REGISTRAR COTIZACION", "\n")
            valor = float(input("Valor cotización: "))
            tipo_id = int(input("ID tipo cotización: "))
            fecha_texto = input("Fecha (YYYY-MM-DD): ")

            fecha = datetime.date.fromisoformat(fecha_texto)
            tipo = srv_tipo.obtener(tipo_id)

            cotizacion = CotizacionDolar(valor, fecha, tipo)
            srv_cot.registrar_cotizacion(cotizacion)

            print("Cotización registrada correctamente.")


        elif opcion == "2":  # Obtener por tipo y fecha
            print(" "*2, "OBTENER POR TIPO Y FECHA", "\n")
            tipo_id = int(input("ID tipo cotización: "))
            fecha_texto = input("Fecha (YYYY-MM-DD): ")

            fecha = datetime.date.fromisoformat(fecha_texto)

            cotizacion = srv_cot.obtener(tipo_id, fecha)
            print(cotizacion)


        elif opcion == "3":  # Histórico
            print(" "*2, "HISTORICO", "\n")
            tipo_id = int(input("ID tipo cotización: "))

            historico = srv_cot.obtener_historico(tipo_id)

            for cotizacion in historico:
                print(cotizacion)

        elif opcion == "4":  # Actualizar
            print(" "*2, "ACTUALIZAR", "\n")
            valor = float(input("Nuevo valor cotización: "))
            tipo_id = int(input("ID tipo cotización: "))
            fecha_texto = input("Fecha (YYYY-MM-DD): ")

            fecha = datetime.date.fromisoformat(fecha_texto)
            tipo = srv_tipo.obtener(tipo_id)

            cotizacion = CotizacionDolar(valor, fecha, tipo)
            srv_cot.actualizar(cotizacion)

            print("Cotización actualizada correctamente.")

            retorno:str = input("\n" + "Volver al menu anterior (S/N) -> ")
            if retorno.upper() == "S":
              menu_CRUD("cotizacion_dolar")
            else:
              return()

        elif opcion == "5":  # Eliminar
            print(" "*2, "ELIMINAR", "\n")
            tipo_id = int(input("ID tipo cotización: "))
            fecha_texto = input("Fecha (YYYY-MM-DD): ")

            fecha = datetime.date.fromisoformat(fecha_texto)

            srv_cot.eliminar(tipo_id, fecha)
            print("Cotización eliminada correctamente.")


    except Exception as e:
        print(f"Error: {e}")

# Funcion que llama al menu correspondiente
def ejecutar_opcion(entidad: str, opcion: str):
    """Invoca al menu correspondiente para la entidad.

    Args:
      opcion (str): Opcion seleccionada para enviarla al menu correspondiente.

    Raises:
      Cualquier excepcion dentro del bloque Try
    """
    try:
        # CRUD BASICO
        if entidad in entidades_base:
            servicios = {
                "categorias": srv_cat,
                "proveedores": srv_prov,
                "monedas": srv_mon,
                "tipo_cotizacion": srv_tipo
            }

            menu_CRUD_basico(entidad, opcion, servicios[entidad])

        # PRODUCTOS
        elif entidad == "productos":
            menu_CRUD_Productos(opcion)
        # STOCK
        elif entidad == "stock":
            menu_CRUD_Stock(opcion)
        # COTIZACION
        elif entidad == "cotizacion_dolar":
            menu_CRUD_Cotizacion_Dolar(opcion)

        else:
            print("Entidad no válida.")

    except Exception as e:
        print(f"\n Error: {e}")

# Main general
def main():
  """Loop de opciones y menues.

    Args:
      opcion (str): Opcion seleccionada.
  """
  opciones_entidad = {"1":"categorias",
                      "2":"proveedores",
                      "3":"monedas",
                      "4":"tipo_cotizacion",
                      "5":"productos",
                      "6":"stock",
                      "7":"cotizacion_dolar",
                      "8":"salir"}
  while True:
    opcion_inicio = menu_INICIO()

    if opcion_inicio == "2":
      break

    while True:
      entidad = menu_ENTIDADES()

      if entidad == "0" or entidad == "8":
        break

      entidad_nombre = opciones_entidad.get(entidad)

      while True:
        opcion = menu_CRUD(entidad_nombre)

        if opcion == "0":
          break

        ejecutar_opcion(entidad_nombre, opcion)

        input("\n- Presione Enter para continuar - ")

