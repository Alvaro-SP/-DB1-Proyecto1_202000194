from flask import Flask, jsonify, request
from flask_cors import CORS
import xlrd
import xlwt
import os
import pandas.io.sql as sql
from configparser import ConfigParser
import pymysql #pyMySQL is a python library for connecting to a MySQL database server from Python.This module has lots of features like it mad CRUD operations simple.
import pymysql.cursors
import pymysql
import pandas as pd
import json
list = [];

#! ████████████████████████ WELCOME TO MY PROJECT ████████████████████████
#* █████████████████████TOMANDO EL ARCHIVO EXCEL:█████████████████████
rootPath = os.getcwd()
rootPath=rootPath+"\\TestFile\\"
loc = (rootPath+"DB_Excel.xlsx")
#* █████████████████████ TOMAR LOS DATOS DEL EXCEL: █████████████████████

# Tomo en varios DataFrames to Lists
df_categoria=pd.read_excel(open(loc, 'rb'),sheet_name=0)
categoria = df_categoria.values.tolist()

df_cliente=pd.read_excel(open(loc, 'rb'),sheet_name=1)
cliente = df_cliente.values.tolist()

df_orden=pd.read_excel(open(loc, 'rb'),sheet_name=2)
orden = df_orden.values.tolist()

df_pais=pd.read_excel(open(loc, 'rb'),sheet_name=3)
pais = df_pais.values.tolist()

df_producto=pd.read_excel(open(loc, 'rb'),sheet_name=4)
producto = df_producto.values.tolist()

df_vendedor=pd.read_excel(open(loc, 'rb'),sheet_name=5)
vendedor = df_vendedor.values.tolist()


#* █████████████████████ CONNECT WITH DATABASE:█████████████████████

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='2412',
                            db='mydb')
                            # charset='utf8mb4',
                            # cursorclass=pymysql.cursors.DictCursro




#* █████████████████████ INSERT ALL DATA IN MYSQL MOTOR: █████████████████████
def BulkInsert():
    #create the table
    #! forma 1
    # mycursor = self.myConnection.cursor();
    #mycursor.execute("CREATE TABLE tbEmailList (tid INT AUTO_INCREMENT PRIMARY KEY, FullName VARCHAR(255), EmailId VARCHAR(255))"); 
    # query = "INSERT INTO tbEmailList (FullName, EmailId) VALUES ('{}', '{}')"
    # for obj in list:
    #     print( obj.FullName, obj.Email);
    #     formattedQuery=query.format(obj.FullName, obj.Email);
    #     mycursor.execute(formattedQuery);
    # self.myConnection.commit()
    # mycursor.close()

    try:
        with connection.cursor() as cursor:
            # Create a new record
                    #             INSERT INTO table_name
                    #               VALUES (value1, value2, value3, ...);
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO CATEGORIA ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO categoria (id_categoria,nombre) VALUES ({}, {})"
            for ca in categoria:
                fq=query.format(ca[0], "\'"+ca[1].replace("\'", "\'\'")+"\'");
                cursor.execute(fq)
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO pais ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Pais (id_pais,nombre) VALUES ({}, {})"
            for ca in pais:
                fq=query.format(ca[0], "\'"+ca[1].replace("\'", "\'\'")+"\'");
                cursor.execute(fq)
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO cliente ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Cliente (idCliente,nombre,apellido,direccion,telefono,tarjetaCredito,edad,salario,genero,id_pais) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
            for ca in cliente:
                fq=query.format(ca[0], "\'"+ca[1].replace("\'", "\'\'")+"\'","\'"+ca[2].replace("\'", "\'\'")+"\'", "\'"+ca[3].replace("\'", "\'\'")+"\'","\'"+str(ca[4])+"\'", "\'"+str(ca[5])+"\'",ca[6], ca[7],"\'"+ca[8].replace("\'", "\'\'")+"\'", ca[9]);
                cursor.execute(fq)
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO vendedor ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Vendedor (idVendedor,nombre,id_pais) VALUES ({}, {}, {})"
            for ca in vendedor:
                fq=query.format(ca[0],"\'"+ ca[1].replace("\'", "\'\'")+"\'",ca[2]);
                cursor.execute(fq)
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO orden ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Orden (id_orden,fecha_orden,id_cliente) VALUES ({}, {}, {})"
            for ca in orden:
                try:
                    a = str(ca[2]).replace("/","-").split()
                    # a = "STR_TO_DATE(\'"+a[0]+"\', \'%Y%m%d\')"  # TO_DATE(<string>, '<format>')
                    fq=query.format(ca[0], "\'"+a[0]+"\'", ca[3]);
                    cursor.execute(fq)
                except:
                    pass
            
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO producto ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Productos (id_producto,nombre,precio,categoria_id_categoria) VALUES ({}, {}, {}, {})"
            for ca in producto:
                fq=query.format(ca[0],"\'"+ ca[1].replace("\'", "\'\'")+"\'",ca[2], ca[3]);
                cursor.execute(fq)
            
            # ! ↓↓↓↓↓↓↓↓↓ INSERTANDO Productos_has_Orden ↓↓↓↓↓↓↓↓↓
            query = "INSERT INTO Productos_has_Orden (Orden_idOrden,linea_orden,Vendedor_idVendedor, Productos_id_producto,cantidad) VALUES ({}, {}, {}, {}, {})"
            for ca in orden:
                fq=query.format(ca[0], ca[1],ca[4], ca[5],ca[6]);
                cursor.execute(fq)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()


