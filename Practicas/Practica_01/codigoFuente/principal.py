#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from analizadorEstructura import AnalizadorInstruccion

def main():
    root = Tk()
    root.withdraw()
    # direccion = ""

    """FINAL"""
    # while not direccion:
    #     direccion = askopenfilename(initialdir="./", filetypes=[("ASM", "*.asm")])
    #     if not direccion:
    #         if not messagebox.askretrycancel(message="No se selecciono ningun archivo, ¿Desea reintentarlo?", title="No se selecciono archivo"):
    #             return

    """PARA DEBUG"""
    # direccion = ".\Practicas\Practica_01\codigoFuente\prueba.asm"
    """PARA PRUEBAS DIRECTAS DE ARCHIVO"""
    # direccion = "prueba.asm"

    # archivo = open(direccion, "r")
    
    # analizador = AnalizadorInstruccion()

    # for linea in archivo.readlines():
    #     (etiqueta, nemonico, operadores, comentarios) = analizador.analizarInstruccion(linea)
    #     # print(analizador.analizarInstruccion(linea))
    #     imprimir(linea, etiqueta, nemonico, operadores, comentarios)
    
    # archivo.close()

    """PARA PRUEBAS UNITARIAS"""
    linea = str(input("Escribe la instruccion: "))
    analizador = AnalizadorInstruccion()
    (etiqueta, nemonico, operadores, comentarios) = analizador.analizarInstruccion(linea)
    imprimir(linea, etiqueta, nemonico, operadores, comentarios)



def imprimir(instruccion, etiqueta, nemonico, operadores, comentarios):
    print("\n" + instruccion)

    if etiqueta != "":
        print("\nEtiqueta:\t\t" + etiqueta)
    if nemonico != "":
        print("Nemonico:\t\t" + nemonico)
    # Evaluar si existen varios operadores
    if operadores != []:
        for elemento in range(len(operadores)):
            print("Operador" + str(elemento+1) + ":\t\t" + operadores[elemento])
    if comentarios != "":
        print("Comentarios:\t\t" + comentarios)

if __name__ == '__main__':
    main()