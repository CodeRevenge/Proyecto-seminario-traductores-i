#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from baseconvert import base
from analizadorEstructura import AnalizadorInstruccion
import sys

class Constantes:
    def __init__(self):
        self.INDICE_NEMONICOS = 0
        self.INDICE_NUM_OPERADORES = 1
        self.INDICE_TIPO = 2
        self.INDICE_CODIGO_HEX = 3

        self.SEPARADOR_COMA = ","

        self.INDICADOR_INMEDIATO = "#"
        self.INDICADOR_OCTAL = "@"
        self.INDICADOR_HEXADECIMAL = "$"
        self.INDICADOR_BINARIO = "%"

        self.COMENTARIO = "#"

        self.DIRECCIONAMIENTO_INHERENTE = "INH"
        self.DIRECCIONAMIENTO_INMEDIATO = "IMM"
        self.DIRECCIONAMIENTO_DIRECTO = "DIR"
        self.DIRECCIONAMIENTO_EXTENDIDO = "EXT"
        self.DIRECCIONAMIENTO_INDEXADO = "IDX"

class ModoDireccionamiento(Constantes):
    def __init__(self):
        Constantes.__init__(self)

        self.instrucciones = []
        self.listaNemonicos = []

    def modoDireccionamiento(self):
        self.nemonicos()
        if not self.listaNemonicos: return False
        self.recogerInstrucciones()
        if not self.instrucciones: return False

        for instruccion in self.instrucciones:
            ocurrencias = self.ocurrenciasNemonicos(instruccion[1])
            if ocurrencias:
                if not self.analizarOperadores(ocurrencias, instruccion[2]): return False
            else:
                print("El mnemotecnico " + instruccion[1] + " no esta definido")
                return False

    def recogerInstrucciones(self):
        analizador = AnalizadorInstruccion()
        self.instrucciones = analizador.analizarEstructura()

    # Función para leer los nemonicos del archivo nemonicos.nem
    def nemonicos(self):
        direccion = "codigoFuente/nemonicos.nem"
        try:
            archivo = open(direccion, "r")
        except IOError:
            root = Tk()
            root.withdraw()
            direccion = ""
            while not direccion:
                if messagebox.askyesno(message="El archivo nemonicos.nem no existe en el directorio por default, ¿desea buscarlo en otro directorio?", title="No se encontro el archivo nemonicos.nem"):
                    direccion = askopenfilename(initialdir="./", filetypes=[("NEM", "*.nem")])
                    if not direccion:
                        if not messagebox.askretrycancel(message="No se selecciono ningun archivo, ¿Desea reintentarlo?", title="No se selecciono archivo"):
                            return False
            self.listaNemonicos.clear()
            archivo = open(direccion, "r")
            for linea in archivo.readlines():
                linea = linea.strip()
                if not linea.startswith(self.COMENTARIO):
                    linea = linea.split(self.SEPARADOR_COMA)
                    self.listaNemonicos.append(linea)
        else:
            self.listaNemonicos.clear()
            for linea in archivo.readlines():
                linea = linea.strip()
                if not linea.startswith(self.COMENTARIO):
                    linea = linea.split(self.SEPARADOR_COMA)
                    self.listaNemonicos.append(linea)

    def ocurrenciasNemonicos(self, nemonico):
        ocurrencias = [valor for indice, valor in enumerate(self.listaNemonicos) if valor[self.INDICE_NEMONICOS] == nemonico]
        return False if not ocurrencias else ocurrencias

    def analizarOperadores(self, ocurrencias, operadores):
        if not operadores:
            return [nemonico for indice, nemonico in enumerate(ocurrencias) if nemonico[self.INDICE_TIPO] == self.DIRECCIONAMIENTO_INHERENTE]
        elif len(operadores) == 1:
            if operadores[0][0] == self.INDICADOR_INMEDIATO:
                hex = self.verificarBase(operadores[0].lstrip(self.INDICADOR_INMEDIATO))
                self.verificarDireccionamiento(hex)
            else:
                hex = self.verificarBase(operadores[0])
                self.verificarDireccionamiento(hex)
        elif len(operadores) == 2:
            pass
        else:
            return False        

    def verificarBase(self, operador):
        hexadecimal = ""
        if operador[0] == self.INDICADOR_HEXADECIMAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_HEXADECIMAL).upper(), 16,16)
            except ValueError:
                print("El operador " + operador[0] + " no esta bien definido")
                print(sys.exc_info()[0])
                return False
        elif operador[0] == self.INDICADOR_OCTAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_OCTAL).upper(), 8,16)
            except ValueError:
                print("El operador " + operador[0] + " no esta bien definido")
                print(sys.exc_info()[0])
                return False
        elif operador[0] == self.INDICADOR_BINARIO:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_BINARIO).upper(), 2,16)
            except ValueError:
                print("El operador " + operador[0] + " no esta bien definido")
                print(sys.exc_info()[0])
                return False
        else:
            try:
                hexadecimal = base(operador.upper(), 10,16)
            except ValueError:
                print("El operador " + operador[0] + " no esta bien definido")
                print(sys.exc_info()[0])
                return False
        return hexadecimal

    def verificarDireccionamiento(self, hexadeciamal):
        pass