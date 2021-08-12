#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 17:42:12 2021

Lee todos los archivos del directorio folder_path
En lugar del print, colocar el llamado al programa de compresión

@author: hernanmorenom
"""
import os
import pandas as pd
folder_path = "/OneDrive - Universidad EAFIT/2 SEM/Datos/proyecto/datasets/archivosCSV/ganado enfermo CSVs/"
for data_file in sorted (os.listdir(folder_path)):
    entrega1 = pd.read_csv ("/OneDrive - Universidad EAFIT/2 SEM/Datos/proyecto/datasets/archivosCSV/ganado enfermo CSVs/" + data_file)
# Aquí debe ir el llamado al algoritmo de compresión
    print (entrega1)
