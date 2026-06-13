
from price_manager.ui.console import main as menu_main
# Si el parametro se envia verdadero, se realizar la precarga
def main(import_default_data: bool = False):
    if import_default_data:
        from price_manager.preload_data.preload_data import precargar_datos
        precargar_datos()

    menu_main()


if __name__ == "__main__":
    main()
