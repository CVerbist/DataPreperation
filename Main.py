#!/usr/bin/env python

import numpy
import DataPreperationFunc as dPF

# Creating random data to test deletion function

x = numpy.random.randint(1, 101, 50)
y = numpy.random.randint(1, 101, 50)

# Run the data preperation algorithm
(newX, newY, xDel, yDel) = dPF.dataPreperation(x, y)
