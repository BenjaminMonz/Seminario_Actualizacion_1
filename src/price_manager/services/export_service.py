
import csv
import os

from price_manager.entities.entities import Producto


class ServicioExportacion:
  """Servicio para exportar productos a CSV."""

  def exportar_productos(
    self,
    productos: list[Producto],
    ruta_archivo: str,
  ) -> None:
    """Exporta productos a archivo CSV."""

    os.makedirs(
      os.path.dirname(ruta_archivo),
      exist_ok=True,
    )

    with open(
      ruta_archivo,
      mode="w",
      newline="",
      encoding="utf-8",
    ) as archivo:

      writer = csv.writer(archivo)

      writer.writerow([
        "id",
        "nombre",
        "descripcion",
        "precio",
        "moneda",
        "categoria",
        "proveedor",
      ])

      for producto in productos:
        writer.writerow([
          producto.id,
          producto.nombre,
          producto.descripcion,
          producto.precio.valor,
          producto.precio.moneda.nombre,
          producto.categoria.nombre,
          producto.proveedor.nombre,
        ])
