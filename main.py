# -*- coding: utf-8 -*-

import unicodedata
import math
import string
import random
from Pelicula import Pelicula
from RegistroIndiceCodigo import RegistroIndiceCodigo
from RegistroIndicePalabra import RegistroIndicePalabra

vectorPeliculas = []
indiceCodigo = []
indicePalabras = []


# Función para ordenar el índice
def ordenarIndice(indice, bandera):
    if len(indice) == 0:
        return
    else:

        if bandera:
            indice.sort(key=lambda x: x.codigo, reverse=False)
        else:
            indice.sort(key=lambda x: x.palabra.lower(), reverse=False)


# Función para añadir una película
def anadirPelicula():

    # Pedir código de película
    while True:
        try:
            codigo = int(input("\nCódigo: "))
        except ValueError:
            print("Debes escribir un código.")
            continue

        if codigo < 0 or codigo > 99999:
            print("Debes escribir un número positivo menor a 5 dígitos.")
            continue
        elif busquedaBinariaCodigo(indiceCodigo, 0, len(indiceCodigo) - 1, codigo):
            print("Ya existe una película con ese código, intente con otro.")
            continue
        else:
            break

    # Pedir título de película
    while True:
        try:
            titulo = input("\nTítulo: ")
        except ValueError:
            print("Debes escribir un título.")
            continue

        if len(titulo) > 30 or len(titulo) < 1:
            print("El título de la película no puede tener más de 30 caracteres o ser vacío.")
            continue
        else:
            break

    # Pedir costo de alquiler de la película
    while True:
        try:
            alquiler = int(input("\nAlquiler: "))
        except ValueError:
            print("Debes escribir un costo de alquiler.")
            continue

        if alquiler < 0 or alquiler > 99999999:
            print("Debes escribir un número positivo menor a 8 dígitos.")
            continue
        else:
            break

    # Crear película y agregar al vector de películas
    nuevaPelicula = Pelicula(codigo, titulo, alquiler)
    vectorPeliculas.append(nuevaPelicula)

    # Guardar película en el índice de códigos de película
    nuevoRegistroCodigo = RegistroIndiceCodigo(
        len(vectorPeliculas)-1, nuevaPelicula.codigo)
    indiceCodigo.append(nuevoRegistroCodigo)
    ordenarIndice(indiceCodigo, True)

    # Guardar película en el índice de palabras de la película
    palabras = titulo.split()

    for palabra in palabras:
        nuevoRegistroPalabra = RegistroIndicePalabra(
            len(vectorPeliculas)-1, palabra)
        indicePalabras.append(nuevoRegistroPalabra)
        ordenarIndice(indicePalabras, False)

    print("\nSu película se ha agregado correctamente.")


# Función para obtener la película después de buscarla en el índice
def obtenerPelicula(index):
    pelicula = vectorPeliculas[index]
    if pelicula.existe == False:
        return
    else:
        return pelicula


# Función de búsqueda binaria por código
def busquedaBinariaCodigo(indice, izquierda, derecha, codigo):

    if derecha >= izquierda:

        mitad = izquierda + (derecha - izquierda) // 2

        if indice[mitad].codigo == codigo:
            return obtenerPelicula(indice[mitad].indice)
        elif indice[mitad].codigo > codigo:
            return busquedaBinariaCodigo(indice, izquierda, mitad-1, codigo)
        else:
            return busquedaBinariaCodigo(indice, mitad + 1, derecha, codigo)
    else:
        return


# Función para eliminación booleana de película
def eliminarPelicula():

    while True:
        try:
            codigo = int(
        input("\nIngrese el código de la pelicula que desea eliminar: "))
        except ValueError:
            print("Debes escribir un código.")
            continue

        if codigo < 0 or codigo > 99999:
            print("Debes escribir un número positivo menor a 5 dígitos.")
            continue
        else:
            break
    

    derecha = len(indiceCodigo) - 1

    pelicula = busquedaBinariaCodigo(indiceCodigo, 0, derecha, codigo)

    if pelicula:
        if pelicula.alquilada:
            print("No se puede eliminar esta película, porque está alquilada.")
        else:
            pelicula.existe = False
            print("La película se ha eliminado con éxito.")
    else:
        print("La película no existe o no está disponible.")


