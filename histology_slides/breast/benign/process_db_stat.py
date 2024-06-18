#!/usr/bin/python3
#coding: utf-8
__author__ = "Fabio Alexandre Spanhol"
__email__ = "faspanhol@gmail.com"

"""

"""

import sys
import os
from glob import glob

try:
     f = open(sys.argv[1], 'r')
except IOError:
    print("Impossible process input file.")
    sys.exit()

d = {40 :0, 
     100:0,
     200:0,
     400:0}

slides = set() #unordered collection with no duplicat elements

#malignant/SOB/ductal_carcinoma/SOB_M_DC-142985/200X : 14
# ./SOB/tubular_adenoma/SOB_B_TA-1415275/200X : 12
#SOB/phyllodes_tumor/SOB_B_PT_14-22704/200X : 42

for row in f:
    slide = row.split('/')[-2]
    magnif = row.split('/')[-1]
    k, qt = magnif.split(':')
    k = int(k.strip()[:-1])
    	
    slides.add(slide)

    d[k] += int(qt)

for k in sorted(d):
    print(k, d[k])

print('Total slides:%d' % len(slides))  
