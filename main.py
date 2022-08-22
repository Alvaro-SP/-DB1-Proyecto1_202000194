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
import json
list = [];

#! ████████████████████████ WELCOME TO MY PROJECT ████████████████████████
#* █████████████████████TOMANDO EL ARCHIVO EXCEL:█████████████████████
rootPath = os.getcwd()
rootPath=rootPath+"/TestFile/";
loc = (rootPath+"calificacion.xlsx");
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    print(sheet.cell_value(i, 0),sheet.cell_value(i, 1))



#* █████████████████████ CONNECT WITH DATABASE:█████████████████████

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='2412',
                            db='db',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


#* █████████████████████ TOMAR LOS DATOS DEL EXCEL: █████████████████████
def ReadFromExcel(self):
    global list
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    for i in range(sheet.nrows):
        #print(sheet.cell_value(i, 0),sheet.cell_value(i, 1))
        list.append(EmailInfo(sheet.cell_value(i, 0),sheet.cell_value(i, 1)));
    print("Successfully retrieved all excel data");

#* █████████████████████ INSERT ALL DATA IN MYSQL MOTOR: █████████████████████
def BulkInsert(self,list):
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
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()

ReadFromExcel()
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
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)