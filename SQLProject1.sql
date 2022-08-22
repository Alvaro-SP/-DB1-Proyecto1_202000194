-- ************* CREANDO TABLA DE CLIENTE *****************
 CREATE TABLE cliente(
	id int NOT NULL AUTO_INCREMENT,
    nombre varchar (100) NOT NULL,
    apellido varchar (100) NOT NULL,
    direccion varchar (100) NOT NULL,
    telefono int NOT NULL,
    tarjetaCredito int NOT NULL,
    edad int NOT NULL,
    genero varchar (100) NOT NULL,
    salArio varchar (100) NOT NULL,
    pais varchar (100) NOT NULL,
    PRIMARY KEY (id)
 );
 -- ************* CREANDO TABLA DE VENDEDOR *****************
  CREATE TABLE vendedor(
	id int NOT NULL AUTO_INCREMENT,
    nombre varchar (100) NOT NULL,
    apellido varchar (100) NOT NULL,
    pais varchar (100) NOT NULL,
    PRIMARY KEY (id)
 );
  -- ************* CREANDO TABLA DE ORDEN *****************
  CREATE TABLE orden(
	orden int NOT NULL AUTO_INCREMENT,
    fecha varchar (100) NOT NULL,
    id_vendedor int NOT NULL,
    id_cliente int NOT NULL,
    PRIMARY KEY (orden)
 );