# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 15:31:17 2021

Programa para comprimir una imagen en formato .jpg con perdidas, usando 
la técnica Seam Carving.

Adaptado de un trabajo de Karthik Karanth (https://karthikkaranth.me/blog/implementing-seam-carving-with-python/)

@authors: Mariana Yepes y Hernán Moreno.

Para: Profesor Mauricio Toro, Estructura de Datos y Algoritmos.
"""

import sys

import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve

# tqdm permite visualizar una barra de progreso en la ventana de terminal

from tqdm import trange

# Calculo del mapa de energía

def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # Conversion de un filtro 2D a uno 3D, replicando el mismo filtro
    # en cada canal: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # Conversion de un filtro 2D a uno 3D, replicando el mismo filtro
    # en cada canal: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # Se suman las energias en los canales R, G y B
    energy_map = convolved.sum(axis=2)

    return energy_map

# Calculo del seam de energía mínima

def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype=np.int)

    for i in range(1, r):
        for j in range(0, c):
            # Verificar el extremo izq de la imagen para asegurar que no tengo index -1
            if j == 0:
                idx = np.argmin(M[i - 1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i - 1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack

# Remoción del seam de mínima energía

def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)

    # Crea una matriz (r, c) con el valor True
    # Luego se quitarán todos los pixels con valor False
    mask = np.ones((r, c), dtype=np.bool)

    # Encontrar la posicion del elemento menor en la ultima fila de M
    
    j = np.argmin(M[-1])

    for i in reversed(range(r)):
        # Marcar los pixels a borrar
        mask[i, j] = False
        j = backtrack[i, j]

    # Como la imagen tiene 3 canales, se convierta mask a 3D
    
    mask = np.stack([mask] * 3, axis=2)

    # Borrar todos los pixels marcados False en mask,
    # y llevar la imagen a la nueva dimensión
    
    img = img[mask].reshape((r, c - 1, 3))

    return img

# Repetición para cada columna

def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c): # usar range si no se desea usar tqdm
        img = carve_column(img)

    return img

def main():
    scale = float(sys.argv[1])
    in_filename = sys.argv[2]
    out_filename = sys.argv[3]

    img = imread(in_filename)
    out = crop_c(img, scale)
    imwrite(out_filename, out)

if __name__ == '__main__':
    main()