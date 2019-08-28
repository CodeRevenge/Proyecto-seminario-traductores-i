#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from modoDireccionamiento import ModoDireccionamiento

def main():
    direccionamiento = ModoDireccionamiento()
    direccionamiento.recogerInstrucciones()
    if not direccionamiento.instrucciones:
        pass


if __name__ == '__main__':
    main()