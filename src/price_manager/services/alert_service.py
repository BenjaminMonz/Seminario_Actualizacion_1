import csv
import datetime
import os


class ServicioAlertasPrecio:
  """Servicio para generar alertas por diferencias de precios."""

  def generar_alertas(
    self,
    ruta_scraper: str,
    ruta_alertas: str,
    diferencia_minima: float,
  ) -> list[dict]:
    """
    Compara precios internos y web para generar alertas.

    Args:
        ruta_scraper:
            Ruta del CSV generado por el scraper.
        ruta_alertas:
            Ruta donde se guardará el CSV de alertas.
        diferencia_minima:
            Diferencia mínima absoluta para generar una alerta.

    Retorna:
        Lista de alertas generadas.
    """
    if not os.path.exists(ruta_scraper):
      raise FileNotFoundError("No existe el archivo del scraper.")

    alertas = []

    with open(
      ruta_scraper,
      mode="r",
      encoding="utf-8",
    ) as archivo:
      reader = csv.DictReader(archivo)

      for fila in reader:
        precio_interno = self._convertir_float(
          fila.get("precio_interno")
        )
        precio_web = self._convertir_float(
          fila.get("precio_web")
        )

        if precio_interno is None or precio_web is None:
          continue

        diferencia = precio_web - precio_interno

        if abs(diferencia) >= diferencia_minima:
          alertas.append({
            "producto": fila.get("producto_interno"),
            "precio_interno": precio_interno,
            "precio_web": precio_web,
            "diferencia": diferencia,
            "tipo_alerta": self._obtener_tipo_alerta(diferencia),
            "url_producto": fila.get("url_producto"),
            "fecha_extraccion": fila.get("fecha_extraccion"),
            "fecha_alerta": datetime.date.today().isoformat(),
          })

    self._guardar_alertas(ruta_alertas, alertas)

    return alertas

  def _guardar_alertas(
    self,
    ruta_alertas: str,
    alertas: list[dict],
  ) -> None:
    """Guarda las alertas generadas en un archivo CSV."""
    os.makedirs(
      os.path.dirname(ruta_alertas),
      exist_ok=True,
    )

    columnas = [
      "producto",
      "precio_interno",
      "precio_web",
      "diferencia",
      "tipo_alerta",
      "url_producto",
      "fecha_extraccion",
      "fecha_alerta",
    ]

    with open(
      ruta_alertas,
      mode="w",
      newline="",
      encoding="utf-8",
    ) as archivo:
      writer = csv.DictWriter(archivo, fieldnames=columnas)
      writer.writeheader()
      writer.writerows(alertas)

  def _convertir_float(self, valor: str | None) -> float | None:
    """Convierte un valor textual a float cuando es posible."""
    if valor in (None, "", "nan"):
      return None

    try:
      return float(valor)
    except ValueError:
      return None

  def _obtener_tipo_alerta(self, diferencia: float) -> str:
    """Clasifica la alerta según la diferencia de precios."""
    if diferencia > 0:
      return "PRECIO_WEB_MAYOR"

    return "PRECIO_WEB_MENOR"
