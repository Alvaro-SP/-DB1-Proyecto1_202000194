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
@app.route('/clienteMasCompra', methods=['GET'])
def clienteMasCompra():
    # global Pacientes
    # Datos=[]
    # for paciente in Pacientes:
    #     objeto = {
    #         'Nombre': paciente.getNombre(),
    #         'Apellido': paciente.getApellido(),
    #         'Fecha': paciente.getNacimiento(),
    #         'Sexo': paciente.getSexo(),
    #         'Username': paciente.getUsername(),
    #         'Contra': paciente.getContra()
    #     }
    #     Datos.append(objeto)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
    return(jsonify(Datos))


#! ☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻ ENDPOINTS ☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻☻
#?  ██████████████████    2    █████████████████████
# 2. Mostrar el producto más y menos comprado. Se debe mostrar el id del
# producto, nombre del producto, categoría, cantidad de unidades y monto
# vendido.
@app.route('/clienteMasCompra', methods=['GET'])
def ProductMaxMin():
    global Pacientes
    Datos=[]
    for paciente in Pacientes:
        objeto = {
            'Nombre': paciente.getNombre(),
            'Apellido': paciente.getApellido(),
            'Fecha': paciente.getNacimiento(),
            'Sexo': paciente.getSexo(),
            'Username': paciente.getUsername(),
            'Contra': paciente.getContra()
        }
        Datos.append(objeto)
    return(jsonify(Datos))
# 3. Mostrar a la persona que más ha vendido. Se debe mostrar el id del 
# vendedor, nombre del vendedor, monto total vendido.

# 4. Mostrar el país que más y menos ha vendido. Debe mostrar el nombre del 
# país y el monto. (Una sola consulta).

# 5. Top 5 de países que más han comprado en orden ascendente. Se le solicita 
# mostrar el id del país, nombre y monto total.

# 6. Mostrar la categoría que más y menos se ha comprado. Debe de mostrar el 
# nombre de la categoría y cantidad de unidades. (Una sola consulta).

# 7. Mostrar la categoría más comprada por cada país. Se debe de mostrar el 
# nombre del país, nombre de la categoría y cantidad de unidades.

# 8. Mostrar las ventas por mes de Inglaterra. Debe de mostrar el número del mes 
# y el monto.

# 9. Mostrar el mes con más y menos ventas. Se debe de mostrar el número de 
# mes y monto. (Una sola consulta).

# 10.Mostrar las ventas de cada producto de la categoría deportes. Se debe de 
# mostrar el id del producto, nombre y monto.


@app.route('/paises')
def show_paises():
    try:
        cursor=connection.cursor()
        sql= "SELECT * FROM pais"
        cursor.execute(sql)
        datos = cursor.fetchall()
        paises = []
        for fila in datos:
            pais = {'idPais': fila[0], 'nombrePais' : fila[1]}
            paises.append(pais)
        return jsonify({'Paises': paises})
    except Exception as ex:
        return jsonify({'Error': 'Error en la consulta'})
BulkInsert()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
    