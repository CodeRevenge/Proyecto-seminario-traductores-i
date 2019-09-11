from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class Instruccion:
    def __init__(self):
        self.etiqueta = ""
        self.nemonico = ""
        self.operadores = []
        self.comentarios = ""

class AnalizadorInstruccion(Instruccion):
    def __init__(self):
        self.simbolo = ""
        self.tipo = 0

    def analizarInstruccion(self, instruccion):
        self.tipo = 0
        self.simbolo = ""
        Instruccion.__init__(self)

        for indice in range(len(instruccion)):
            if self.tipo != 2:
                if instruccion[indice] != " ":
                    self.simbolo += instruccion[indice]
                else:
                    self.asignarTipo()
                    self.tipo += 1
                    self.simbolo = ""
            else:
                if instruccion[indice] != ";":
                    self.simbolo += instruccion[indice]
                else:
                    self.asignarTipo()
                    self.tipo += 1
                    self.simbolo = ""
                    indice -= 1

            if indice == len(instruccion)-1:
                self.asignarTipo()


        
        return self.etiqueta, self.nemonico, self.operadores

    def asignarTipo(self):
        tipoSimbolo = {
            0: self.asignarEtiqueta,
            1: self.asignarNemonico,
            2: self.asignarOperadores,
            3: self.asignarComentarios
        }

        tipoSimbolo.get(int(self.tipo))()


    def asignarEtiqueta(self):
        self.etiqueta = self.simbolo
    
    def asignarNemonico(self):
        self.nemonico = self.simbolo
    
    def asignarOperadores(self):
        oper = self.simbolo.split(",")
        for x in range(len(oper)):
            a = oper[x].strip()
            if a != "":
                self.operadores.append(a)

    def asignarComentarios(self):
        self.comentarios = self.simbolo

    def analizarEstructura(self):
        root = Tk()
        root.withdraw()
        direccion = ""
        instrucciones = []
        while not direccion:
            direccion = askopenfilename(initialdir="./", filetypes=[("ASM", "*.asm")])
            if not direccion:
                if not messagebox.askretrycancel(message="No se selecciono ningun archivo, ¿Desea reintentarlo?", title="No se selecciono archivo"):
                    return False
        archivo = open(direccion, "r")
        for linea in archivo.readlines():
            linea = linea.rstrip()
            if linea != "":
                # Retorna una tupla del tipo (etiqueta:str, nemonico:str, operadores:list, comentarios:str)
                instrucciones.append(self.analizarInstruccion(linea))      
        archivo.close()
        return instrucciones