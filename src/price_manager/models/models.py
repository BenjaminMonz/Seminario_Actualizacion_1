
from sqlalchemy import text

from price_manager.database.connection import ConexionDB


def crear_tablas() -> None:
  """Crea manualmente las tablas relacionales del sistema."""

  with ConexionDB() as cn:

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Tipo_Cotizacion (
        Id INT,
        Nombre VARCHAR,
        CONSTRAINT PK_Tipo_Cotizacion_Id PRIMARY KEY (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Categoria (
        Id INT,
        Nombre VARCHAR,
        CONSTRAINT PK_Categoria_Id PRIMARY KEY (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Moneda (
        Id INT,
        Nombre VARCHAR,
        CONSTRAINT PK_Moneda_Id PRIMARY KEY (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Proveedor (
        Id INT,
        Nombre VARCHAR,
        Contacto VARCHAR,
        CONSTRAINT PK_Proveedor_Id PRIMARY KEY (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Producto (
        Id INT,
        Nombre VARCHAR,
        Descripcion VARCHAR,
        Precio FLOAT,
        Id_Moneda INT,
        Id_Categoria INT,
        Id_Proveedor INT,
        CONSTRAINT PK_Producto_Id PRIMARY KEY (Id),
        CONSTRAINT FK_Producto_Moneda
          FOREIGN KEY (Id_Moneda) REFERENCES Moneda (Id),
        CONSTRAINT FK_Producto_Categoria
          FOREIGN KEY (Id_Categoria) REFERENCES Categoria (Id),
        CONSTRAINT FK_Producto_Proveedor
          FOREIGN KEY (Id_Proveedor) REFERENCES Proveedor (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Precio_Historico (
        Id_Precio INT,
        Id_Producto INT,
        Valor FLOAT,
        Fecha DATE,
        Id_Moneda INT,
        CONSTRAINT PK_Precio_Historico_Id PRIMARY KEY (Id_Precio),
        CONSTRAINT FK_Precio_Historico_Producto
          FOREIGN KEY (Id_Producto) REFERENCES Producto (Id),
        CONSTRAINT FK_Precio_Historico_Moneda
          FOREIGN KEY (Id_Moneda) REFERENCES Moneda (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Stock (
        Id_Producto INT,
        Cantidad INT,
        CONSTRAINT PK_Stock_Id_Producto PRIMARY KEY (Id_Producto),
        CONSTRAINT FK_Stock_Id_Producto
          FOREIGN KEY (Id_Producto) REFERENCES Producto (Id)
      );
    """))

    cn.execute(text("""
      CREATE TABLE IF NOT EXISTS Cotizacion_Dolar (
        Valor FLOAT,
        Fecha DATE,
        Id_Tipo_Cotizacion INT,
        CONSTRAINT PK_Cotizacion_Dolar_Id_Tipo
          PRIMARY KEY (Id_Tipo_Cotizacion, Fecha),
        CONSTRAINT FK_Cotizacion_Dolar_Tipo_Cotizacion
          FOREIGN KEY (Id_Tipo_Cotizacion) REFERENCES Tipo_Cotizacion (Id)
      );
    """))
