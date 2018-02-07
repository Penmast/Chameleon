import math, random, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class Worker(QThread):

    def __init__(self, parent = None):

        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0
