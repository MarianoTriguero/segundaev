# -*- coding: utf-8 -*-

from lxml import etree
from collections import OrderedDict
doc = etree.parse("restaurantes.xml")
raiz = doc.getroot()

#---------------------------------------------- XML ------------------------------------------
#Dado el nombre de una localidad, muestra los nombres, teléfonos y los e-mails de los locales que estén dentro de esa localidad
localidad = raw_input("Dame el nombre de una localidad:  ").upper()
locales = raiz.findall("row")
for local in locales:
	if local.find("municipality").text == localidad:
		print str(local.find("documentName").text) + " - " + str(local.find("phoneNumber").text) + " - " + str(local.find("email").text)

pausa=raw_input("\n --------------------------------------------------------- \n")
#Muestra solamente los locales que no tengan acceso para discapacitados dado un tipo de local y un dominio de correo electrónico.

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
	if local.find("restorationType").text == busqueda:
		if dominio in str(local.find("email").text):
			print local.find("documentName").text

pausa=raw_input("\n --------------------------------------------------------- \n")
#Cuenta cuantos locales con estrellas Michelín hay por cada población.

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
for local in locales:
	if local.find("room").text != None:
		if local.find("bodega").text != None:
			print "El local " + str(local.find("documentName").text) + " dispone de bodega propia y de habitaciones."
		else:
			print "El local " + str(local.find("documentName").text) + " dispone de habitaciones pero no de bodega propia."

#JSON
import json
f=open("alojamientos.json","r")
doc1 = json.load(f)
hotel = raw_input("Dame el nombre de un alojamiento: ")

pausa=raw_input("\n --------------------------------------------------------- \n")

#Dado el nombre de un hotel, mostrar su nombre, dirección, web y descripción en el siguiente formato:
#HOTEL: “NOMBRE HOTEL”
#SITUADA EN LA “LOCALIDAD” DE DONDE SEA EN LA CALLE/AVENIDA/PLAZA”
#“DESCRIPCION”
#VISITA “WEB DEL HOTEL” PARA MÁS INFORMACIÓN.
for aloj in doc1:
	if aloj["documentName"] == hotel:
		print "HOTEL: " + aloj["documentName"]
		print "SITUADA EN LA LOCALIDAD DE " + aloj["municipality"] + " EN LA DIRECCION " + aloj["address"]
		if aloj["documentDescription"] != None:
			print aloj["documentDescription"]
		else:
			print aloj["turismDescription"]
		if aloj["web"] != None:
			print "VISITA " + aloj["web"] + " PARA MAS INFORMACION"

pausa=raw_input("\n --------------------------------------------------------- \n")

#Dado el número de estrellas concreto, mostrar en el formato anterior los hoteles ordenados alfabéticamente por la localidad
#en la que se encuentran.
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
			print ciudad + " - " + str(hot["municipality"])

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

for rest in restaurantes:
	print rest.find("documentName").text