'''---COMENTARIO TOQUE---'''
app = Flask(__name__)
CORS(app)

#! ☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻ ENDPOINTS ☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻
#?  ██████████████████    1    █████████████████████
# 1. Mostrar el cliente que más ha comprado. Se debe de mostrar el id del cliente, 
# nombre, apellido, país y monto total.
@app.route('/1', methods=['GET'])
def uno():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
                SELECT Cliente.idCliente, Cliente.nombre, Cliente.apellido,
                Pais.nombre as Pais,
                SUM(Productos_has_Orden.cantidad * Productos.precio) as Monto_Total
                FROM Orden
                JOIN Cliente ON Orden.id_cliente = Cliente.idCliente
                JOIN Pais ON Pais.id_pais = Cliente.id_pais
                JOIN Productos_has_Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
                JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
                GROUP BY Orden.id_cliente  ORDER BY Monto_Total DESC LIMIT 1 ;
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()


#?  ██████████████████    2    █████████████████████
# 2. Mostrar el producto más y menos comprado. Se debe mostrar el id del
# producto, nombre del producto, categoría, cantidad de unidades y monto
# vendido.
@app.route('/2', methods=['GET'])
def dos():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
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
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID_PRODUCTO': fila[0], 'NOMBRE_PRODUCTO' : fila[1], 'NOMBRE_CATEGORIA' : fila[2], 'CANTIDAD' : fila[3], 'MONTO_TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'PRODUCTO_MAS_MENOS_COMPRADO': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 3. Mostrar a la persona que más ha vendido. Se debe mostrar el id del 
# vendedor, nombre del vendedor, monto total vendido.
@app.route('/3', methods=['GET'])
def tres():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql ='''
            SELECT
                Vendedor.idVendedor,
                Vendedor.nombre,
                SUM(Productos_has_Orden.cantidad * Productos.precio) as Monto_Total_Vendido
            FROM Productos_has_Orden
            JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
            JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
            GROUP BY Vendedor.idVendedor ORDER BY Monto_Total_Vendido DESC LIMIT 1;
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID_VENDEDOR': fila[0], 'NOMBRE' : fila[1], 'MONTO_TOTAL_VENDIDO' : fila[2]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 4. Mostrar el país que más y menos ha vendido. Debe mostrar el nombre del 
# país y el monto. (Una sola consulta).
@app.route('/4', methods=['GET'])
def cuatro():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
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
            )as c2;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 5. Top 5 de países que más han comprado en orden ascendente. Se le solicita 
# mostrar el id del país, nombre y monto total.
@app.route('/5', methods=['GET'])
def cinco():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
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
            )AS C5 ORDER BY Monto_Vendido ASC;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 6. Mostrar la categoría que más y menos se ha comprado. Debe de mostrar el 
# nombre de la categoría y cantidad de unidades. (Una sola consulta).
@app.route('/6', methods=['GET'])
def seis():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
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
                    JOIN categoria ON Productos.id_producto = categoria.id_categoria
                    GROUP BY name_category ORDER BY cant ASC LIMIT 1
                )
            )as C6;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 7. Mostrar la categoría más comprada por cada país. Se debe de mostrar el 
# nombre del país, nombre de la categoría y cantidad de unidades.
@app.route('/7', methods=['GET'])
def siete():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
            SELECT Pais.nombre, categoria.nombre,
            SUM(cantidad) as cantidad FROM Productos_has_Orden
            JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
            JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
            JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
            JOIN Pais ON Pais.id_pais = Vendedor.id_pais
            GROUP BY Pais.nombre, categoria.nombre ORDER BY Pais.nombre, cantidad DESC;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 8. Mostrar las ventas por mes de Inglaterra. Debe de mostrar el número del mes 
# y el monto.
@app.route('/8', methods=['GET'])
def ocho():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
            SELECT MONTH(Orden.fecha_orden) as mes,
            SUM(Productos_has_Orden.cantidad * Productos.precio) as monto
            FROM Productos_has_Orden
            JOIN Orden ON Orden.id_orden = Productos_has_Orden.Orden_idOrden
            JOIN Vendedor ON Vendedor.idVendedor = Productos_has_Orden.Vendedor_idVendedor
            JOIN Pais ON Pais.id_pais = Vendedor.id_pais
            JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
            WHERE Pais.nombre = 'Inglaterra'
            GROUP BY mes;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 9. Mostrar el mes con más y menos ventas. Se debe de mostrar el número de 
# mes y monto. (Una sola consulta).
@app.route('/9', methods=['GET'])
def nueve():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
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
            ) AS c9;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()
# 10.Mostrar las ventas de cada producto de la categoría deportes. Se debe de 
# mostrar el id del producto, nombre y monto.

@app.route('/10', methods=['GET'])
def diez():

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = '''
            SELECT (Productos.id_producto) AS id_producto, (Productos.nombre) AS nombre,
            ROUND(SUM((Productos_has_Orden.cantidad * Productos.precio)),2) AS monto FROM Productos_has_Orden
            JOIN Productos ON Productos_has_Orden.Productos_id_producto = Productos.id_producto
            JOIN categoria ON Productos.categoria_id_categoria = categoria.id_categoria
            WHERE categoria.nombre LIKE 'Deportes'
            GROUP BY id_producto;'''
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            templist = []
            for fila in result:
                atributos = {'ID': fila[0], 'NOMBRE' : fila[1], 'PAIS' : fila[2], 'TOTAL' : fila[3]}
                templist.append(atributos)
            return jsonify({'Cliente_Mas_Compra': templist})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
    finally:
        connection.close()



# @app.route('/paises')
# def show_paises():
#     try:
#         cursor=connection.cursor()
#         sql= "SELECT * FROM pais"
#         cursor.execute(sql)
#         datos = cursor.fetchall()
#         paises = []
#         for fila in datos:
#             pais = {'idPais': fila[0], 'nombrePais' : fila[1]}
#             paises.append(pais)
#         return jsonify({'Paises': paises})
#     except Exception as ex:
#         return jsonify({'Error': 'Error en la consulta'})


BulkInsert()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
