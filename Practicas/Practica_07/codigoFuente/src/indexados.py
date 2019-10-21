from bitstring import Bits
from baseconvert import base
from src.funcionalidades import Funcionalidad

class Indexados(Funcionalidad):
    def __init__(self):
        Funcionalidad.__init__(self)

        self.R_X = '00'
        self.R_Y = '01'
        self.R_SP = '10'
        self.R_PC = '11'

        self.REGISTRO_A = 'A'
        self.REGISTRO_B = 'B'
        self.REGISTRO_D = 'D'
        self.REGISTRO_X = 'X'
        self.REGISTRO_Y = 'Y'
        self.REGISTRO_SP = 'SP'
        self.REGISTRO_PC = 'PC'

        self.IDX = 'IDX'
        self.IDX_1 = 'IDX1'
        self.IDX_2 = 'IDX2'

        self.MAX_5_B = 15
        self.MIN_5_B = -16
        self.MAX_9_B = 255
        self.MIN_9_B = -256
        self.MAX_16_B = 65535
        self.MIN_16_B = -32768

    def analizarInstruccion(self, obj, instruccion, ocurrencias):
        operadores = instruccion[2]
        codOp = ocurrencias[-1][3]

        if operadores[1].startswith('+') or operadores[1].startswith('-') or operadores[1].endswith('+') or operadores[1].endswith('-'):
            pass
        else:
            if self.verificarRegistro(obj, operadores[1]):
                if self.verificarRegistroAcc(obj, operadores[0]):
                    pass
                else:
                    # if obj.esLetra(operadores[0]):
                    #     pass
                    # else:
                    size = self.determinarTamaño(obj, operadores[0])
                    if size == 16:
                        nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.IDX_2]
                        nem = nem[0]
                        codOp = codOp + ''.zfill(int(nem[4]))
                        posAct = obj.posicionHex()
                        obj.sumarPosicion(len(codOp), tipo=False)
                        return [posAct, codOp, nem, instruccion, self.IDX_2]
                    elif size == 9:
                        nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.IDX_1]
                        nem = nem[0]
                        codOp = codOp + ''.zfill(int(nem[4]))
                        posAct = obj.posicionHex()
                        obj.sumarPosicion(len(codOp), tipo=False)
                        return [posAct, codOp, nem, instruccion, self.IDX_1]
                    elif size == 5:
                        nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.IDX]
                        nem = nem[0]
                        codOp = codOp + ''.zfill(int(nem[4]))
                        posAct = obj.posicionHex()
                        obj.sumarPosicion(len(codOp), tipo=False)
                        return [posAct, codOp, nem, instruccion, self.IDX]
                    else:
                        return False

            else:
                print('Error: Se esperaba un nombre de registro y se recibio {}'.format(operadores[1]))

    def verificarRegistro(self, obj, operador):
        x = operador == obj.REGISTRO_X
        y = operador == obj.REGISTRO_Y
        sp = operador == obj.REGISTRO_SP
        pc = operador == obj.REGISTRO_PC

        if x or y or sp or pc:
            return True
    
    def verificarRegistroAcc(self, obj, operador):
        a = operador == obj.REGISTRO_A
        b = operador == obj.REGISTRO_B
        d = operador == obj.REGISTRO_D

        if a or b or d:
            return True

    def determinarTamaño(self, obj, operador):
        if obj.esEtiquetaInd(operador):
            return 16

        op = self.verificarBaseFull(operador)
        if type(op) == str:
            opInt = int(self.hex2Dec(op))   
        else:
            opInt = op

        if opInt > self.MAX_16_B or opInt < self.MIN_16_B:
            print('El operador {} esta fuera de rango'.format(opInt))
            return False
        elif opInt > self.MAX_9_B or opInt < self.MIN_9_B:
            return 16
        elif opInt > self.MAX_5_B or opInt < self.MIN_5_B:
            return 9
        else:
            return 5

    def obtenerCodRegistro(self, registro):
        if registro == self.REGISTRO_X:
            return self.R_X
        elif registro == self.REGISTRO_Y:
            return self.R_Y
        elif registro == self.REGISTRO_SP:
            return self.R_SP
        elif registro == self.REGISTRO_PC:
            return self.R_PC

    def verificarIndexados(self, obj, instruccion):
        switch = {
            'IDX':self.funcion01,
            'IDX1':self.funcion02,
            'IDX2':self.funcion02,
        }

        return switch.get(instruccion[4],self.default)(obj, instruccion)

    
    def funcion01(self, obj, instruccion):
        codop = instruccion[1][:2]
        num = int(self.verificarBaseFull(instruccion[3][2][0]))

        rr = self.obtenerCodRegistro(instruccion[3][2][1])

        if num >= 0:
            n = '0'
        else:
            n = '1'

        nnnn = Bits(int=num, length=8).bin[4:]

        return codop + base(rr + '0' + n + nnnn,2,16,string=True).zfill(int(instruccion[2][4]))



    def funcion02(self, obj, instruccion):
        if instruccion[4] == self.IDX_1:
            codop = instruccion[1][:2]
            num = int(self.verificarBaseFull(instruccion[3][2][0]))
            rr = self.obtenerCodRegistro(instruccion[3][2][1])
            z = '0'
            if num >= 0:
                s = '0'
            else:
                s = '1'
            
            offset = Bits(int=num, length=12).bin[4:]
        else:
            codop = instruccion[1][:2]
            a = obj.existeIdentificador(instruccion[3][2][0])
            if a[0]:
                idNum = a[1][1]
                num = int(self.verificarBaseFull(idNum))
            else:
                num = int(self.verificarBaseFull(instruccion[3][2][0]))
            rr = self.obtenerCodRegistro(instruccion[3][2][1])
            z = '1'
            if num >= 0:
                s = '0'
                offset = Bits(uint=num, length=16).bin
            else:
                s = '1'
                offset = Bits(int=num, length=16).bin[4:]


        return codop + base('111' + rr + '0' + z + s + offset,2,16,string=True).zfill(int(instruccion[2][4]))

    def default(self):
        print('No existe este tipo de indexado')



