from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()


    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.header_lay = self._create_headers()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.header_lay)
        self.setLayout(self.main_lay)

    def _create_headers(self):
        self.scatter_what_header_lbl = QtWidgets.QLabel("Scatter What")
        self.scatter_where_header_lbl = QtWidgets.QLabel("Scatter Where")
        self.random_scale_header_lbl = QtWidgets.QLabel("Random Scale")
        self.random_rotation_header_lbl = QtWidgets.QLabel("Random Rotation")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_what_header_lbl, 0, 0)
        layout.addWidget(self.scatter_where_header_lbl, 1, 0)
        layout.addWidget(self.random_scale_header_lbl, 2, 0)
        layout.addWidget(self.random_rotation_header_lbl, 3, 0)
        return layout
