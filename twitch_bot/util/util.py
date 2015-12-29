from PyQt4 import QtGui

def hue_65535_to_365(val_65535):
    ratio = float(val_65535) / float(65535)
    val_359 = int(359 * ratio)

    return val_359

def hue_qcolor(hue_color):
    hue = hue_65535_to_365(hue_color)
    return QtGui.QColor.fromHsv(hue, 255, 128)