# Función para buscar una película por su código y saber si está alquilada
def buscarPeliculaCodigo():

    while True:
        try:
            codigo = int(input("\nIngrese el código de la película que desea buscar: "))
        except ValueError:
            print("Debes escribir un código.")
            continue

        if codigo < 0 or codigo > 99999:
            print("Debes escribir un número positivo menor a 5 dígitos.")
            continue
        else:
            break

    derecha = len(indiceCodigo) - 1
    pelicula = busquedaBinariaCodigo(indiceCodigo, 0, derecha, codigo)

    if pelicula:
        print("\nTítulo: " + pelicula.titulo)

        if pelicula.alquilada:
            print("La película está alquilada por el socio #" + str(pelicula.socio))
        else:
            print("La película no está alquilada.")
    else:
        print("La película no existe.")


# Función de búsqueda binaria por palabra
def busquedaBinariaPalabra(indice, izquierda, derecha, palabra):

    palabraNormalizada = ''.join(x for x in unicodedata.normalize('NFKD', palabra) if x in string.ascii_letters).lower()

    if derecha >= izquierda:

        mitad = izquierda + (derecha - izquierda) // 2
        palabraNormalizadaIndice = ''.join(x for x in unicodedata.normalize('NFKD', indice[mitad].palabra) if x in string.ascii_letters).lower()
        

        if palabraNormalizadaIndice == palabraNormalizada:

            peliculasPalabra = [indice[mitad].indice]

            izquierdaMitad = mitad - 1
            derechaMitad = mitad + 1

            while izquierdaMitad >= 0:
                palabraNormalizadaIndiceIzquierda = ''.join(x for x in unicodedata.normalize('NFKD', indice[izquierdaMitad].palabra) if x in string.ascii_letters).lower()
                if palabraNormalizadaIndiceIzquierda == palabraNormalizada:
                    peliculasPalabra.append(indice[izquierdaMitad].indice)

                izquierdaMitad = izquierdaMitad - 1

            while derechaMitad < len(indice):
                palabraNormalizadaIndiceDerecha = ''.join(x for x in unicodedata.normalize('NFKD', indice[derechaMitad].palabra) if x in string.ascii_letters).lower()
                if (palabraNormalizadaIndiceDerecha == palabraNormalizada):
                    peliculasPalabra.append(indice[derechaMitad].indice)

                derechaMitad = derechaMitad + 1

            return peliculasPalabra

        elif palabraNormalizadaIndice > palabraNormalizada:
            return busquedaBinariaPalabra(indice, izquierda, mitad - 1, palabra)
            
        else:
            return busquedaBinariaPalabra(indice, mitad + 1, derecha, palabra)

    else:
        return


# Función para buscar una película por una palabra y saber si está alquilada
def buscarPeliculaPalabra():

    palabra = input("\nIngrese una (1) palabra de la película que desea buscar: ")
    derecha = len(indicePalabras) - 1
    peliculas = busquedaBinariaPalabra(indicePalabras, 0, derecha, palabra)
    
    apuntador = -1

    if peliculas:
        for indice in peliculas:

            indiceAnterior = -1

            if apuntador > 0:
                indiceAnterior = peliculas[apuntador]

            apuntador = apuntador + 1

            if indiceAnterior != indice:
                pelicula = obtenerPelicula(indice)

                print("\nTítulo: " + pelicula.titulo)

                if pelicula.alquilada:
                    print("La película está alquilada por el socio #" +
                        str(pelicula.socio))
                else:
                    print("La película no está alquilada.")
    else:
        print("No existe ninguna película con esa palabra.")


# Función para alquilar pelicula
def alquilarPelicula():

    while True:
        try:
            codigo = int(input("\nIngrese el código de la pelicula que desea alquilar: "))
        except ValueError:
            print("Debes escribir un código.")
            continue

        if codigo < 0 or codigo > 99999:
            print("Debes escribir un número positivo menor a 5 dígitos.")
            continue
        else:
            break

    
    derecha = len(indiceCodigo) - 1
    pelicula = busquedaBinariaCodigo(indiceCodigo, 0, derecha, codigo)

    if pelicula:
        if pelicula.alquilada == True:
            print("Disculpe, esa película ya está alquilada.")

        else:

            while True:
                try:
                    socio = int(input("\nIngrese el número del socio: "))
                except ValueError:
                    print("Debes escribir un número de socio.")
                    continue

                if socio < 0 or socio > 99999:
                    print("Debes escribir un número de socio menor a 5 dígitos.")
                    continue
                else:
                    break

            pelicula.socio = socio
            pelicula.alquilada = True

            print("La película ha sido alquilada correctamente.")

    else:
        print("Esa película no existe o no está disponible.")


