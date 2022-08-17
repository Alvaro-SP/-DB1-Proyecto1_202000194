from flask import Flask, jsonify, request
from flask_cors import CORS
import xlrd
import xlwt
import os
import pandas.io.sql as sql
from configparser import ConfigParser
import mysql.connector
import json
#! ████████████████████████ WELCOME TO MY PROJECT ████████████████████████
#*TOMANDO EL ARCHIVO EXCEL:
rootPath = os.getcwd()
rootPath=rootPath+"/TestFile/";
loc = (rootPath+"calificacion.xlsx");
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    print(sheet.cell_value(i, 0),sheet.cell_value(i, 1))

#* TOMAR LOS DATOS DEL EXCEL:
def ReadFromExcel(self):
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    list = [];
    for i in range(sheet.nrows):
        #print(sheet.cell_value(i, 0),sheet.cell_value(i, 1))
        list.append(EmailInfo(sheet.cell_value(i, 0),sheet.cell_value(i, 1)));
    print("Successfully retrieved all excel data");

#* INSERT ALL DATA IN MYSQL MOTOR:
def BulkInsert(self,list):
    mycursor = self.myConnection.cursor();
    #create the table
    #mycursor.execute("CREATE TABLE tbEmailList (tid INT AUTO_INCREMENT PRIMARY KEY, FullName VARCHAR(255), EmailId VARCHAR(255))"); 
    query = "INSERT INTO tbEmailList (FullName, EmailId) VALUES ('{}', '{}')"
    for obj in list: 
        print( obj.FullName, obj.Email);
        formattedQuery=query.format(obj.FullName, obj.Email);
        mycursor.execute(formattedQuery);
    self.myConnection.commit()
    mycursor.close()


'''---COMENTARIO TOQUE---'''
app = Flask(__name__)
CORS(app)
# 1. Mostrar el cliente que más ha comprado. Se debe de mostrar el id del cliente, 
# nombre, apellido, país y monto total.

# 2. Mostrar el producto más y menos comprado. Se debe mostrar el id del 
# producto, nombre del producto, categoría, cantidad de unidades y monto 
# vendido.

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

#██████████████████   PACIENTES    █████████████████████
#OBTENER LOS PACIENTES
@app.route('/Pacientes', methods=['GET'])
def getPacientes():    
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

#POSTEAR LOS PACIENTES DESDE EL LOGIN U OTRO
@app.route('/Pacientes', methods=['POST'])
def AgregarPaciente():
    global Pacientes
    nombre = request.json['Nombre']
    nombre=nombre.replace(" ","")
    apellido= request.json['Apellido']
    nacimiento = request.json['Fecha']
    sexo = request.json['Sexo']
    username = request.json['Usuario']
    contra = request.json['Contraseña']

    nuevo = Paciente(nombre,apellido,nacimiento,sexo,username,contra)
    Pacientes.append(nuevo)
    return jsonify({'Mensaje':'Se agrego el Paciente exitosamente',})
 
#OBTENER UN DATO DE LOS PACIENTES   
@app.route('/Pacientes/login/<string:username>', methods=['GET'])
def ObtenerPacient(username): 
    global Pacientes  
    for paciente in Pacientes:
        if paciente.getUsername() == username :
            objeto = {
            'Nombre': paciente.getNombre(),
            'Apellido': paciente.getApellido(),
            'Fecha': paciente.getNacimiento(),
            'Sexo': paciente.getSexo(),
            'Username': paciente.getUsername(),
            'Contra': paciente.getContra(),
            'tipo':0
            }
            return(jsonify(objeto))     
    salida = { "Mensaje": "No existe el usuario con ese nombre"}

    return(jsonify(salida))

#OBTENER UN DATO DE LOS PACIENTES LOGEADOS
@app.route('/Pacientes/<string:nombre>', methods=['GET'])
def ObtenerUserPaciente(nombre): 
    global Pacientes
    for paciente in Pacientes:
        if paciente.getNombre() == nombre:
            objeto = {
            'Nombre': paciente.getNombre(),
            'Apellido': paciente.getApellido(),
            'Fecha': paciente.getNacimiento(),
            'Sexo': paciente.getSexo(),
            'Username': paciente.getUsername(),
            'Contra': paciente.getContra()
            }
            return(jsonify(objeto))     
    salida = { "Mensaje": "No existe el usuario con ese nombre"}

    return(jsonify(salida))

#ACTUALIZAR UN PACIENTE 
@app.route('/Pacientes/<string:nombre>', methods=['PUT'])
def ActualizarPaciente(nombre):    
    global Pacientes
    for i in range(len(Pacientes)):
        if nombre == Pacientes[i].getNombre():
            Pacientes[i].setNombre(request.json['nombre'])
            Pacientes[i].setApellido(request.json['apellido'])
            Pacientes[i].setNacimiento(request.json['fecha'])
            Pacientes[i].setSexo(request.json['sexo'])
            Pacientes[i].setUsername(request.json['usuario'])
            Pacientes[i].setContra(request.json['contra'])
            return jsonify({'Mensaje':'Se actualizo el dato exitosamente'})
    # Si llega a este punto, quiere decir que salio del for
    return jsonify({'Mensaje':'No se encontro el dato para actualizar'})

#ELIMINAR UN PACIENTE 
@app.route('/Pacientes/<string:nombre>', methods=['DELETE'])
def EliminarPersona(nombre):
    global Pacientes    
    for i in range(len(Pacientes)):        
        if nombre == Pacientes[i].getNombre():            
            del Pacientes[i]            
            return jsonify({'Mensaje':'Se elimino el dato exitosamente'})           
    return jsonify({'Mensaje':'No se encontro el dato para eliminar'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)