# -*- coding: utf-8 -*-

from lxml import etree
from random import randint
from collections import OrderedDict
doc = etree.parse("restaurantes.xml")
raiz = doc.getroot()

print "------------------------------ XML -----------------------------------\n"
#Dado el nombre de una localidad, muestra los nombres, teléfonos y los e-mails de los locales que estén dentro de esa localidad
print "Después de que introduzcas el nombre de una localidad, se mostrará el nombre, teléfono y el email de los locales de esa localidad\n"
localidad = raw_input("Dame el nombre de una localidad:  ").upper()
locales = raiz.findall("row")
for local in locales:
	if local.find("municipality").text == localidad:
		print str(local.find("documentName").text) + " - " + str(local.find("phoneNumber").text) + " - " + str(local.find("email").text)

pausa=raw_input("\n --------------------------------------------------------- \n")
#Muestra solamente los locales que no tengan acceso para discapacitados dado un tipo de local y un dominio de correo electrónico.
print "Se van a mostrar los locales que no tienen acceso para discapacitados introduciendo un tipo de local y la parte de un dominio de correo electrónico.\n"
#De esta manera obtengo todos los tipos de locales que hay para elegir
tiposrestaurante = []
for local in locales:
	tipo = local.find("restorationType").text
	if tipo not in tiposrestaurante:
		print tipo
		tiposrestaurante.append(tipo)

busqueda = raw_input("¿Qué tipo quieres buscar?\n")
dominio = raw_input("Con qué dominio de correo quieres buscar?\n")#@loquesea.loquesea
#Con esto buscamos el local indicándole el tipo y el dominio
for local in locales:
	if local.find("restorationType").text == busqueda and dominio in str(local.find("email").text) and local.find("accesibility").text == None:
		print local.find("documentName").text

pausa=raw_input("\n --------------------------------------------------------- \n")
#Cuenta cuantos locales con estrellas Michelín hay por cada población.
print "Se mostrarán cuantos locales con estrellas Michelín hay por cada población.\n"
localidades = []
for local in locales:
#	Si no está la localidad en localidades se agrega a la lista
	resp = False
	for loc in localidades:
		if local.find("municipality").text == loc[0]:
			resp = True
			#Si resulta que la ciudad está en la lista, accedemos a su variable y la aumentamos en uno
			if local.find("michelinStar").text != None:
				loc[1] = loc[1] + int(local.find("michelinStar").text)
	if resp == False or len(localidades) == 0:
		if local.find("michelinStar").text != None:
			localidades.append([local.find("municipality").text,int(local.find("michelinStar").text)])
		else:
			localidades.append([local.find("municipality").text,0])

#Mostramos la lista de localidades y sus respectivas estrellas Michelín.
for loc in localidades:
	if loc[1] != 0:
		print loc[0] + " - " + str(loc[1]) + " estrellas Michelín"

cont = raw_input("Presiona enter para continuar.")
pausa=raw_input("\n --------------------------------------------------------- \n")

#Busca cuales son los locales recomendados por guías turísticas e indica si estos tienen bodega privada o no.
print "Se mostrará a continuación los locales recomendados por guías turísticas y se mostrará si tienen bodega privada o no\n"
for local in locales:
	if local.find("room").text != None:
		if local.find("bodega").text != None:
			print "El local " + str(local.find("documentName").text) + " dispone de bodega propia y de habitaciones."
		else:
			print "El local " + str(local.find("documentName").text) + " dispone de habitaciones pero no de bodega propia."

pausa=raw_input("\n --------------------------JSON----------------------------- \n")
#JSON
import json
f=open("alojamientos.json","r")
doc1 = json.load(f)
hotel = raw_input("Dame el nombre de un alojamiento: ")

#Dado el nombre de un hotel, mostrar su nombre, dirección, web y descripción en el siguiente formato:
#HOTEL: “NOMBRE HOTEL”
#SITUADA EN LA “LOCALIDAD” DE DONDE SEA EN LA CALLE/AVENIDA/PLAZA”
#“DESCRIPCION”
#VISITA “WEB DEL HOTEL” PARA MÁS INFORMACIÓN.
print "Introduce el nombre de un hotel y se mostrará información relevante sobre el mismo.\n"
for aloj in doc1:
	if aloj["documentName"] == hotel:
		print "HOTEL: " + aloj["documentName"]
		print "SITUADA EN LA LOCALIDAD DE " + aloj["municipality"] + " EN LA DIRECCION " + aloj["address"]
		if aloj["turismDescription"] != None:
			print aloj["turismDescription"]
		else:
			print aloj["turismDescription"]
		if aloj["web"] != None:
			print "VISITA " + aloj["web"] + " PARA MAS INFORMACION"

pausa=raw_input("\n --------------------------------------------------------- \n")

#Dado el número de estrellas concreto, mostrar en el formato anterior los hoteles ordenados alfabéticamente por la localidad
#en la que se encuentran.
print "Cuando introduzcas un número de estrellas concreto, se mostraran los hoteles ordenados alfabéticamente en el formato del apartado anterior.\n"
estrellas = str(raw_input("Dame un número de estrellas: "))
hoteles = []
#Almacenamos los hoteles que coinciden con la categoría de entrada
for aloj in doc1:
	if str(aloj["category"]) == estrellas:
		hoteles.append(aloj)
