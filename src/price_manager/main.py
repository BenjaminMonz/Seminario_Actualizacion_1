
from price_manager.models.models import crear_tablas
from price_manager.migrations.migrations import migrar_datos
from price_manager.ui.console import main as ejecutar_menu


desactivar_git_push = False


def inicializar_base_datos() -> None:
  """Inicializa tablas y datos base."""

  crear_tablas()
  migrar_datos()


def main(import_default_data: bool = False) -> None:
  """Ejecuta el sistema."""

  # Inicializar la base únicamente cuando se quiere importar datos de ejemplo
  if import_default_data:
    inicializar_base_datos()

  ejecutar_menu()


if __name__ == "__main__":
  main(import_default_data=False)
