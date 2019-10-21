from baseconvert import base
from bitstring import Bits

class Funcionalidad:
    def __init__(self):
        self.INDICADOR_OCTAL = "@"
        self.INDICADOR_HEXADECIMAL = "$"
        self.INDICADOR_BINARIO = "%"
    
    def verificarBase(self, operador):
        hexadecimal = ""
        if operador[0] == self.INDICADOR_HEXADECIMAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_HEXADECIMAL).upper(), 16,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        elif operador[0] == self.INDICADOR_OCTAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_OCTAL).upper(), 8,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        elif operador[0] == self.INDICADOR_BINARIO:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_BINARIO).upper(), 2,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        else:
            try:
                hexadecimal = base(operador.upper(), 10,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        return hexadecimal

    def verificarBaseFull(self, operador):
        hexadecimal = ""
        if operador[0] == self.INDICADOR_HEXADECIMAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_HEXADECIMAL).upper(), 16,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        elif operador[0] == self.INDICADOR_OCTAL:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_OCTAL).upper(), 8,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        elif operador[0] == self.INDICADOR_BINARIO:
            try:
                hexadecimal = base(operador.lstrip(self.INDICADOR_BINARIO).upper(), 2,16,string=True)
            except ValueError:
                # print("El operador " + operador + " no esta bien definido")
                return False
        else:
            return int(operador)
        return hexadecimal

    def dec2Hex(self, convertir):
        try:
            hexadecimal = base(str(convertir).upper(), 10,16, string=True)
        except ValueError:
            print("El valor " + str(convertir) + " no puede ser convertido de decimal a hexadecimal")
            return False
        return hexadecimal

    def hex2Dec(self, convertir):
        try:
            decimal = base(convertir.upper(), 16,10, string=True)
        except ValueError:
            print("El valor " + str(convertir) + " no puede ser convertido de hexadecimal a decimal")
            return False
        return decimal

