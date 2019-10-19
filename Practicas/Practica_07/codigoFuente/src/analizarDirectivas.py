from src.crearContLoc import ContadorLocalidades

class Directiva(ContadorLocalidades):
    def __init__(self):
        self.ORG = "ORG"
        self.END = "END"
        self.START = "START"
        self.EQU = "EQU"
        self.BSZ = "BSZ"
        self.FILL = "FILL"
        self.DC_B = "DC.B"
        self.DC_W = "DC.W"
        self.FCC = "FCC"
        self.FCB = "FCB"

        

        self.toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])


        self.DIRECTIVAS = {
            "ORG": self.dirOrg,
            "END": self.dirEnd,
            "START": self.dirStart,
            "EQU": self.dirEqu,
            "BSZ": self.dirBSZ,
            "FILL": self.dirFill,
            "DC.B": self.dirDC_B,
            "DC.W": self.dirDC_W,
            "FCC": self.dirFCC,
            "FCB": self.dirFCB,
        }
        
        ContadorLocalidades.__init__(self)

    def analizarDirectiva(self, instruccion):
        return self.DIRECTIVAS.get(instruccion[1].upper(), self.Error)(instruccion)

    def Error(self, param):
        return False

    def dirOrg(self, instruccion):
        if len(instruccion[2]) > 1:
            print("Error: La directiva ORG recibió " + str(len(instruccion[2])) + "argumentos y se esperaba 1 argumento")
            return False
        else:
            direccion = instruccion[2][0]
            direccion = self.verificarBase(direccion)
            if direccion:
                # self.escribirContLoc(self.posicionHex())
                # self.guardarTabla(self.posicionHex(), "")
                nuevaDir = self.asignarPosicion(direccion)
                if nuevaDir:
                    # self.guardarTabla(self.posicionHex(), "")
                    # self.escribirContLoc(nuevaDir)
                    return direccion
            else:
                print("Error: La directiva ORG recibió un parametro invalido")
                return False

    def dirEnd(self, instruccion):
        if len(instruccion[2]) > 0:
            print("Error: La directiva END recibió " + str(len(instruccion[2])) + "argumentos y no se esperaba ninguno")
        else:
            # self.guardarTabla(self.posicionHex(), "")
            # self.escribirContLoc(self.posicionHex())
            return False
        
    def dirStart(self, instruccion):
        if len(instruccion[2]) > 0:
            print("Error: La directiva START recibió " + str(len(instruccion[2])) + "argumentos y no se esperaba ninguno")
            return False
        else:
            nuevaDir = self.asignarPosicion("0")
            if nuevaDir:
                    # self.guardarTabla(self.posicionHex(), "")
                    # self.escribirContLoc(nuevaDir)
                    return nuevaDir

    def dirEqu(self, instruccion):
        if len(instruccion[2]) > 1:
            print("Error: La directiva EQU recibió " + str(len(instruccion[2])) + "argumentos y se esperaba uno")
            return False
        elif len(instruccion[2]) == 0:
            print("Error: La directiva EQU recibió " + str(len(instruccion[2])) + "argumentos y se esperaba uno")
            return False
        else:
            etiqueta = instruccion[0]
            posicion = instruccion[2][0]
            posicion = self.verificarBase(posicion)
            self.listarTabSim([etiqueta, posicion])
            # self.escribirTabSim(etiqueta + " " + posicion)
            # self.escribirContLoc(self.posicionHex())
            # self.guardarTabla(self.posicionHex(), "")
            return True

    def dirBSZ(self, instruccion):
        if len(instruccion[2]) != 1:
            print("Error: La directiva BSZ recibió " + str(len(instruccion[2])) + "argumentos y se esperaba uno")
            return False
        else:
            posiciones = instruccion[2][0]
            cadena = "".zfill(int(posiciones)*2)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(int(posiciones)*2), False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            
            return nPos


    def dirFill(self, instruccion):
        if len(instruccion[2]) != 2:
            print("Error: La directiva FILL recibió " + str(len(instruccion[2])) + "argumentos y se esperaban dos")
            return False
        else:
            cadena = ""
            byte_ = instruccion[2][0]
            byte_ = self.verificarBase(byte_).zfill(2)
            veces = int(instruccion[2][1])
            cadena = byte_ * veces

            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(veces*2), False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos
            

    def dirDC_B(self, instruccion):
        if len(instruccion[2]) == 0:
            cadena = "".zfill(2)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion("2", False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos
        else:
            cadena = ""
            for operador in instruccion[2]:
                temp = self.verificarBase(operador)
                if len(temp) > 2:
                    print("Error: La directiva DC.B recibió un parametro de más de un byte")
                    return False
                else:
                    cadena += temp.zfill(2)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(len(cadena)), False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos

    def dirDC_W(self, instruccion):
        if len(instruccion[2]) == 0:
            cadena = "".zfill(4)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion("4", False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos
        else:
            cadena = ""
            for operador in instruccion[2]:
                temp = self.verificarBase(operador)
                if len(temp) > 4:
                    print("Error: La directiva DC.W recibió un parametro de más de dos byte")
                    return False
                else:
                    cadena += temp.zfill(4)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(len(cadena)), False)
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos

    def dirFCB(self, instruccion):
        if len(instruccion[2]) != 1:
            print("Error: La directiva FCC recibió " + str(len(instruccion[2])) + "argumentos y se esperaba uno")
            return False
        else:
            cadena = self.verificarBase(instruccion[2][0]).zfill(2)
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(len(cadena)))
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos

    def dirFCC(self, instruccion):
        if len(instruccion[2]) != 1:
            print("Error: La directiva FCC recibió " + str(len(instruccion[2])) + "argumentos y se esperaba uno")
            return False
        else:
            cadena = instruccion[2][0][1:-1]
            cadena = self.toHex(cadena).upper()
            self.listarTabla(self.posicionHex(), cadena)
            nPos = self.sumarPosicion(str(len(cadena)))
            # self.escribirCodOp(cadena)
            # self.escribirContLoc(nPos)
            return nPos