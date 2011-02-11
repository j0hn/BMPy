#!/usr/bin/env python
'''Graphical interface for BMPy'''

from PyQt4.QtCore import Qt, QString, SIGNAL, SLOT
from PyQt4.QtGui import *

import tempfile
import sys
import os

from bmpy import BMPy

class MainWindow(QMainWindow):
    '''Project's main window'''

    def __init__(self):
        QMainWindow.__init__(self)


        # Window settings
        self.setWindowTitle("Bmpy Editor")
        self.setWindowIcon(QIcon("images/logo.png"))
        self.resize(500, 550)
        self.center()

        # The BMPy object
        self.bmpy = None # not loaded yet
        self.filename = None
        self.tmpfilename = None

        # File Actions
        self.exitAction = QAction(QIcon("images/exit.png"), "Exit", self)
        self.openAction = QAction(QIcon("images/open.png"), "Open", self)
        self.saveAction = QAction(QIcon("images/save.png"), "Save", self)
        self.undoAction = QAction(QIcon("images/undo.png"), "Undo", self)
        self.redoAction = QAction(QIcon("images/redo.png"), "Redo", self)

        # Edit Actions
        self.blurAction = QAction(QIcon("images/blur.png"), "Blur", self)
        self.flipHAction = QAction(QIcon("images/fliph.png"), "Flip\nHorizontal", self)
        self.flipVAction = QAction(QIcon("images/flipv.png"), "Flip\nVertical", self)
        self.mosaicAction = QAction(QIcon("images/mosaic.png"), "Mosaic", self)
        self.invertAction = QAction(QIcon("images/invert.png"), "Invert", self)
        self.desaturateAction = QAction(QIcon("images/desaturate.png"), "Desaturate", self)
        self.sepiaAction = QAction(QIcon("images/sepia.png"), "Sepia", self)

        # Actions signal connections
        self.connect(self.exitAction, SIGNAL("triggered()"), SLOT("close()"))
        self.connect(self.openAction, SIGNAL("triggered()"), self.on_open)
        self.connect(self.saveAction, SIGNAL("triggered()"), self.on_save)
        self.connect(self.undoAction, SIGNAL("triggered()"), self.on_undo)
        self.connect(self.redoAction, SIGNAL("triggered()"), self.on_redo)
        self.connect(self.blurAction, SIGNAL("triggered()"), self.on_blur)
        self.connect(self.flipHAction, SIGNAL("triggered()"), self.on_fliph)
        self.connect(self.flipVAction, SIGNAL("triggered()"), self.on_flipv)
        self.connect(self.mosaicAction, SIGNAL("triggered()"), self.on_mosaic)
        self.connect(self.invertAction, SIGNAL("triggered()"), self.on_invert)
        self.connect(self.desaturateAction, SIGNAL("triggered()"), self.on_desaturate)
        self.connect(self.sepiaAction, SIGNAL("triggered()"), self.on_sepia)

        # File Toolbar
        self._fileToolbar = QToolBar()
        self.addToolBar(self._fileToolbar)
        self._fileToolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self._fileToolbar.addAction(self.openAction)
        self._fileToolbar.addAction(self.saveAction)
        self._fileToolbar.addAction(self.undoAction)
        self._fileToolbar.addAction(self.redoAction)

        # Edit Toolbar
        self._editToolbar = QToolBar()
        self.editToolbar = self.addToolBar(Qt.LeftToolBarArea, self._editToolbar)
        self._editToolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self._editToolbar.addAction(self.blurAction)
        self._editToolbar.addAction(self.desaturateAction)
        self._editToolbar.addAction(self.sepiaAction)
        self._editToolbar.addAction(self.mosaicAction)
        self._editToolbar.addAction(self.invertAction)

        # MenuBar
        menubar = self.menuBar()

        fileitem = menubar.addMenu("&File")
        fileitem.addAction(self.openAction)
        fileitem.addAction(self.saveAction)
        fileitem.addAction(self.exitAction)

        edititem = menubar.addMenu("&Edit")
        edititem.addAction(self.undoAction)
        edititem.addAction(self.redoAction)
        edititem.addAction(self.flipHAction)
        edititem.addAction(self.flipVAction)

        filtersitem = menubar.addMenu("F&ilters")
        filtersitem.addAction(self.blurAction)
        filtersitem.addAction(self.desaturateAction)
        filtersitem.addAction(self.sepiaAction)
        filtersitem.addAction(self.mosaicAction)
        filtersitem.addAction(self.invertAction)

        # Status Bar
        self.statusBar()

        # Graphics View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.setCentralWidget(self.view)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, \
                  (screen.height()-size.height())/2)

    def errorDialog(self, title, message):
        blureff = QGraphicsBlurEffect(self)
        self.setGraphicsEffect(blureff)

        QMessageBox.critical(self, title, message, QMessageBox.Ok)

        self.setGraphicsEffect(None)

    def update_image(self):
        self.scene.clear()
        image = QPixmap(self.filename)
        self.scene.addPixmap(image)

    def update_edit_image(self):
        self.scene.clear()
        self.bmpy.save_to(self.tmpfilename)
        image = QPixmap(self.tmpfilename)
        self.scene.addPixmap(image)


    def on_open(self):
        this_file_path = os.path.abspath(__file__)

        filename = QFileDialog.getOpenFileName(self, 'Open file', this_file_path)
        if filename == "": return

        try:
            self.bmpy = BMPy(filename)
            self.filename = filename
            self.tmpfilename = tempfile.mkstemp(suffix=".bmp")[1]
            self.update_image()
        except Exception, e:
            self.errorDialog("Load Error", "Error: " + str(e))

    def on_save(self):
        filename = QFileDialog.getSaveFileName(self, "Save file", self.filename)
        if filename == "": return

        self.bmpy.save_to(filename)

    def on_undo(self):
        #self.update_image()
        print "undo"

    def on_redo(self):
        #self.update_edit_image()
        print "redo"

    def on_blur(self):
        text, ok = QInputDialog.getText(self, "Blur", "Enter blur box: width, height: ")

        if ok:
            try:
                text = text.split(",")
                width = int(text[0])
                height = int(text[1])

                self.bmpy.box_blur(width, height)
                self.update_edit_image()
            except ValueError:
                self.errorDialog("Blur error",
                        "Invalid box blur format, use numbers!")
            except IndexError:
                self.errorDialog("Blur error", "Invalid blur format\n" + \
                        "You have to insert width, height")

    def on_fliph(self):
        self.bmpy.flip_horizontal()
        self.update_edit_image()

    def on_flipv(self):
        self.bmpy.flip_vertical()
        self.update_edit_image()

    def on_mosaic(self):
        text, ok = QInputDialog.getText(self, "Mosaic", "Enter the mosaic size:")

        if ok:
            try:
                self.bmpy.mosaic(int(text))
                self.update_edit_image()
            except ValueError:
               self.errorDialog("Mosaic error", "Invalid Mosaic size")

    def on_invert(self):
        self.bmpy.invert()
        self.update_edit_image()

    def on_desaturate(self):
        self.bmpy.desaturate()
        self.update_edit_image()

    def on_sepia(self):
        self.bmpy.sepia()
        self.update_edit_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = MainWindow()
    gui.show()

    sys.exit(app.exec_())
