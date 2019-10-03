#!/usr/bin/env python
import numpy
import DataPreperationFunc as dPF

x = numpy.random.randint(1, 101, 50)
y = numpy.random.randint(1, 101, 50)

(newX, newY, xDel, yDel) = dPF.dataPreperation(x, y)

