#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from src.modoDireccionamiento import ModoDireccionamiento

def main():
    direccionamiento = ModoDireccionamiento()
    direccionamiento.modoDireccionamiento()
    direccionamiento.segundoPaso(direccionamiento.listaTabla, direccionamiento.listaTABSIM)
    direccionamiento.vaciarCodigo(direccionamiento.listaTabla, direccionamiento.listaTABSIM)
    if not direccionamiento.instrucciones:
        pass


if __name__ == '__main__':
    main()