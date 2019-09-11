from src.funcionalidades import Funcionalidad

class ContadorLocalidades(Funcionalidad):
    def __init__(self):
        self.NOMBRE_ARCHIVO_CONT_LOC = "contloc.cl"
        self.NOMBRE_ARCHIVO_TAB_SIM = "TABSIM"
        self.NOMBRE_ARCHIVO_COD_OP = "codop.hex"
        self.NOMBRE_TABLA = "tabla.lst"
        self.SEPARADOR = '\n'
        self.SEPARADOR_COD_OP = " "

        self.contador = 0

        self.crearArchivos()

        Funcionalidad.__init__(self)

    def crearArchivos(self):
        archivo = open(self.NOMBRE_ARCHIVO_CONT_LOC,'w')
        archivo.close()
        archivo = open(self.NOMBRE_ARCHIVO_TAB_SIM,'w')
        archivo.close()
        archivo = open(self.NOMBRE_ARCHIVO_COD_OP,'w')
        archivo.close()
        archivo = open(self.NOMBRE_TABLA, 'w')
        archivo.close()

    def escribirCodOp(self, codigoOp):
        codop = open(self.NOMBRE_ARCHIVO_COD_OP, 'a')
        nCodop = self.separarCodop(codigoOp)
        codop.write(nCodop + self.SEPARADOR)
        codop.close()

    def escribirContLoc(self, posicion):
        contloc = open(self.NOMBRE_ARCHIVO_CONT_LOC, "a")
        contloc.write(posicion + self.SEPARADOR)
        contloc.close()

    def escribirTabSim(self, instruccion):
        archivo = open(self.NOMBRE_ARCHIVO_TAB_SIM,"a")
        archivo.write(instruccion + self.SEPARADOR)
        archivo.close()

    def sumarPosicion(self, agregado, tipo = True):
        if tipo:
            agregadoDec = self.hex2Dec(agregado)
        else:
            agregadoDec = agregado

        if agregadoDec:
            self.contador += int(int(agregadoDec)/2)
            return self.posicionHex().zfill(4)
        else:
            return agregadoDec

    def posicionHex(self):
        return self.dec2Hex(self.contador).zfill(4)

    def asignarPosicion(self, posicion):
        nContador = self.hex2Dec(posicion)
        if nContador:
            self.contador = int(nContador)
            return self.posicionHex().zfill(4)
        else:
            return False

    def guardarTabla(self, localidad, codop):
        tabla = open(self.NOMBRE_TABLA,'a')
        ncodop = self.separarCodop(codop)
        tabla.write(localidad + " " + ncodop + " \n")
        tabla.close()

    def separarCodop(self, codop):
        nCodop = ""
        for x in range(0,len(codop),2):
            nCodop += codop[x:x+2] + self.SEPARADOR_COD_OP
        return nCodop.rstrip()