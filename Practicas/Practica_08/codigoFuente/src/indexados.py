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
        self.D_IDX = 'D_IDX'
        self.E_IDX2 = 'E_IDX2'
        self.F_4 = 'F_4'
        self.F_5 = 'F_5'

        self.MAX_5_B = 15
        self.MIN_5_B = -16
        self.MAX_9_B = 255
        self.MIN_9_B = -256
        self.MAX_16_B = 65535
        self.MIN_16_B = -32768

    def analizarInstruccion(self, obj, instruccion, ocurrencias):
        operadores = instruccion[2]
        codOp = ocurrencias[-1][3]

        if len(operadores) > 2:
            print('Error: Se recibieron más de dos operadores. {}'.format(instruccion))
            return False
        else:
            if operadores[0].startswith('[') and operadores[1].endswith(']'):
                if operadores[0].endswith('D') and len(operadores[0]) == 2:
                    nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.D_IDX]
                    nem = nem[0]
                    codOp = nem[3]
                    codOp = codOp + ''.zfill(int(nem[4]))
                    posAct = obj.posicionHex()
                    obj.sumarPosicion(len(codOp), tipo=False)
                    return [posAct, codOp, nem, instruccion, self.D_IDX]
                else:
                    n = operadores[0][1:]
                    size = self.determinarTamaño(obj, n)
                    if size <= 16:
                        nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.E_IDX2]
                        nem = nem[0]
                        codOp = nem[3]
                        codOp = codOp + ''.zfill(int(nem[4]))
                        posAct = obj.posicionHex()
                        obj.sumarPosicion(len(codOp), tipo=False)
                        return [posAct, codOp, nem, instruccion, self.E_IDX2]
                    else:
                        print('Error: El operador esta fuera de rango. {}'.format(instruccion))
            elif operadores[1].startswith('+') or operadores[1].startswith('-') or operadores[1].endswith('+') or operadores[1].endswith('-'):
                size = (int(operadores[0]) > 0 and int(operadores[0]) <= 8)
                if size:
                    nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.IDX]
                    nem = nem[0]
                    codOp = nem[3]
                    codOp = codOp + ''.zfill(2)
                    posAct = obj.posicionHex()
                    obj.sumarPosicion(len(codOp), tipo=False)
                    return [posAct, codOp, nem, instruccion, self.F_4]
                else:
                    print('Error: El operador esta fuera de rango. {}'.format(instruccion))
            else:
                if self.verificarRegistro(obj, operadores[1]):
                    if self.verificarRegistroAcc(obj, operadores[0]):
                        nem = [valor for indice, valor in enumerate(ocurrencias) if valor[2] == self.IDX]
                        nem = nem[0]
                        codOp = nem[3]
                        codOp = codOp + ''.zfill(2)
                        posAct = obj.posicionHex()
                        obj.sumarPosicion(len(codOp), tipo=False)
                        return [posAct, codOp, nem, instruccion, self.F_5]
                    else:
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
        else:
            print('Error: El registro no es valido. {}'.format(registro))
            return False

    def verificarIndexados(self, obj, instruccion):
        switch = {
            'IDX':self.funcion01,
            'IDX1':self.funcion02,
            'IDX2':self.funcion02,
            'E_IDX2':self.funcion03,
            'F_4':self.funcion04,
            'F_5':self.funcion05,
            'D_IDX':self.funcion06,
        }

        return switch.get(instruccion[4],self.default)(obj, instruccion)

    
    def funcion01(self, obj, instruccion):
        codop = instruccion[1][:2]
        num = int(self.verificarBaseFull(instruccion[3][2][0]))

        rr = self.obtenerCodRegistro(instruccion[3][2][1])
        if not rr:
            return False

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
            if not rr:
                return False
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
            if not rr:
                return False
            z = '1'
            if num >= 0:
                s = '0'
                offset = Bits(uint=num, length=16).bin
            else:
                s = '1'
                offset = Bits(int=num, length=16).bin[4:]


        return codop + base('111' + rr + '0' + z + s + offset,2,16,string=True).zfill(int(instruccion[2][4]))

    def funcion03(self, obj, instruccion):
        codop = instruccion[1][:2]
        a = obj.existeIdentificador(instruccion[3][2][0][1:])
        if a[0]:
            idNum = a[1][1]
            num = self.verificarBaseFull(idNum)
        else:
            num = self.verificarBaseFull(instruccion[3][2][0][1:])

        rr = self.obtenerCodRegistro(instruccion[3][2][1][:-1])
        if not rr:
            return False


        if type(num) == int:
            n = Bits(int=num, length=16).bin[4:]
        else:
            n = Bits(hex=num).bin

        return codop + base('111' + rr + '011',2,16,string=True) + base(n,2,16,string=True).zfill(4)
    
    def funcion04(self, obj, instruccion):
        codop = instruccion[1][:2]

        a = obj.existeIdentificador(instruccion[3][2][0])
        if a[0]:
            idNum = a[1][1]
            num = self.verificarBaseFull(idNum)
        else:
            num = self.verificarBaseFull(instruccion[3][2][0])
        
        if instruccion[3][2][1].startswith('+') or instruccion[3][2][1].startswith('-'):
            if instruccion[3][2][1][1:] == self.REGISTRO_PC:
                print('Error: No es valido el registro PC para esta instrucción. {}'.format(instruccion))
                return False
            rr = self.obtenerCodRegistro(instruccion[3][2][1][1:])
            if not rr:
                return False
            p = '0'
        elif instruccion[3][2][1].endswith('+') or instruccion[3][2][1].endswith('-'):
            if instruccion[3][2][1][:-1] == self.REGISTRO_PC:
                print('Error: No es valido el registro PC para esta instrucción. {}'.format(instruccion))
                return False
            rr = self.obtenerCodRegistro(instruccion[3][2][1][:-1])
            if not rr:
                return False
            p = '1'

        if instruccion[3][2][1].startswith('+') or instruccion[3][2][1].endswith('+'):
            nnnn = Bits(int=int(num)-1, length=8).bin[4:]
        elif instruccion[3][2][1].startswith('-') or instruccion[3][2][1].endswith('-'):
            nnnn = Bits(int=-int(num), length=8).bin[4:]

        return codop + base(rr + '1' + p + nnnn,2,16,string=True)

    def funcion05(self, obj, instruccion):
        codop = instruccion[1][:2]

        if instruccion[3][2][0] == self.REGISTRO_A:
            aa = '00'
        elif instruccion[3][2][0] == self.REGISTRO_B:
            aa = '01'
        elif instruccion[3][2][0] == self.REGISTRO_D:
            aa = '10'
        else:
            print('Error: El acumulador no existe. {}'.format(instruccion))
            return False

        rr = self.obtenerCodRegistro(instruccion[3][2][1])

        return codop + base('111' + rr + '1' + aa,2,16,string=True)


    
    def funcion06(self, obj, instruccion):
        codop = instruccion[1][:2]

        rr = self.obtenerCodRegistro(instruccion[3][2][1][:-1])
        if not rr:
            return False

        return codop + base('111' + rr + '111',2,16,string=True)


    def default(self):
        print('No existe este tipo de indexado')



