# -*- coding: utf-8 -*-
import os

__author__ = 'Ignacio Fernández'

import unittest


def quitar_tildes(palabra):
    tildes = {'á': 'a',
              'é': 'e',
              'í': 'i',
              'ó': 'o',
              'ú': 'u',
              'ü': 'u'}
    sin_tildes = list(palabra)
    for cont in range(len(palabra)):
        letra = palabra[cont]
        if letra in tildes:
            sin_tildes[cont] = tildes[letra]
    return ''.join(sin_tildes)


def quitar_tildes2(palabra):
    tildes = {'á': 'a',
              'é': 'e',
              'í': 'i',
              'ó': 'o',
              'ú': 'u',
              'ü': 'u',
              'ñ': 'n'}
    sin_tildes = list(palabra)
    for cont in range(len(palabra)):
        letra = palabra[cont]
        if letra in tildes:
            sin_tildes[cont] = tildes[letra]
    return ''.join(sin_tildes)


def reemplazar_fonemas_similares(palabra):
    fonemas = (('y', 'i'),
               ('que', 'ke'),
               ('qui', 'ki'),
               ('ch', 'kx'),
               ('sh', 'kx'),
               ('ll', 'i'),
               ('alm', 'arm'),
               ('elm', 'erm'),
               ('ge', 'je'),
               ('gi', 'ji'),
               ('ce', 'se'),
               ('ci', 'si'),
               ('c', 'k'),
               ('z', 's'),
               ('v', 'b'),
               ('ks', 'x'),
               ('h', ''),
               ('ñ', 'n'))
    palabra = quitar_tildes(palabra)
    for fone, reemplazo in fonemas:
        palabra = palabra.replace(fone, reemplazo)
    return palabra


def similar1(w1, w2):
    similar = (
        ('a', 'c'), ('a', 'e'), ('a', 'o'),
        ('b', 'd'), ('b', 'h'), ('b', 'p'), ('b', 'q'), ('b', 'r'), ('b', 'v'),
        ('c', 'e'), ('c', 'g'), ('c', 'n'), ('c', 'o'), ('c', 'q'), ('c', 'u'),
        ('d', 'g'), ('d', 'h'), ('d', 'o'), ('d', 'p'), ('d', 'q'),
        ('e', 'f'), ('e', 'o'),
        ('f', 'i'), ('f', 'j'), ('f', 'l'), ('f', 'p'), ('f', 't'),
        ('g', 'j'), ('g', 'o'), ('g', 'p'), ('g', 'q'), ('g', 'y'),
        ('h', 'k'), ('h', 'l'), ('h', 'm'), ('h', 'n'), ('h', 'r'),
        ('i', 'j'), ('i', 'l'), ('i', 't'), ('i', 'y'),
        ('j', 'l'), ('j', 'p'), ('j', 'q'), ('j', 'y'),
        ('k', 'x'),
        ('l', 't'), ('l', 'r'),
        ('m', 'n'), ('m', 'w'),
        ('n', 'u'), ('n', 'z'), ('n', 'ñ'),
        ('o', 'p'), ('o', 'q'), ('o', 'u'), ('o', 'v'),
        ('p', 'q'), ('p', 'r'),
        ('q', 'y'),
        ('s', 'z'),
        ('u', 'v'), ('u', 'w'), ('u', 'y'),
        ('v', 'w'), ('v', 'y')
    )
    diferencias = abs(len(w1) - len(w2))
    for i in range(min(len(w1), len(w2))):
        if w1[i] != w2[i]:
            if w1[i] < w2[i]:
                pair = (w1[i], w2[i])
            else:
                pair = (w2[i], w1[i])
            if pair in similar:
                diferencias += 1
            else:
                diferencias += 2
    return diferencias


def similares(palabra1, palabra2):
    if reemplazar_fonemas_similares(palabra1) == reemplazar_fonemas_similares(palabra2):
        return True
    palabra1 = quitar_tildes(palabra1)
    palabra2 = quitar_tildes(palabra2)
    diferencias = similar1(palabra1, palabra2)
    if diferencias < 2:
        return True
    return False


def prefijo(p):
    return reemplazar_fonemas_similares(p)[:4]


def comienzos_iguales(p1, p2):
    if quitar_tildes2(p1)[:4] == quitar_tildes2(p2)[:4]:
        return True
    p1 = prefijo(p1)
    p2 = prefijo(p2)
    return p1 == p2


def buscar_conflictos(lista, palabra):
    confictos = []
    for p in lista:
        if comienzos_iguales(p, palabra) or similares(p, palabra):
            confictos.append(p)
    return confictos


def leer_lista_2048(nombre_fichero):
    return [linea.strip() for linea in open(nombre_fichero, 'r', encoding='utf-8-sig').readlines()]


