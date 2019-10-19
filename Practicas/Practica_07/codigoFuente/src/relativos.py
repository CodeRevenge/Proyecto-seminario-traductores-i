from baseconvert import base
from bitstring import Bits
from src.crearContLoc import ContadorLocalidades
from src.funcionalidades import Funcionalidad

class Relativos(ContadorLocalidades):
    def __init__(self):
        ContadorLocalidades.__init__(self)
        Funcionalidad.__init__(self)

        self.RELATIVO = 'REL'
        self.RELATIVO_9 = 'REL9'
        self.LIMITE_MAX_REL8 = 127
        self.LIMITE_MIN_REL8 = -128
        self.LIMITE_MAX_REL16 = 32767
        self.LIMITE_MIN_REL16 = -32768
        self.LIMITE_REL9 = 255
        self.REGISTROS = ['A','B','D','X','Y','SP']

        self.direccionesRelativos = []
        self.direccionesRelativos9 = []

    def esRelativo(self, nemonico):
        return True if nemonico[2] == self.RELATIVO or nemonico[2] == self.RELATIVO_9 else False

    def esEtiqueta(self, operador):
        if operador[0] != '$' or operador[0] != '%' or operador[0] != '@':
            try:
                base(operador,10, string=True)
            except ValueError:
                return True
            else:
                return False



    def asignarMemoriaRelativo(self, nemonico):
        codop = nemonico[3]
        codop += "".zfill(int(nemonico[4]))
        return codop

    def asignarMemoriaRelativo_REL9(self):
        return '040000'

    def validarOperadoresRel(self, instruccion):
        return True if len(instruccion[2]) == 1 else False

    def validarOperadoresRel_9(self, instruccion):
        return True if len(instruccion[2]) == 2 else False
    
    def tipoRelativo(self, instruccion):
        if instruccion == self.RELATIVO:
            return self.RELATIVO
        elif instruccion == self.RELATIVO_9:
            return self.RELATIVO_9
        else:
            return False

    def verificarRelativos(self, instruccion):
        if len(instruccion[2][3]) == 2:
            return self.verificarRel8(instruccion)
        elif len(instruccion[2][3]) == 4:
            return self.verificarRel16(instruccion)
        else:
            False

    def verificarRel8(self, instruccion):
        operador = instruccion[3][2][0]
        id = self.existeIdentificador(operador)
        if id[0]:
            op = id[1][1]
            sigPos = self.obtenerSiguientePosicion(instruccion)
            op = Bits(hex=op).int
            sigPos = Bits(hex=sigPos).int
            res = op - sigPos
            if res <= self.LIMITE_MAX_REL8 and res >= self.LIMITE_MIN_REL8:
                op = Bits(int=res,length=8)
                return instruccion[1][0:2] + op.hex.upper()
            else:
                print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))
        else:
            operador = self.verificarBase(operador)
            sigPos = self.obtenerSiguientePosicion(instruccion)
            operador = Bits(hex=operador).int
            sigPos = Bits(hex=sigPos).int
            res = operador - sigPos
            if res <= self.LIMITE_MAX_REL8 and res >= self.LIMITE_MIN_REL8:
                op = Bits(int=res,length=8)
                return instruccion[1][0:2] + op.hex.upper()
            else:
                print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))
        


    def verificarRel16(self, instruccion):
        operador = instruccion[3][2][0]
        id = self.existeIdentificador(operador)
        if id[0]:
            op = id[1][1]
            sigPos = self.obtenerSiguientePosicion(instruccion)
            op = Bits(hex=op).int
            sigPos = Bits(hex=sigPos).int
            res = op - sigPos
            if res <= self.LIMITE_MAX_REL16 and res >= self.LIMITE_MIN_REL16:
                op = Bits(int=res,length=16)
                return instruccion[1][0:4] + op.hex.upper()
            else:
                print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))
        else:
            operador = self.verificarBase(operador)
            sigPos = self.obtenerSiguientePosicion(instruccion)
            res = Bits(hex=operador).int - Bits(hex=sigPos).int
            if res <= self.LIMITE_MAX_REL16 and res >= self.LIMITE_MIN_REL16:
                op = Bits(int=res,length=16)
                return instruccion[1][0:4] + op.hex.upper()
            else:
                print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))

    def verificarRelativos_9(self, instruccion):
        registro = instruccion[3][2][0]
        operador = instruccion[3][2][1]
        if registro in self.REGISTROS:
            id = self.existeIdentificador(operador)
            if id[0]:
                op = id[1][1]
                sigPos = self.obtenerSiguientePosicion(instruccion)
                op = Bits(hex=op).int
                sigPos = Bits(hex=sigPos).int
                res = op - sigPos
                if abs(res) <= self.LIMITE_REL9:
                    op = Bits(int=res,length=12)
                    nemonico = self.encontrarNemonicoRel9(instruccion, res)
                    return instruccion[1][0:2] + nemonico[4] + op.hex[1:].upper()
                else:
                    print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))
            else:
                operador = self.verificarBase(operador)
                sigPos = self.obtenerSiguientePosicion(instruccion)
                res = Bits(hex=operador).int - Bits(hex=sigPos).int
                if abs(res) <= self.LIMITE_REL9:
                    op = Bits(int=res,length=12)
                    nemonico = self.encontrarNemonicoRel9(instruccion, res)
                    return instruccion[1][0:2] + nemonico[4] + op.hex[1:].upper()
                else:
                    print('El mnemomico {} esta fuera de rango -> {}'.format(instruccion[2][0],res))
        else:
            print("El mnemonico {} esperaba un nombre de registro como primer parametro y recibió {}".format(instruccion[2][0], registro))

    def encontrarNemonicoRel9(self, instruccion, operador):
        indReg = self.REGISTROS.index(instruccion[3][2][0])
        if operador >= 0:
            return instruccion[2][:6][indReg]
        else:
            return instruccion[2][6:12][indReg]

    def obtenerSiguientePosicion(self, instruccion):
        actual = int(base(instruccion[0], 16, 10, string=True))
        agregado = len(instruccion[1])/2
        a = base(actual+agregado,10,16,string=True).rstrip('.')
        return a

    def existeIdentificador(self, operador):
        for e in self.listaTABSIM:
            if operador == e[0]:
                return [True,e]
        return [False]