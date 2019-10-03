#!/usr/bin/env python

from matplotlib import pyplot as plt
import numpy
from matplotlib.widgets import Button, RectangleSelector


def lineSelectCallback(eClick, eRelease):
    """
    Gets the x,y coordinates of the click and release
    :param eClick: Click event
    :param eRelease: Release event
    """
    x1, y1 = eClick.xdata, eClick.ydata
    x2, y2 = eRelease.xdata, eRelease.ydata


def toggleSelector(event):
    """
    Pressing "q" will exit the selection procedure and take the drawn rectangle.
    If no rectangle is drawn it will return (0, 0, 0, 1) resulting in no points being deleted
    """
    print('Acquired rectangle.')
    if event.key in ['Q', 'q'] and toggleSelector.RS.active:
        toggleSelector.RS.set_active(False)


def extractingData(x, y, xDel, yDel):
    """
    Method that will let you draw a square around the data you want to delete.
    It will also show you the already deleted data if there is any.
    :param x: remaining x-values of data points
    :param y: remaining y-values of data points
    :param xDel: x-values of already deleted points
    :param yDel: y-values of already deleted points
    :return: limits of rectangle, ie. [xmin, xmax, ymin, ymax]
    """
    if numpy.size(xDel) == 0:
        fig, axD = plt.subplots(figsize=(8, 6))
        plt.title(
            "Draw a rectangle with the mouse around the points you want to delete \n and press q to validate. \n You can adjust square after drawing.")
        plt.scatter(x, y)

    else:
        plt.figure(figsize=(8, 6))

        ax = plt.subplot(121)
        plt.scatter(x, y, 50, "b", ".", label="Data")
        plt.scatter(xDel, yDel, 50, "r", ".", label="Deleted Data")
        # Put a legend to the bottom of the current axis
        ax.legend(loc='center right', bbox_to_anchor=(0.8, -0.10))
        axD = plt.subplot(122)
        plt.scatter(x, y, 50, "b", ".")
        plt.suptitle(
            "Draw a rectangle with the mouse around the points you want to delete \n and press q to validate, in the right subplot. \n You can adjust square after drawing.")

    toggleSelector.RS = RectangleSelector(axD, lineSelectCallback,
                                           drawtype='box', useblit=False,
                                           button=[1],
                                           spancoords='pixels',
                                           interactive=True)
    plt.connect('key_press_event', toggleSelector)  # Connecting the "q" key to exit the drawing of the rectangle
    plt.show()
    return toggleSelector.RS.extents


def dataPreperation(x, y):
    """
    Main method that will determine which points are within the selected area
    and subsequently delete them.
    :param x: x-values of the data
    :param y: y-values of the data
    :return: Remaining x, y values and the deleted x, values
    """

    # Determines behavior of buttons, ie. continue with deleting or exit
    class DeletingData(object):
        def delData(self, event):
            plt.close()
            print("Starting the deletion program.")
            userAns['delDat'] = True

        def contRout(self, event):
            plt.close()
            print("Exiting data deletion program.")
            userAns['delDat'] = False

    userAns = {}  # Used to store whether to continue or stop deleting points
    xDel = []
    yDel = []

    plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.2)

    plt.scatter(x, y)

    callback = DeletingData()

    # Creating physical location of button

    axCont = plt.axes([0.81, 0.05, 0.1, 0.075])
    axDel = plt.axes([0.7, 0.05, 0.1, 0.075])
    bCont = Button(axCont, "Exit")
    bCont.on_clicked(callback.contRout)
    bDel = Button(axDel, "Delete")
    bDel.on_clicked(callback.delData)
    plt.show()

    while userAns['delDat']:
        rectLim = extractingData(x, y, xDel, yDel)

        # Checking which points are within the drawn rectangle and subsequently delete them
        indDel = numpy.where((x > rectLim[0]) & (x < rectLim[1]) & (y > rectLim[2]) & (y < rectLim[3]))
        xDel = numpy.append(xDel, x[indDel])
        yDel = numpy.append(yDel, y[indDel])
        x = numpy.delete(x, indDel)
        y = numpy.delete(y, indDel)

        plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)
        ax = plt.subplot(121)
        plt.title("Original deleted data")
        plt.scatter(x, y, 50, "b", ".", label="Data")
        plt.scatter(xDel, yDel, 50, "r", "x", label="Deleted Data")
        # Put a legend to the bottom of the current axis
        ax.legend(loc='center right', bbox_to_anchor=(0.8, -0.15))
        plt.subplot(122)
        plt.title("Remaining data")
        plt.scatter(x, y, 50, "b", ".")

        callback = DeletingData()
        axCont = plt.axes([0.81, 0.05, 0.1, 0.075])
        axDel = plt.axes([0.7, 0.05, 0.1, 0.075])
        bCont = Button(axCont, "Exit")
        bCont.on_clicked(callback.contRout)
        bDel = Button(axDel, "Delete")
        bDel.on_clicked(callback.delData)

        plt.show()

    return x, y, xDel, yDel

