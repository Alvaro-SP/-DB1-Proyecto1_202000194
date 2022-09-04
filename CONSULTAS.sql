--! 1. Mostrar el cliente que más ha comprado. Se debe de mostrar el id del cliente, 
--! nombre, apellido, país y monto total.

-- SELECT Cliente.idCliente, nombre, apellido, 
-- (SELECT nombre FROM Pais WHERE Cliente.id_pais = id_pais) as Pais, 
-- SUM(
--     (SELECT precio FROM Productos WHERE Orden.id_producto = Productos.id_producto)
--     *
--     cantidad
-- )  AS Monto_Total
-- FROM Cliente, Orden
-- WHERE Cliente.idCliente = Orden.id_cliente
-- GROUP BY Cliente.idCliente, nombre, apellido, id_pais
-- ORDER BY Monto_Total DESC LIMIT 1;



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


SELECT id_producto, nameProduct, nameCategoria, cantidad, Monto_Total FROM
(
    (
        -- EL MAS COMPRADO:
        SELECT
            Productos.id_producto as id_producto,
            Productos.nombre as nameProduct,
            categoria.nombre as nameCategoria,
            SUM(cantidad) as cantidad,
            SUM(cantidad * Productos.precio) as Monto_Total
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON categoria.id_categoria = Productos.categoria_id_categoria
        GROUP BY id_producto ORDER BY cantidad DESC LIMIT 1
    )
    UNION ALL
    (
        -- EL MENOS COMPRADO:
        SELECT
            Productos.id_producto as id_producto,
            Productos.nombre as nameProduct,
            categoria.nombre as nameCategoria,
            SUM(cantidad) as cantidad,
            SUM(Productos_has_Orden.cantidad * Productos.precio) as Monto_Total
        FROM Productos_has_Orden
        JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
        JOIN categoria ON categoria.id_categoria = Productos.categoria_id_categoria
        GROUP BY id_producto ORDER BY cantidad ASC LIMIT 1
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
        GROUP BY Pais.id_Pais ORDER BY Monto_Vendido DESC LIMIT 5
    )
)AS C5 ORDER BY Monto_Vendido ASC;


--! 6. Mostrar la categoría que más y menos se ha comprado. Debe de mostrar el 
--! nombre de la categoría y cantidad de unidades. (Una sola consulta).


--! 7. Mostrar la categoría más comprada por cada país. Se debe de mostrar el 
--! nombre del país, nombre de la categoría y cantidad de unidades.


--! 8. Mostrar las ventas por mes de Inglaterra. Debe de mostrar el número del mes 
--! y el monto.


--! 9. Mostrar el mes con más y menos ventas. Se debe de mostrar el número de 
--! mes y monto. (Una sola consulta).


--! 10.Mostrar las ventas de cada producto de la categoría deportes. Se debe de 
--! mostrar el id del producto, nombre y monto.
