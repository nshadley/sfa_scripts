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
        self.setWindowTitle("Scatter Tool")
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()


    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.header_lay = self._create_headers()
        self.line_edit_lay = self._line_edit_ui()
        self.line_edit_lay.addLayout(self._random_scale_ui(), 2, 1)
        self.line_edit_lay.addLayout(self._random_rotation_ui(), 3, 1)
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.line_edit_lay)
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.main_lay.addWidget(self.scatter_btn)
        self.setLayout(self.main_lay)

    def _line_edit_ui(self):
        self.scatter_what_le = QtWidgets.QLineEdit("Object to scatter")
        self.scatter_where_le = QtWidgets.QLineEdit("Where to scatter")
        layout = self._create_headers()
        layout.addWidget(self.scatter_what_le, 0, 1)
        layout.addWidget(self.scatter_where_le, 1, 1)
        return layout

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

    def _random_scale_ui(self):
        self.scale_x_lbl = QtWidgets.QLabel("x")
        self.scale_y_lbl = QtWidgets.QLabel("y")
        self.scale_z_lbl = QtWidgets.QLabel("z")
        self.scale_min_lbl = QtWidgets.QLabel("Min")
        self.scale_max_lbl = QtWidgets.QLabel("Max")
        self.scale_min_x_btn = QtWidgets.QSpinBox()
        self.scale_min_y_btn = QtWidgets.QSpinBox()
        self.scale_min_z_btn = QtWidgets.QSpinBox()
        self.scale_max_x_btn = QtWidgets.QSpinBox()
        self.scale_max_y_btn = QtWidgets.QSpinBox()
        self.scale_max_z_btn = QtWidgets.QSpinBox()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scale_x_lbl, 0, 1)
        layout.addWidget(self.scale_y_lbl, 0, 2)
        layout.addWidget(self.scale_z_lbl, 0, 3)
        layout.addWidget(self.scale_min_lbl, 1, 0)
        layout.addWidget(self.scale_max_lbl, 2, 0)
        layout.addWidget(self.scale_min_x_btn, 1, 1)
        layout.addWidget(self.scale_min_y_btn, 1, 2)
        layout.addWidget(self.scale_min_z_btn, 1, 3)
        layout.addWidget(self.scale_max_x_btn, 2, 1)
        layout.addWidget(self.scale_max_y_btn, 2, 2)
        layout.addWidget(self.scale_max_z_btn, 2, 3)
        return layout

    def _random_rotation_ui(self):
        self.rotation_x_lbl = QtWidgets.QLabel("x")
        self.rotation_y_lbl = QtWidgets.QLabel("y")
        self.rotation_z_lbl = QtWidgets.QLabel("z")
        self.rotation_min_lbl = QtWidgets.QLabel("Min")
        self.rotation_max_lbl = QtWidgets.QLabel("Max")
        self.rotation_min_x_btn = QtWidgets.QSpinBox()
        self.rotation_min_y_btn = QtWidgets.QSpinBox()
        self.rotation_min_z_btn = QtWidgets.QSpinBox()
        self.rotation_max_x_btn = QtWidgets.QSpinBox()
        self.rotation_max_y_btn = QtWidgets.QSpinBox()
        self.rotation_max_z_btn = QtWidgets.QSpinBox()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rotation_x_lbl, 0, 1)
        layout.addWidget(self.rotation_y_lbl, 0, 2)
        layout.addWidget(self.rotation_z_lbl, 0, 3)
        layout.addWidget(self.rotation_min_lbl, 1, 0)
        layout.addWidget(self.rotation_max_lbl, 2, 0)
        layout.addWidget(self.rotation_min_x_btn, 1, 1)
        layout.addWidget(self.rotation_min_y_btn, 1, 2)
        layout.addWidget(self.rotation_min_z_btn, 1, 3)
        layout.addWidget(self.rotation_max_x_btn, 2, 1)
        layout.addWidget(self.rotation_max_y_btn, 2, 2)
        layout.addWidget(self.rotation_max_z_btn, 2, 3)
        return layout