#Ahora almacenamos las ciudades de los hoteles con la categoría de entrada
ciudades = []
for hot in hoteles:
	if str(hot["municipality"]) not in ciudades:
		ciudades.append(str(hot["municipality"]))

#Ahora se irá recorriendo la lista de alojamientos de forma ordenada sin modificar la original, de esta forma, al estar las
#ciudades ordenadas conseguiremos el orden que deseamos.
for ciudad in sorted(ciudades):
	for hot in hoteles:
		if ciudad == str(hot["municipality"]):
			print "HOTEL: " + hot["documentName"]
			print "SITUADA EN LA LOCALIDAD DE " + hot["municipality"] + " EN LA DIRECCION " + hot["address"]
			if hot["turismDescription"] != None:
				print hot["turismDescription"]
			else:
				print hot["turismDescription"]
			if hot["web"] != None:
				print "VISITA " + hot["web"] + " PARA MAS INFORMACION\n\
				\n"

pausa=raw_input("\n --------------------------------------------------------- \n")

#Necesitamos saber cual es el ranking de las mejores ciudades para hacer surf. Para ello contaremos las ciudades que tengan 
#más alojamientos con posibilidad de hacer surf y las ordenaremos en orden descendente.

surf = []
ciudadsurf = {}
#Buscamos los alojamientos con surfing
for aloj in doc1:
	if str(aloj["surfing"]) != "":
		surf.append(aloj)

#Contamos las ciudades con alojamientos con surfing
for s in surf:
	if str(s["municipality"]) not in ciudadsurf:
		ciudadsurf[str(s["municipality"])] = 1
	else:
		ciudadsurf[str(s["municipality"])] = ciudadsurf[str(s["municipality"])] + 1
			
#Con la ayuda de OrderedDict conseguimos obtener los datos de un diccionario ordenados

ciudadsurfsorted = OrderedDict(sorted(ciudadsurf.items(), key=lambda t: t[1], reverse=True))

for x in ciudadsurfsorted:
	print x + " - " + str(ciudadsurfsorted[x]) + " alojamientos habilitados para surf."

pausa=raw_input("\n --------------------------------------------------------- \n")

#XML + JSON

#Dado el nombre de un alojamiento, muestra los locales situados en la misma localidad que el alojamiento.

#Obtenemos la ciudad de alojamiento
entrada = raw_input("Dame el nombre de un alojamiento: ")
for x in doc1:
	if str(x["documentName"]) == entrada:
		objetivo = str(x["municipality"])

#Buscamos los locales que se encuentran en la ciudad
restaurantes = []
for local in locales:
	if str(local.find("municipality").text) == objetivo:
		restaurantes.append(local)

#Mostramos los locales
for rest in restaurantes:
	print rest.find("documentName").text

pausa=raw_input("\n --------------------------------------------------------- \n")

#Muestra 5 posibles combinaciones de alojamiento y restaurante para discapacitados.

#Buscamos los alojamientos con accesibilidad
alojdisc = []
for x in doc1:
	if str(x["accesibility"]) != "":
		alojdisc.append(x)

#Buscamos los locales con accesibilidad
restdisc = []
for local in locales:
	if local.find("accesibility").text != None:
		restdisc.append(local)

#Usamos números aleatorios para acceder a 5 locales y 5 alojamientos aleatoriamente y los mostramos
for x in xrange(0,5):
	print "Restaurante " + str(restdisc[randint(0,len(alojdisc) -1)].find("documentName").text) + " y alojamiento " + str(alojdisc[randint(0,len(alojdisc) - 1)]["documentName"])

pausa=raw_input("\n --------------------------------------------------------- \n")
		
#¿Cuántos alojamientos y restaurantes poseen la misma marca? Muestra solamente las marcas existentes
#en ambos archivos. Además debes de almacenar las marcas que no coincidan para después mostrarlas con el formato:
#“La marca (marca) no coincide en ambos archivos, los locales o restaurantes que la poseen son:
#(Objetos que poseen la marca)”.

#Buscamos las marcas en la lista de alojamientos
marcas = {}
for aloj in doc1:
	if str(aloj["marks"]) not in marcas and aloj["marks"] != None :
		marcas[str(aloj["marks"])] = 1
	elif aloj["marks"] != None:
		marcas[str(aloj["marks"])] = marcas[str(aloj["marks"])] + 1	
#Buscamos las marcas en la lista de restaurantes
for local in locales:
	if str(local.find("marks").text) not in marcas and local.find("marks").text != None:
		marcas[str(local.find("marks").text)] = 1
	elif local.find("marks").text != None:
		marcas[str(local.find("marks").text)] = marcas[str(local.find("marks").text)] + 1

#Mostramos las marcas y la cantidad de repeticiones
for x in marcas:
	print "Marca: " + x + " se repite " + str(marcas[x]) + " veces."




