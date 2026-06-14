import datetime
import functools

from sqlalchemy import text

from price_manager.database.connection import ConexionDB


class Auditoria:
  """Representa un registro de auditoría del sistema."""

  def __init__(
    self,
    accion: str,
    fecha: str,
    detalles: str,
    id: int | None = None,
  ):
    self.id = id
    self.accion = accion
    self.fecha = fecha
    self.detalles = detalles

  def __repr__(self) -> str:
    return (
      f"Auditoria(id={self.id}, "
      f"accion='{self.accion}', "
      f"fecha='{self.fecha}', "
      f"detalles='{self.detalles}')"
    )


class RepositorioAuditoria:
  """Repositorio para registrar y consultar auditorías."""

  def crear_tabla(self) -> None:
    """Crea la tabla de auditoría si no existe."""
    with ConexionDB() as cn:
      cn.execute(
        text("""
          CREATE TABLE IF NOT EXISTS Auditoria (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Accion TEXT NOT NULL,
            Fecha TEXT NOT NULL,
            Detalles TEXT NOT NULL
          )
        """)
      )

  def registrar(
    self,
    accion: str,
    detalles: str,
  ) -> Auditoria:
    """Registra una operación auditada."""
    self.crear_tabla()

    fecha = datetime.datetime.now().isoformat(
      timespec="seconds"
    )

    with ConexionDB() as cn:
      resultado = cn.execute(
        text("""
          INSERT INTO Auditoria (Accion, Fecha, Detalles)
          VALUES (:accion, :fecha, :detalles)
        """),
        {
          "accion": accion,
          "fecha": fecha,
          "detalles": detalles,
        },
      )

      auditoria_id = resultado.lastrowid

    return Auditoria(
      id=auditoria_id,
      accion=accion,
      fecha=fecha,
      detalles=detalles,
    )

  def listar_todos(self) -> list[Auditoria]:
    """Obtiene todos los registros de auditoría."""
    self.crear_tabla()

    with ConexionDB() as cn:
      resultado = cn.execute(
        text("""
          SELECT Id, Accion, Fecha, Detalles
          FROM Auditoria
          ORDER BY Id DESC
        """)
      )

      return [
        Auditoria(
          id=fila.Id,
          accion=fila.Accion,
          fecha=fila.Fecha,
          detalles=fila.Detalles,
        )
        for fila in resultado
      ]


def auditar_operacion(accion: str):
  """
  Decora una función para registrar su ejecución en auditoría.

  Args:
      accion:
          Nombre descriptivo de la operación auditada.

  Retorna:
      Decorador aplicable a funciones o métodos.
  """
  def decorador(funcion):
    @functools.wraps(funcion)
    def wrapper(*args, **kwargs):
      resultado = funcion(*args, **kwargs)

      detalles = (
        f"Funcion: {funcion.__name__}; "
        f"Args: {len(args)}; "
        f"Kwargs: {list(kwargs.keys())}"
      )

      RepositorioAuditoria().registrar(
        accion=accion,
        detalles=detalles,
      )

      return resultado

    return wrapper

  return decorador
