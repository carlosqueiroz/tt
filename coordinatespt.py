#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import numpy as np
import numpy.ma as ma


# Receber dados do PHP
try:
    data = json.loads(sys.argv[1])
except:
    print "ERROR"
    sys.exit(1)


# Função para calcular a rotação HFS


def get_coordinates(gantry, coll, couch, SAD):

    # Rotation no eixo X  (Collimator)
    collimator_matrix = np.matrix([[np.cos(coll), np.sin(coll), 0],
                              [np.sin(-coll), np.cos(coll), 0],
                              [0, 0, 1]])

    # Rotation no eixo Y  (couch)
    couch_matrix = np.matrix([[np.cos(couch), np.sin(couch), 0],
                              [np.sin(-couch), np.cos(couch), 0],
                              [0, 0, 1]])

    # Rotação no Eixo Z ( Gantry )
    gantry_matrix = np.matrix([[np.cos(gantry), 0, np.sin(gantry)],
                               [0, 1, 0],
                               [np.sin(gantry), 0, np.cos(gantry)]])


    #order: collimator, gantry, couch. 
    #00852 0x300A:0x012C IsocenterPosition              DS 50  [100.959176612292\52.8287469269864\-6.4116182178251]
    # Rotated Source point (1st gantry, 2nd couch)
    sourcePoint_bev = np.matrix([[40-100.959176612292, 30-52.8287469269864, -20+6.4116182178251]])
    #sourcePoint_bev = np.matrix([[40, 30, -20]])
    # projeção daria 4.0 x e 1.89 no y

    resultT = sourcePoint_bev * collimator_matrix* gantry_matrix * couch_matrix
    x1 = resultT.item(0)
    y1 = resultT.item(1)
    z =  resultT.item(2)
    X = (x1*SAD)/(SAD-z) 
    Y = (y1*SAD)/(SAD-z)
    result = np.matrix([X,Y])
    # Convertendo a matriz Nympy para lista (lista pode ser convertida em JSON)
    resultList = result.tolist()

    return resultList


# Chamando função e Passando parametros recebidos.
new_coordinates = get_coordinates(data['gantryAngle'], data['collAngle'], data[
                                  'couchAngle'], data['SAD'])


# enviando resultado para o PHP
print json.dumps(new_coordinates)
