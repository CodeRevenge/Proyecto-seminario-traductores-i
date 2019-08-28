#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from analizadorEstructura import AnalizadorInstruccion

class ModoDireccionamiento:
    def __init__(self):
        self.instrucciones = []

    def modoDireccionamiento(self):
        pass

    def recogerInstrucciones(self):
        analizador = AnalizadorInstruccion()
        self.instrucciones = analizador.analizarEstructura()

    def nemonicos(self):
        pass