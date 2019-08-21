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
        # self.rxEtiqueta = "[_a-zA-Z]\w*"
        # self.rxNemonico = "[A-Z]+"
        # self.rxOperadores = "\w+"
        # self.rxComentarios = ";[\w" "]*"
        

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
        oper = self.simbolo.split(",")
        for x in range(len(oper)):
            a = oper[x].strip()
            if a != "":
                self.operadores.append(a)

    def asignarComentarios(self):
        self.comentarios = self.simbolo

    