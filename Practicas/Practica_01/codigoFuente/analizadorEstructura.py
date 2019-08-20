import re

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
        self.rxEtiqueta = "[_a-zA-Z][_a-zA-Z0-9]*"
        self.rxNemonico = "[A-Z]+"
        

    def analizarInstruccion(self, instruccion):
        self.tipo = 0
        self.simbolo = ""
        Instruccion.__init__(self)

        for indice in range(len(instruccion)):
            if instruccion[indice] != " ":
                self.simbolo += instruccion[indice]
            else:
                self.asignarTipo()
                self.tipo += 1
                self.simbolo = ""

            if indice == len(instruccion)-1:
                self.asignarTipo()

        return self.etiqueta, self.nemonico, self.operadores, self.comentarios

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
        self.operadores.append(self.simbolo)

    def asignarComentarios(self):
        self.comentarios = self.simbolo

    