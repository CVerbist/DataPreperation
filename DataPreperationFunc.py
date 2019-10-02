#!/usr/bin/env python


from matplotlib import pyplot as plt
import numpy
from matplotlib.widgets import Button, RectangleSelector


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata



def toggle_selector(event):
    print('Acquired rectangle.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)


def ExtractingData(x, y, xDel, yDel):

    if numpy.size(xDel) == 0:
        fig, axD = plt.subplots()
        plt.title(
            "Draw a rectangle with the mouse around the points you want to delete \n and press q to validate. \n You can adjust square after drawing.")
        plt.scatter(x, y)

    else:
        fig = plt.figure()

        plt.subplot(121)
        plt.scatter(x, y, 30, "b", ".", label = "Data")
        plt.scatter(xDel, yDel, 30, "r", ".", label = "Deleted Data")
        plt.legend()
        axD = plt.subplot(122)
        plt.scatter(x, y, 30, "b", ".")
        plt.suptitle(
            "Draw a rectangle with the mouse around the points you want to delete \n and press q to validate, in the right subplot. \n You can adjust square after drawing.")

    toggle_selector.RS = RectangleSelector(axD, line_select_callback,
                                           drawtype='box', useblit=False,
                                           button=[1],
                                           spancoords='pixels',
                                           interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    return toggle_selector.RS.extents  # Returns limits of rectangle, ie. [xmin, xmax, ymin, ymax]


def dataPreperation(x, y):
    class deletingData(object):
        def delData(self, event):
            plt.close()
            print("Starting the deletion program.")
            userAns['delDat'] = True

        def contRout(self, event):
            plt.close()
            print("Exiting data deletion program.")
            userAns['delDat'] = False

    userAns = {}
    xDel = []
    yDel = []

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    plt.scatter(x, y)

    callback = deletingData()
    axCont = plt.axes([0.81, 0.05, 0.1, 0.075])
    axDel = plt.axes([0.7, 0.05, 0.1, 0.075])
    bCont = Button(axCont, "Exit")
    bCont.on_clicked(callback.contRout)
    bDel = Button(axDel, "Delete")
    bDel.on_clicked(callback.delData)
    plt.show()

    while userAns['delDat']:
        rectLim = ExtractingData(x, y, xDel, yDel)
        indDel = numpy.where((x > rectLim[0]) & (x < rectLim[1]) & (y > rectLim[2]) & (y < rectLim[3]))
        xDel = numpy.append(xDel, x[indDel])
        yDel = numpy.append(yDel, y[indDel])
        x = numpy.delete(x, indDel)
        y = numpy.delete(y, indDel)
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        plt.subplot(121)
        plt.title("Original data + deleted data")
        plt.scatter(x, y, 30, "b", ".", label = "Data")
        plt.scatter(xDel, yDel, 30, "r", ".", label = "Deleted Data")
        plt.legend()
        plt.subplot(122)
        plt.title("Remaining data.")
        plt.scatter(x, y, 30, "b", ".")

        callback = deletingData()
        axCont = plt.axes([0.81, 0.05, 0.1, 0.075])
        axDel = plt.axes([0.7, 0.05, 0.1, 0.075])
        bCont = Button(axCont, "Exit")
        bCont.on_clicked(callback.contRout)
        bDel = Button(axDel, "Delete")
        bDel.on_clicked(callback.delData)

        plt.show()
        # break

    return x, y, xDel, yDel

