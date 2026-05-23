
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection


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
    engine = create_engine(
      f"sqlite:///{self.directorio_base}/{self.nombre_DB}",
      echo=True,
    )
    return engine.connect()

  def __enter__(self) -> Connection:
    self.conexion = self.conectarDB()
    self.transaccion = self.conexion.begin()
    return self.conexion

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type:
      self.transaccion.rollback()
    else:
      self.transaccion.commit()

    self.conexion.close()

try:

  with ConexionDB() as cn:

      print("Conexión iniciada.")

      # Una vez creadas las tablas y sus funciones, se llaman acá pasando por parametro a cn.

      raise ValueError("Hubo un error.")

except Exception as e:
  print(f"Error: {e}")
