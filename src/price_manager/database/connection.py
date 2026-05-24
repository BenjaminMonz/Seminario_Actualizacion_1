
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

# Clase encargada de la conexión con SQL
class ConexionDB:

  def __init__(
    self,
    nombre_base: str = "price_Manager.db",
    directorio: str = "/content/price_manager/src/price_manager/database",
  ):
    self.conexion = None
    self.transaccion = None
    self.nombre_DB = nombre_base
    self.directorio_base = directorio

  def conectarDB(self) -> Connection:
    """
      Establece una conexión con la base de datos.

      Utiliza SQLAlchemy para crear el engine y abrir
      una conexión.

      Returns: Objeto de conexión de SQLAlchemy.
    """
    engine = create_engine(
      f"sqlite:///{self.directorio_base}/{self.nombre_DB}",
      echo=True,
    )
    return engine.connect()

  def __enter__(self) -> Connection:
    """
      Método especial del context manager.

      Se ejecuta automáticamente al ingresar al bloque WITH.
      Abre la conexión e inicia una transacción.

      Returns: Conexión activa a la base de datos.
    """
    self.conexion = self.conectarDB()
    self.transaccion = self.conexion.begin()
    return self.conexion

  def __exit__(self, exc_type, exc_val, exc_tb):
    """
      Método especial del context manager.

      Se ejecuta automáticamente al finalizar el bloque WITH.

      Funcionalidad:
          - Si ocurre un error realiza un rollback.
          - Si no ocurre error hace un commit.
          - Luego, al finalizar, cierra la conexión.

      Args:
          exc_type: Tipo de excepción ocurrida.
          exc_val: Valor/mensaje de la excepción.
          exc_tb: Información del traceback de la excepción.
    """
    if exc_type:
      self.transaccion.rollback()
    else:
      self.transaccion.commit()

    self.conexion.close()

try:

  with ConexionDB() as cn:

      print("Conexión iniciada.")

      raise ValueError("Hubo un error.")

except Exception as e:
  print(f"Error: {e}")
