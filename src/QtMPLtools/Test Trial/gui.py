# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from QtMPLtools.matplotlibwidgets import MPLsurface3D

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from tkinter import filedialog as fd
import numpy as np
import matplotlib as mpl
from matplotlib import cm


class Ui_UIFigure(object):

    def loadDataClicked(self):
        fileRequest = fd.askopenfilename(filetypes=[("CSV Files", ".csv")])

        if not fileRequest:
            return

        data = np.delete(np.genfromtxt(fileRequest, delimiter=','), 0, 0)

        phiVec = np.unique(data[:, 0])
        thetaVec = np.unique(data[:, 1])

        radPattern = np.zeros((len(thetaVec), len(phiVec)))

        k = 0
        for j in range(len(phiVec)):
            for i in range(len(thetaVec)):
                radPattern[i, j] = 20*np.log10(abs(data[k, 3] ** 2) + abs(data[k, 4] ** 2))
                k += 1

        THETA, PHI = np.meshgrid(thetaVec, phiVec)
        THETA = (np.pi / 180) * np.transpose(THETA)
        PHI = (np.pi / 180) * np.transpose(PHI)
        scalePattern = radPattern + abs(np.min(radPattern))

        XX = scalePattern * np.sin(THETA) * np.cos(PHI)
        YY = scalePattern * np.sin(THETA) * np.sin(PHI)
        ZZ = scalePattern * np.cos(THETA)

        cmap = mpl.cm.jet
        norm = mpl.colors.Normalize(vmin=np.min(radPattern), vmax=np.max(radPattern))


        self.surfPlot.axes.plot_surface(XX, YY, ZZ, cmap=cmap)
        self.cbar = self.surfPlot.figure.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=self.surfPlot.axes)
        self.surfPlot.axes.set_axis_off()

        self.surfPlot.draw()

        self.loadData.setDisabled(True)
        self.deleteData.setEnabled(True)

    def deleteDataClicked(self):
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)

        Z = np.empty((X.shape[0], X.shape[1]))
        Z[:] = np.nan

        self.surfPlot.axes.set_axis_on()
        self.surfPlot.axes.cla()
        self.cbar.remove()

        self.surfPlot.draw()

        self.loadData.setEnabled(True)
        self.deleteData.setDisabled(True)

    def setupUi(self, UIFigure):
        UIFigure.setObjectName("UIFigure")
        UIFigure.resize(375, 373)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("chamberLogo.jpg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        UIFigure.setWindowIcon(icon)
        UIFigure.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=UIFigure)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.surfPlot = MPLsurface3D(parent=self.centralwidget)
        self.surfPlot.setObjectName("surfPlot")

        self.navToolbar = NavigationToolbar(self.surfPlot, UIFigure)
        self.navToolbar.setObjectName("navtoolbar")
        self.gridLayout.addWidget(self.navToolbar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.surfPlot, 1, 0, 1, 1)

        self.loadData = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadData.setStyleSheet("background-color: rgb(160, 160, 160);\n"
                                    "font: 700 14pt \"Segoe UI\";")
        self.loadData.setObjectName("loadData")
        self.gridLayout.addWidget(self.loadData, 2, 0, 1, 1)

        self.deleteData = QtWidgets.QPushButton(parent=self.centralwidget)
        self.deleteData.setStyleSheet("background-color: rgb(160, 160, 160);\n"
                                    "font: 700 14pt \"Segoe UI\";")
        self.deleteData.setObjectName("deleteData")
        self.deleteData.setDisabled(True)
        self.gridLayout.addWidget(self.deleteData, 3, 0, 1, 1)

        UIFigure.setCentralWidget(self.centralwidget)

        self.retranslateUi(UIFigure)
        self.loadData.clicked.connect(self.loadDataClicked)
        self.deleteData.clicked.connect(self.deleteDataClicked)
        QtCore.QMetaObject.connectSlotsByName(UIFigure)

    def retranslateUi(self, UIFigure):
        _translate = QtCore.QCoreApplication.translate
        UIFigure.setWindowTitle(_translate("UIFigure", "MainWindow"))
        self.surfPlot.setTitle(_translate("UIFigure", "Radiation Pattern"))
        self.surfPlot.setXlabel(_translate("UIFigure", "X"))
        self.surfPlot.setYlabel(_translate("UIFigure", "Y"))
        self.surfPlot.setZlabel(_translate("UIFigure", "Z"))
        self.loadData.setText(_translate("UIFigure", "Load Data"))
        self.deleteData.setText(_translate("UIFigure","Delete Data"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    UIFigure = QtWidgets.QMainWindow()
    ui = Ui_UIFigure()
    ui.setupUi(UIFigure)
    UIFigure.show()
    sys.exit(app.exec())
