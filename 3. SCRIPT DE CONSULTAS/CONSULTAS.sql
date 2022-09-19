--! 1. Mostrar el cliente que más ha comprado. Se debe de mostrar el id del cliente, 
--! nombre, apellido, país y monto total.

SELECT Cliente.idCliente, Cliente.nombre, Cliente.apellido,
Pais.nombre as Pais,
SUM(Productos_has_Orden.cantidad * Productos.precio) as Monto_Total
FROM Orden
JOIN Cliente ON Orden.id_cliente = Cliente.idCliente
JOIN Pais ON Pais.id_pais = Cliente.id_pais
JOIN Productos_has_Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
GROUP BY Orden.id_cliente  ORDER BY Monto_Total DESC LIMIT 1 ;



--! 2. Mostrar el producto más y menos comprado. Se debe mostrar el id del 
--! producto, nombre del producto, categoría, cantidad de unidades y monto 
--! vendido.


SELECT id_producto, nameProduct, nameCategoria, cantidad, monto FROM
(
    (
        -- EL MAS COMPRADO:
        SELECT
            Productos.id_producto as id_producto,
            Productos.nombre as nameProduct,
            categoria.nombre as nameCategoria,
            SUM(cantidad) as cantidad,
            ROUND(SUM(Productos_has_Orden.cantidad * Productos.precio),2) as monto
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON categoria.id_categoria = Productos.categoria_id_categoria
        GROUP BY id_producto ORDER BY monto ASC LIMIT 1
    )
    UNION ALL
    (
        -- EL MENOS COMPRADO:
        SELECT
            Productos.id_producto as id_producto,
            Productos.nombre as nameProduct,
            categoria.nombre as nameCategoria,
            SUM(cantidad) as cantidad,
            ROUND(SUM(Productos_has_Orden.cantidad * Productos.precio),2) as monto
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON categoria.id_categoria = Productos.categoria_id_categoria
        GROUP BY id_producto ORDER BY cantidad  desc LIMIT 1
    )
)as c2;

--! 3. Mostrar a la persona que más ha vendido. Se debe mostrar el id del 
--! vendedor, nombre del vendedor, monto total vendido.
SELECT
    Vendedor.idVendedor,
    Vendedor.nombre,
    SUM(Productos_has_Orden.cantidad * Productos.precio) as Monto_Total_Vendido
FROM Productos_has_Orden
JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
GROUP BY Vendedor.idVendedor ORDER BY Monto_Total_Vendido DESC LIMIT 1;

--! 4. Mostrar el país que más y menos ha vendido. Debe mostrar el nombre del 
--! país y el monto. (Una sola consulta).


SELECT nombre_pais, Monto_Vendido FROM
(
    (
        -- EL MAS VENDIDO:
        SELECT
            Pais.nombre as nombre_pais,
            SUM(cantidad * Productos.precio) as Monto_Vendido
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
        JOIN Pais ON Pais.id_pais = Vendedor.id_pais
        GROUP BY Pais.id_pais ORDER BY Monto_Vendido DESC LIMIT 1
    )
    UNION ALL
    (
        -- EL MENOS VENDIDO:
        SELECT
            Pais.nombre as nombre_pais,
            SUM(cantidad * Productos.precio) as Monto_Vendido
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
        JOIN Pais ON Pais.id_pais = Vendedor.id_pais
        GROUP BY Pais.id_pais ORDER BY Monto_Vendido ASC LIMIT 1
    )
)as c2;


--! 5. Top 5 de países que más han comprado en orden ascendente. Se le solicita 
--! mostrar el id del país, nombre y monto total.
SELECT * FROM
(
    (
        -- EL MAS VENDIDO:
        SELECT
            Pais.id_pais as id_Pais,
            Pais.nombre as nombre_pais,
            SUM(cantidad * Productos.precio) as Monto_Vendido
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
        JOIN Cliente ON Cliente.idCliente = Orden.id_cliente
        JOIN Pais ON Pais.id_pais = Cliente.id_pais
        GROUP BY Pais.id_Pais ORDER BY Monto_Vendido ASC LIMIT 5
    )
)AS C5 ORDER BY C5.Monto_Vendido ASC;


--! 6. Mostrar la categoría que más y menos se ha comprado. Debe de mostrar el 
--! nombre de la categoría y cantidad de unidades. (Una sola consulta).

SELECT name_category, cant FROM
(
    (
        -- EL QUE MAS HA COMPRADO
        SELECT categoria.nombre as name_category,
        SUM(Productos_has_Orden.cantidad) as cant
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
        GROUP BY name_category ORDER BY cant DESC LIMIT 1

    )
    UNION ALL
    (
        -- EL QUE MENOS HA COMPRADO
        SELECT categoria.nombre as name_category,
        SUM(Productos_has_Orden.cantidad) as cant
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
        GROUP BY name_category ORDER BY cant ASC LIMIT 1
    )
)as C6;

--! 7. Mostrar la categoría más comprada por cada país. Se debe de mostrar el 
--! nombre del país, nombre de la categoría y cantidad de unidades.


SELECT * FROM(
SELECT (Pais.nombre) AS pais, (categoria.nombre) AS categoria,
SUM(cantidad) AS cantidad FROM Productos_has_Orden
JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
JOIN Cliente ON Cliente.idCliente = Orden.id_cliente
JOIN Pais ON Pais.id_pais = Cliente.id_pais
GROUP BY Pais.nombre, categoria.nombre ORDER BY  cantidad DESC
) AS c7 GROUP BY c7.pais ORDER BY c7.cantidad ASC;


--! 8. Mostrar las ventas por mes de Inglaterra. Debe de mostrar el número del mes 
--! y el monto.

SELECT MONTH(Orden.fecha_orden) as mes,
SUM(Productos_has_Orden.cantidad * Productos.precio) as monto
FROM Productos_has_Orden
JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
JOIN Pais ON Pais.id_pais = Vendedor.id_pais
JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
WHERE Pais.nombre = 'Inglaterra'
GROUP BY mes;

--! 9. Mostrar el mes con más y menos ventas. Se debe de mostrar el número de 
--! mes y monto. (Una sola consulta).

SELECT mes, monto FROM
(
    (
        SELECT MONTH(Orden.fecha_orden) AS mes,
        ROUND(SUM((Productos_has_Orden.cantidad * Productos.precio)),2) AS monto 
        FROM Productos_has_Orden
        JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        GROUP BY mes ORDER BY monto DESC LIMIT 1
    )
    UNION ALL
    (
        SELECT MONTH(Orden.fecha_orden) AS mes,
        ROUND(SUM((Productos_has_Orden.cantidad * Productos.precio)),2) AS monto 
        FROM Productos_has_Orden
        JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        GROUP BY mes ORDER BY monto ASC LIMIT 1
    )
) AS c9;

--! 10.Mostrar las ventas de cada producto de la categoría deportes. Se debe de 
--! mostrar el id del producto, nombre y monto.

SELECT (Productos.id_producto) AS id_producto, (Productos.nombre) AS nombre,
ROUND(SUM((Productos_has_Orden.cantidad * Productos.precio)),2) AS monto FROM Productos_has_Orden
JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
WHERE categoria.nombre LIKE 'Deportes'
GROUP BY id_producto;