# Función para devolver una película
def devolverPelicula():

    while True:
        try:
            codigo = int(input("\nIngrese el código de la película a devolver: "))
        except ValueError:
            print("Debes escribir un código.")
            continue

        if codigo < 0 or codigo > 99999:
            print("Debes escribir un número positivo menor a 5 dígitos.")
            continue
        else:
            break
    
    derecha = len(indiceCodigo) - 1
    pelicula = busquedaBinariaCodigo(indiceCodigo, 0, derecha, codigo)

    if pelicula:

        if pelicula.alquilada == False:
            print("Esta película no está alquilada.")

        else:
            pelicula.alquilada = False
            pelicula.socio = 0
            print("La película ha sido devuelta correctamente.")
    else:
        print("La película con ese código no existe.")


# Función para compactar y reindexar la películas
def compactarPeliculas():

    peliculasCompacto = []
    indiceCodigo = []
    indicePalabras = []
    global vectorPeliculas

    for pelicula in vectorPeliculas:
        if pelicula.existe:
            peliculasCompacto.append(pelicula)

            # Guardar película en el índice de códigos de película
            nuevoRegistroCodigo = RegistroIndiceCodigo(
                len(peliculasCompacto)-1, pelicula.codigo)
            indiceCodigo.append(nuevoRegistroCodigo)
            ordenarIndice(indiceCodigo, True)

            # Guardar película en el índice de palabras de la película
            palabras = pelicula.titulo.split()

            for palabra in palabras:
                nuevoRegistroPalabra = RegistroIndicePalabra(
                    len(peliculasCompacto)-1, palabra)
                indicePalabras.append(nuevoRegistroPalabra)
                ordenarIndice(indicePalabras, False)

    vectorPeliculas = peliculasCompacto

# Función para guardar las películas en un txt cuando termina el programa


def guardarTxt():
    archivo = open("BaseDeDatos.txt", "w+")

    for pelicula in vectorPeliculas:
        archivo.write(str("codigo\n"))
        archivo.write(str(pelicula.codigo) + "\n")
        archivo.write("titulo\n")
        archivo.write(pelicula.titulo + "\n")
        archivo.write("socio\n")
        archivo.write(str(pelicula.socio) + "\n")
        archivo.write("alquiler\n")
        archivo.write(str(pelicula.alquiler) + "\n")
        archivo.write("alquilada\n")
        archivo.write(str(pelicula.alquilada) + "\n")
        archivo.write("<3 <3 <3 <3 <3 <3 <3 <3 <3 <3\n")

    archivo.close()


# Función para leer el archivo txt al iniciar el programa
def leerTxt():

    archivo = open("BaseDeDatos.txt", "r")
    documento = []

    codigo = ""
    titulo = ""
    alquiler = ""
    socio = ""
    existe = ""
    alquilada = ""

    for texto in archivo:
        documento.append(texto)

    for index in range(len(documento)):

        if documento[index] == "codigo\n":
            codigo = documento[index+1]
            codigo = codigo[:-1]
            codigo = int(codigo)

        elif documento[index] == "titulo\n":
            titulo = documento[index+1]
            titulo = titulo[:-1]

        elif documento[index] == "alquiler\n":
            alquiler = documento[index+1]
            alquiler = alquiler[:-1]
            alquiler = int(alquiler)

        elif documento[index] == "socio\n":
            socio = documento[index+1]
            socio = socio[:-1]
            socio = int(socio)

        elif documento[index] == "alquilada\n":
            alquilada = documento[index+1]
            alquilada = alquilada[:-1]
            if alquilada == "True":
                alquilada = True
            else:
                alquilada = False

        elif documento[index] == "<3 <3 <3 <3 <3 <3 <3 <3 <3 <3\n":
            nuevaPelicula = Pelicula(codigo, titulo, alquiler,
                                socio, True, alquilada)
            vectorPeliculas.append(nuevaPelicula)

            # Guardar película en el índice de códigos de película
            nuevoRegistroCodigo = RegistroIndiceCodigo(
                len(vectorPeliculas)-1, nuevaPelicula.codigo)
            indiceCodigo.append(nuevoRegistroCodigo)
            ordenarIndice(indiceCodigo, True)

            # Guardar película en el índice de palabras de la película
            palabras = titulo.split()

            for palabra in palabras:
                nuevoRegistroPalabra = RegistroIndicePalabra(
                    len(vectorPeliculas)-1, palabra)
                indicePalabras.append(nuevoRegistroPalabra)
                ordenarIndice(indicePalabras, False)

        else:
            continue


