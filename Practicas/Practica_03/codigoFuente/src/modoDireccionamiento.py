#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from src.analizadorEstructura import AnalizadorInstruccion
from src.analizarDirectivas import Directiva
import sys

class Constantes(Directiva):
    def __init__(self):
        self.INDICE_NEMONICOS = 0
        self.INDICE_NUM_OPERADORES = 1
        self.INDICE_TIPO = 2
        self.INDICE_CODIGO_HEX = 3

        self.INDICE_DIRECTIVA = 1

        self.SEPARADOR_COMA = ","

        self.INDICADOR_INMEDIATO = "#"
        

        self.INDICE_ETIQUETA = 0
        self.INDICE_NEMONICO = 1
        self.INDICE_OPERADORES = 2

        self.COMENTARIO = "#"

        self.DIRECCIONAMIENTO_INHERENTE = "INH"
        self.DIRECCIONAMIENTO_INMEDIATO = "IMM"
        self.DIRECCIONAMIENTO_DIRECTO = "DIR"
        self.DIRECCIONAMIENTO_EXTENDIDO = "EXT"
        self.DIRECCIONAMIENTO_INDIZADO = "IDX"
        self.DIRECCIONAMIENTO_RELATIVO = "REL"

        Directiva.__init__(self)

class ModoDireccionamiento(Constantes):
    def __init__(self):
        Constantes.__init__(self)

        self.instrucciones = []
        self.listaNemonicos = []
        self.listaDirectivas = []

    def modoDireccionamiento(self):
        self.nemonicos()
        self.directivas()
        if not self.listaNemonicos: return False
        self.recogerInstrucciones()
        if not self.instrucciones: return False
        # print('{:^10}'.format("Bytes") + "|" + '{:^30}'.format("Instrucción") + "|" + '{:^30}'.format("Tipo direccionamiento"))
        for instruccion in self.instrucciones:
            if instruccion[0]:
                self.validarEtiquetas(instruccion)
                pass
            if self.validarDirectivas(instruccion):
                if not self.analizarDirectiva(instruccion):
                    return
                # print('{:^10}'.format("LI") + "|" + '{:<30}'.format(self.unirLista(instruccion, " ")) + "|" +'{:^30}'.format("Directiva")) 
            else:
                ocurrencias = self.ocurrenciasNemonicos(instruccion[self.INDICE_NEMONICO])
                if ocurrencias:
                    nemonico = self.analizarOperadores(ocurrencias, instruccion[self.INDICE_OPERADORES])
                    if not nemonico[0]: 
                        pass
                        # print('{:^10}'.format("-----") + "|" + '{:<30}'.format(self.unirLista(instruccion, " ")) + "|" + '{:^30}'.format("Es invalida"))
                        print("El mnemonico " + instruccion[1] + " no es valido con los operadores indicados")
                        return False
                    else:
                        self.guardarTabla(self.posicionHex(), self.convertirCodOp(nemonico[0][0], nemonico[1]))
                        self.sumarPosicion(str(self.calcularBytes(nemonico[0][0])))
                        self.escribirContLoc(self.posicionHex())
                        self.escribirCodOp(self.convertirCodOp(nemonico[0][0], nemonico[1]))
                        # print('{:^10}'.format(self.calcularBytes(nemonico[0])) + "|" + '{:<30}'.format(self.unirLista(instruccion, " ")) + "|" + '{:^30}'.format(nemonico[0][2]))
                        '''Añadir a archivo'''
                else:
                    print("El mnemotecnico " + instruccion[1] + " no esta definido")  
                    return False

    def convertirCodOp(self, nemonico, instruccion):
        cadena = ""
        cadena = nemonico[3]

        for tam in range(4,len(nemonico)):
            if instruccion[0][0] == '#':
                cadena += instruccion[0][1].zfill(int(nemonico[tam]))
            else:
                cadena += instruccion[tam-4].zfill(int(nemonico[tam]))
        
        return cadena

    def unirLista(self, lista, separador):
        cadena = ""
        for elemento in lista:
            if type(elemento) == list:
                for a in elemento:
                    cadena += str(a) + ","
            else:
                cadena += str(elemento) + separador

        return cadena.rstrip(" ,")


    def calcularBytes(self, _nemonico):
        bytes_ = 0
        bytes_ += len(_nemonico[self.INDICE_CODIGO_HEX])
        for x in range(4,len(_nemonico)):
            bytes_ +=  int(_nemonico[x])

        return bytes_

    def recogerInstrucciones(self):
        analizador = AnalizadorInstruccion()
        self.instrucciones = analizador.analizarEstructura()

    def validarDirectivas(self, instruccion):
        ocurrencias = [valor for indice, valor in enumerate(self.listaDirectivas) if valor == instruccion[self.INDICE_DIRECTIVA]]
        return False if not ocurrencias else ocurrencias

    # Función para leer los nemonicos del archivo nemonicos.nem
    def nemonicos(self):
        direccion = "src/nemonicos.nem"
        try:
            archivo = open(direccion, "r")
        except IOError:
            root = Tk()
            root.withdraw()
            direccion = ""
            while not direccion:
                if messagebox.askyesno(message="El archivo nemonicos.nem no existe en el directorio por default, ¿desea buscarlo en otro directorio?", title="No se encontro el archivo nemonicos.nem"):
                    direccion = askopenfilename(initialdir="./src/", filetypes=[("NEM", "*.nem")])
                    if not direccion:
                        if not messagebox.askretrycancel(message="No se selecciono ningun archivo, ¿Desea reintentarlo?", title="No se selecciono archivo"):
                            return False
                else:
                    return
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

    # Función para leer las directivas del achivo directivas.dir
    def directivas(self):
        direccion = "src/directivas.dir"
        try:
            archivo = open(direccion, "r")
        except IOError:
            root = Tk()
            root.withdraw()
            direccion = ""
            while not direccion:
                if messagebox.askyesno(message="El archivo directivas.dir no existe en el directorio por default, ¿desea buscarlo en otro directorio?", title="No se encontro el archivo directivas.dir"):
                    direccion = askopenfilename(initialdir="./src/", filetypes=[("DIR", "*.dir")])
                    if not direccion:
                        if not messagebox.askretrycancel(message="No se selecciono ningun archivo, ¿Desea reintentarlo?", title="No se selecciono archivo"):
                            return False
                else:
                    return
            self.listaDirectivas.clear()
            archivo = open(direccion, "r")
            for linea in archivo.readlines():
                linea = linea.strip()
                self.listaDirectivas.append(linea)
        else:
            self.listaDirectivas.clear()
            for linea in archivo.readlines():
                linea = linea.strip()
                self.listaDirectivas.append(linea)

    def ocurrenciasNemonicos(self, nemonico):
        ocurrencias = [valor for indice, valor in enumerate(self.listaNemonicos) if valor[self.INDICE_NEMONICOS] == nemonico]
        return False if not ocurrencias else ocurrencias

    def analizarOperadores(self, ocurrencias, operadores):
        filtro = [valor for indice, valor in enumerate(ocurrencias) if int(valor[self.INDICE_NUM_OPERADORES]) == len(operadores)]
        if not filtro:
            return False
        else:
            if not operadores:
                return [nemonico for indice, nemonico in enumerate(ocurrencias) if nemonico[self.INDICE_TIPO] == self.DIRECCIONAMIENTO_INHERENTE]
            else:
                operadoresHex = []
                for operador in operadores:
                    if operador[0] == self.INDICADOR_INMEDIATO:
                        base = self.verificarBase(operador.lstrip(self.INDICADOR_INMEDIATO))
                        if not base:
                            return False
                        operadoresHex.append([self.INDICADOR_INMEDIATO, base])
                    else:
                        base = self.verificarBase(operador)
                        if not base:
                            return False
                        operadoresHex.append(base)

                nemonico = self.verificarDireccionamiento(operadoresHex, filtro)

                return nemonico, operadoresHex

    """Recibe una lista con los operadores convertidos en hexadecimal
        Además de las ocurrencias relacionadas con la cantidad de operadores
    """
    def verificarDireccionamiento(self, operadoresHex, ocurrencias):
        indice = 0
        nemonico = []
        temp = []
        for operador in operadoresHex:
            if type(operador) == list:
                longitud = len(operador[1])
                if not nemonico:
                    nemonico.append([nemonico for x, nemonico in enumerate(ocurrencias) if nemonico[self.INDICE_TIPO] == self.DIRECCIONAMIENTO_INMEDIATO and int(nemonico[indice + 4]) >= longitud])
                else:
                    temp.append([nemonico for x, nemonico in enumerate(nemonico) if nemonico[self.INDICE_TIPO] == self.DIRECCIONAMIENTO_INMEDIATO and int(nemonico[indice + 4]) == longitud])
                    nemonico = temp.copy()
                indice += 1
            else:
                longitud = len(operador)
                if not nemonico:
                    nemonico.append([nemonico for x, nemonico in enumerate(ocurrencias) if nemonico[self.INDICE_TIPO] != self.DIRECCIONAMIENTO_INMEDIATO and int(nemonico[4+indice]) >= longitud])
                else:
                    temp.append([nemonico for x, nemonico in enumerate(nemonico) if nemonico[self.INDICE_TIPO] != self.DIRECCIONAMIENTO_INMEDIATO and int(nemonico[indice + 4]) == longitud])
                    nemonico = temp.copy()
                indice += 1
        
        return nemonico[0]

    def validarEtiquetas(self, instruccion):
        if instruccion[1] != self.EQU:
            self.escribirTabSim(instruccion[0] + " " + self.posicionHex())