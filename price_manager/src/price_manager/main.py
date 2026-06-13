
from price_manager.preload_data.preload_data import precargar_datos
from price_manager.ui.console import main as ejecutar_menu


desactivar_git_push = False


def main(import_default_data: bool = False) -> None:
  """Ejecuta el sistema Price Manager.

  Args:
    import_default_data (bool): indica si deben precargarse los CSV.
  """
  if import_default_data:
    precargar_datos()

  ejecutar_menu()


if __name__ == "__main__":
  main(import_default_data=True)