# MÉTODO MAIN DEL PROYECTO
starter = True


while starter == True:

    print("\n\n-------------------------------------------|    INVENTARIO BLOCKBUSTER    |--------------------------------------------\n\n")
    print("     Este proyecto fue elaborado por Nicole Brito y Giselle Ferreira, estudiantes de la Universidad Metropolitana, \n     en la asignatura de Organización del Computador, dictada por el profesor Rafael Matienzo.\n")
    print("     Este es un programa que implementa un inventario de peliculas para una tienda de alquiler de videos tipo\n     Blockbuster.\n\n")

    leerTxt()
    seguirEjecutando = True

    while seguirEjecutando:

        print("-----------------------------------------------------------------------------------------------------------------------\n")
        print("MENÚ:\n")
        print("1 - Añadir película")
        print("2 - Eliminar película")
        print("3 - Consultar película por código")
        print("4 - Consultar película por palabra")
        print("5 - Alquilar película")
        print("6 - Devolver película")
        print("7 - Compactar base de datos de películas")
        print("8 - Finalizar programa")

        while True:
            try:
                opcion = int(input("\nIngrese el número de la función que desea: "))
            except ValueError:
                print("Debes escribir una opción válida.")
                continue

            if opcion < 1 or opcion > 8:
                print("Debes escribir una opción válida.")
                continue
            else:
                break

        if opcion == 1:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            anadirPelicula()
        elif opcion == 2:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            eliminarPelicula()
        elif opcion == 3:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            buscarPeliculaCodigo()
        elif opcion == 4:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            buscarPeliculaPalabra()
        elif opcion == 5:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            alquilarPelicula()
        elif opcion == 6:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            devolverPelicula()
        elif opcion == 7:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")

            while True:
                try:
                    print("\nADVERTENCIA: Al compactar la tabla el programa se cerrará porque no pueden haber usuarios usando \nla base de datos durante el proceso de compactado.")
                    seguro = int(input("¿Está seguro que desea compactar la tabla? \n\n1 - NO\n2 - SI \n\nIngrese su respuesta: "))
                except ValueError:
                    print("Debes escribir una opción válida.")
                    continue

                if seguro < 1 or seguro > 2:
                    print("Debes escribir una opción válida.")
                    continue
                else:
                    if seguro == 2:
                        seguirEjecutando = False
                        starter = False
                        print("\n\n-----------------------------------------------------------------------------------------------------------------------\n")
                        print("Gracias por usar Blockbuster.")
                        compactarPeliculas()
                        guardarTxt()
                    break

            compactarPeliculas()
        
        
        if opcion != 8 and opcion != 7: 
            while True:
                try:
                    print("\n\n-----------------------------------------------------------------------------------------------------------------------\n")
                    seguir = int(input("¿Desea seguir ejecutado el programa? \n\n1 - SI\n2 - NO \n\nIngrese su respuesta: "))
                except ValueError:
                    print("Debes escribir una opción válida.")
                    continue

                if seguir < 1 or seguir > 2:
                    print("Debes escribir una opción válida.")
                    continue
                else:
                    if seguir == 2:
                        seguirEjecutando = False
                        starter = False
                        print("\n\n-----------------------------------------------------------------------------------------------------------------------\n")
                        print("Gracias por usar Blockbuster.")
                        compactarPeliculas()
                        guardarTxt()
                    break

        
        if opcion == 8:
            print("\n-----------------------------------------------------------------------------------------------------------------------\n")
            print("Gracias por usar Blockbuster.")
            compactarPeliculas()
            guardarTxt()
            seguirEjecutando = False
            starter = False

        



        

        
