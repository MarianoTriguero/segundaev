# -*- coding: utf-8 -*-

from lxml import etree
doc = etree.parse("restaurantes.xml")
raiz = doc.getroot()

#---------------------------------------------- XML ------------------------------------------
#Dado el nombre de una localidad, muestra los nombres, teléfonos y los e-mails de los locales que estén dentro de esa localidad
localidad = raw_input("Dame el nombre de una localidad:  ").upper()
locales = raiz.findall("row")
for local in locales:
	if local.find("municipality").text == localidad:
		print str(local.find("documentName").text) + " - " + str(local.find("phoneNumber").text) + " - " + str(local.find("email").text)

print " ----------------------------------------------------------------------- "
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

print " ------------------------------------------------------------------------ "
#Cuenta cuantos locales con estrellas Michelín hay por cada población.
localidades = []
for local in locales:
	#Si no está la localidad en localidades se agrega a la lista
	if local.find("municipality").text not in localidades:
		localidades.append([local.find("municipality").text,0])
	#Si tiene una estrella michelín, buscamos la localidad en la lista y actualizamos el valor del segundo campo
	if local.find("michelinStar").text == 1:
		for loc in localidades:
			if local.find("municipality").text == loc[0]:
				loc[1] = loc[1] + 1