class SpanishBIP39WordlistTest(unittest.TestCase):
    def test_comiezos_iguales(self):
        comienzos_similares = (
            ('hola', 'ola'),
            ('repetir', 'repecho'),
            ('vasodilatador', 'bazofia'),
            ('árbol', 'arbóreo'),
            ('piñón', 'pino'),
            ('rayar', 'rallar'),
            ('bollo', 'boyo'),
            ('picó', 'pico'),
            ('cenar', 'senado')
        )
        fallo_test = False
        for pareja in comienzos_similares:
            if not comienzos_iguales(pareja[0], pareja[1]):
                print('ERROR: "%s" y "%s" dice que no comienzan igual.' % (pareja[0], pareja[1]))
                fallo_test = True
            if not comienzos_iguales(pareja[1], pareja[0]):
                print('ERROR: "%s" y "%s" dice que no comienzan igual.' % (pareja[1], pareja[0]))
                fallo_test = True

        comienzos_diferentes = (
            ('gato', 'pato'),
            ('pollo', 'bollo'),
            ('corcho', 'corto'),
            ('chocolate', 'cocotero'),
            ('rayo', 'ralla'),
            ('yeso', 'ileso')
        )
        for pareja in comienzos_diferentes:
            if comienzos_iguales(pareja[0], pareja[1]):
                print('ERROR: "%s" y "%s" dice que comienzan igual.' % (pareja[0], pareja[1]))
                fallo_test = True
            if comienzos_iguales(pareja[1], pareja[0]):
                print('ERROR: "%s" y "%s" dice que comienzan igual.' % (pareja[1], pareja[0]))
                fallo_test = True

        self.failIf(fallo_test)

    def test_similar(self):
        palabras_similares = (
            ('hola', 'ola'),
            ('casa', 'caza'),
            ('vaso', 'bazo'),
            ('baya', 'valla'),
            ('zumo', 'sumo'),
            ('cerrar', 'serrar'),
            ('gato', 'pato'),
            ('pollo', 'bollo'),
            ('picó', 'pico'),
            ('maño', 'mano'),
            ('reno', 'remo'),
            ('zyan', 'cian'),
            ('hierro', 'yerro'),
            ('quilo', 'kilo'),
            ('chiquillo', 'chykiyo'),
            ('jinete', 'ginete'),
            ('jarra', 'garra'),
            ('kiko', 'quico'),
            ('rey', 'reí'),
            ('pupa', 'popa'),
            ('caldo', 'cardo'),
            ('colar', 'cola'),
            ('peña', 'pena'),
            ('peñón', 'penon'),
            ('pañal', 'panal'),
            ('arma', 'alma'),
            ('ñoño', 'nono'),
            ('quiosco', 'kiosko')
        )
        fallo_test = False
        for pareja in palabras_similares:
            if not similares(pareja[0], pareja[1]):
                print('ERROR: "%s" y "%s" dice que no son similares' % (pareja[0], pareja[1]))
                fallo_test = True
            if not similares(pareja[1], pareja[0]):
                print('ERROR: "%s" y "%s" dice que no son similares' % (pareja[1], pareja[0]))
                fallo_test = True

        palabras_diferentes = (
            ('armar', 'alma'),
            ('barco', 'carro'),
            ('ventana', 'casa'),
            ('gato', 'perico'),
            ('metro', 'reto'),
            ('pichón', 'pico'),
            ('pincho', 'pico'),
            ('hallar', 'vallar'),
            ('hilar', 'chillar'),
            ('chino', 'cino'),
            ('guerra', 'gerra'),
            ('gestor', 'castor'),
            ('kaki', 'cuqui'),
            ('vez', 'ver'),
            ('popa', 'pipa'),
            ('piña', 'pino'),
            ('peña', 'penas'),
            ('acceso', 'acceder'),
            ('huelo', 'huelga'),
            ('ahora', 'aorta')
        )
        for pareja in palabras_diferentes:
            if similares(pareja[0], pareja[1]):
                print('ERROR: "%s" y "%s" dice que son similares' % (pareja[0], pareja[1]))
                fallo_test = True
            if similares(pareja[1], pareja[0]):
                print('ERROR: "%s" y "%s" dice que  son similares' % (pareja[1], pareja[0]))
                fallo_test = True

        self.failIf(fallo_test)

    def test_conflicto_lista_de_palabras(self):
        fallo = False
        palabras = leer_lista_2048(os.path.join(os.path.dirname(__file__), 'wordlist') + '/spanish.txt')
        if len(palabras) != 2048:
            print('Numero de palabras (%s) no es 2048' % len(palabras))
            fallo = True

        for palabra in palabras:
            if len(palabra) > 8 or len(palabra) < 3:
                print('%s fuera de longitud' % palabra)
            conflic = buscar_conflictos(palabras, palabra)
            if conflic != [palabra]:
                print('%s entra en conflicto con %s' % (palabra, conflic))
                fallo = True
        self.failIf(fallo)


if __name__ == '__main__':
    unittest.main()
