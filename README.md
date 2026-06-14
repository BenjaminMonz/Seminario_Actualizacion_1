# Price Manager - Sprint 3

## Descripción

Price Manager es una aplicación desarrollada en Python para la gestión de productos, precios, stock y cotizaciones de moneda. En este Sprint se incorporan funcionalidades de scraping, generación de alertas de precios, reportes en Excel y auditoría de operaciones.

## Funcionalidades implementadas

### Ejercicio 1
- Preparación de estructura del Sprint 3.
- Configuración de carpetas y dependencias necesarias.

### Ejercicio 2
- Carga de información desde archivos SQL.
- Inicialización de datos en base SQLite.

### Ejercicio 3
- Implementación del scraper `StarComputacionSpider`.
- Extracción de:
  - Precio web.
  - URL de imagen.
  - Formas de pago.
  - Descripción detallada.
- Implementación de Loaders.
- Implementación de Pipelines.

### Ejercicio 4
- Comparación entre precios internos y precios obtenidos mediante scraping.
- Generación de alertas de diferencias de precio.
- Exportación de alertas a CSV.

### Ejercicio 5
- Generación de reporte Excel con:
  - Producto.
  - Precio interno.
  - Precio web.
  - Diferencia.
  - Fecha de extracción.

### Ejercicio 6
- Implementación de auditoría mediante decoradores.
- Registro de:
  - Acción.
  - Fecha.
  - Detalles.
- Auditoría de operaciones relevantes del sistema.

### Ejercicio 7
- Incorporación de nuevas opciones de menú:
  - Ejecutar scraping.
  - Generar reporte.
  - Ver historial de auditoría.

## Tecnologías utilizadas

- Python
- SQLite
- SQLAlchemy
- Scrapy
- Pandas
- OpenPyXL

## Estructura principal

```text
price_manager/
├── exports/
├── src/
│   └── price_manager/
│       ├── database/
│       ├── entities/
│       ├── repositories/
│       ├── reports/
│       ├── scraper/
│       ├── services/
│       └── ui/
├── README.md
└── CHANGELOG.md
