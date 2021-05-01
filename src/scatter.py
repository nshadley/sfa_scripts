from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
import random

random.seed(1234)


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
        self.scattertool = ScatterTool()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.header_lay = self._create_headers()
        self.percent_lay = self._percent_vertices_ui()
        self.normal_lay = self._normal_checkbox_ui()
        self.line_edit_lay = self._line_edit_ui()
        self.select_btn_lay = self._create_select_buttons()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.select_btn_lay)
        self.main_lay.addLayout(self.percent_lay)
        self.main_lay.addLayout(self.normal_lay)
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.main_lay.addWidget(self.scatter_btn)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter)
        self.select_what_btn.clicked.connect(self._select_what)
        self.select_where_objects_btn.clicked.connect(self._select_where_object)
        self.select_where_vertices_btn.clicked.connect(self._select_where_vertices)
        self.select_where_obj_vert_btn.clicked.connect(self._select_where_obj_vert)

    @QtCore.Slot()
    def _scatter(self):
        self._set_scattertool_properties_from_ui()
        self.scattertool.scatter_each()

    @QtCore.Slot()
    def _select_what(self):
        selected_obj = cmds.ls(selection=True, transforms=True)
        self.scatter_what_le.setText(selected_obj[0])

    @QtCore.Slot()
    def _select_where_object(self):
        selected_obj = cmds.ls(selection=True, transforms=True)
        self.scatter_where_lw.clear()
        self.scattertool.vertices_selected = False
        for sel_obj in selected_obj:
            self.scatter_where_lw.addItem(sel_obj)

    @QtCore.Slot()
    def _select_where_vertices(self):
        selection = cmds.ls(selection=True, flatten=True)
        selected_verts = cmds.polyListComponentConversion(selection, toVertex=True)
        selected_verts = cmds.filterExpand(selected_verts, selectionMask=31)
        self.scatter_where_lw.clear()
        self.scattertool.vertices_selected = True
        for vert in selected_verts:
            self.scatter_where_lw.addItem(vert)

    @QtCore.Slot()
    def _select_where_obj_vert(self):
        selection = cmds.ls(selection=True, flatten=True)
        selected_verts = cmds.polyListComponentConversion(selection, toVertex=True)
        selected_verts = cmds.filterExpand(selected_verts, selectionMask=31)
        self.scatter_where_lw.clear()
        self.scatterool.vertices_selected = True
        for vert in selected_verts:
            self.scatter_where_lw.addItem(vert)

    def _set_scattertool_properties_from_ui(self):
        self.scattertool.selected_object = self.scatter_what_le.text()
        items = []
        for x in range(self.scatter_where_lw.count()):
            items.append(self.scatter_where_lw.item(x).text())
        self.scattertool.selected_location = items
        self.scattertool.scale_x_min = self.scale_min_x_btn.value()
        self.scattertool.scale_y_min = self.scale_min_y_btn.value()
        self.scattertool.scale_z_min = self.scale_min_z_btn.value()
        self.scattertool.scale_x_max = self.scale_max_x_btn.value()
        self.scattertool.scale_y_max = self.scale_max_y_btn.value()
        self.scattertool.scale_z_max = self.scale_max_z_btn.value()
        self.scattertool.rotation_x_min = self.rotation_min_x_btn.value()
        self.scattertool.rotation_y_min = self.rotation_min_y_btn.value()
        self.scattertool.rotation_z_min = self.rotation_min_z_btn.value()
        self.scattertool.rotation_x_max = self.rotation_max_x_btn.value()
        self.scattertool.rotation_y_max = self.rotation_max_y_btn.value()
        self.scattertool.rotation_z_max = self.rotation_max_z_btn.value()
        self.scattertool.normal_aligned = self.normal_chbx.isChecked()
        self.scattertool.percent_to_scatter = self.percent_sbx.value()
        self.scattertool.location_x_max = self.location_max_x_btn.value()
        self.scattertool.location_y_max = self.location_max_y_btn.value()
        self.scattertool.location_z_max = self.location_max_z_btn.value()
        self.scattertool.location_x_min = self.location_min_x_btn.value()
        self.scattertool.location_y_min = self.location_min_y_btn.value()
        self.scattertool.location_z_min = self.location_min_z_btn.value()

    def _line_edit_ui(self):
        self.scatter_what_le = QtWidgets.QLineEdit("Object to scatter")
        self.scatter_where_lw = QtWidgets.QListWidget()
        layout = self._create_headers()
        layout.addWidget(self.scatter_what_le, 0, 1)
        layout.addWidget(self.scatter_where_lw, 1, 1)
        return layout

    def _percent_vertices_ui(self):
        self.percent_lbl = QtWidgets.QLabel("Percent to Scatter")
        self.percent_lbl.setStyleSheet("font: bold")
        self.percent_sbx = QtWidgets.QSpinBox()
        self.percent_sbx.setRange(1, 100)
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.percent_lbl, self.percent_sbx)
        return layout

    def _normal_checkbox_ui(self):
        self.normal_header_lbl = QtWidgets.QLabel("Align to normals?")
        self.normal_header_lbl.setStyleSheet("font: bold")
        self.normal_chbx = QtWidgets.QCheckBox()
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.normal_header_lbl, self.normal_chbx)
        return layout

    def _random_location_ui(self):
        self.location_x_lbl = QtWidgets.QLabel("x")
        self.location_y_lbl = QtWidgets.QLabel("y")
        self.location_z_lbl = QtWidgets.QLabel("z")
        self.location_min_lbl = QtWidgets.QLabel("Min")
        self.location_max_lbl = QtWidgets.QLabel("Max")
        self.location_min_x_btn = QtWidgets.QDoubleSpinBox()
        self.location_min_x_btn.setRange(-100, 100)
        self.location_min_y_btn = QtWidgets.QDoubleSpinBox()
        self.location_min_y_btn.setRange(-100, 100)
        self.location_min_z_btn = QtWidgets.QDoubleSpinBox()
        self.location_min_z_btn.setRange(-100, 100)
        self.location_max_x_btn = QtWidgets.QDoubleSpinBox()
        self.location_max_x_btn.setRange(-100, 100)
        self.location_max_y_btn = QtWidgets.QDoubleSpinBox()
        self.location_max_y_btn.setRange(-100, 100)
        self.location_max_z_btn = QtWidgets.QDoubleSpinBox()
        self.location_max_z_btn.setRange(-100, 100)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.location_x_lbl, 0, 1)
        layout.addWidget(self.location_y_lbl, 0, 2)
        layout.addWidget(self.location_z_lbl, 0, 3)
        layout.addWidget(self.location_min_lbl, 1, 0)
        layout.addWidget(self.location_max_lbl, 2, 0)
        layout.addWidget(self.location_min_x_btn, 1, 1)
        layout.addWidget(self.location_min_y_btn, 1, 2)
        layout.addWidget(self.location_min_z_btn, 1, 3)
        layout.addWidget(self.location_max_x_btn, 2, 1)
        layout.addWidget(self.location_max_y_btn, 2, 2)
        layout.addWidget(self.location_max_z_btn, 2, 3)
        return layout

    def _create_headers(self):
        self.scatter_what_header_lbl = QtWidgets.QLabel("Scatter What")
        self.scatter_what_header_lbl.setStyleSheet("font: bold")
        self.scatter_where_header_lbl = QtWidgets.QLabel("Scatter Where")
        self.scatter_where_header_lbl.setStyleSheet("font: bold")
        self.random_scale_header_lbl = QtWidgets.QLabel("Random Scale")
        self.random_scale_header_lbl.setStyleSheet("font: bold")
        self.random_rotation_header_lbl = QtWidgets.QLabel("Random Rotation")
        self.random_rotation_header_lbl.setStyleSheet("font: bold")
        self.random_location_header_lbl = QtWidgets.QLabel("Random Location Offset")
        self.random_location_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_what_header_lbl, 0, 0)
        layout.addWidget(self.scatter_where_header_lbl, 1, 0)
        layout.addWidget(self.random_scale_header_lbl, 2, 0)
        layout.addWidget(self.random_rotation_header_lbl, 3, 0)
        layout.addWidget(self.random_location_header_lbl, 4, 0)
        return layout

    def _create_select_buttons(self):
        self.select_what_btn = QtWidgets.QPushButton("Selected Object")
        layout = self._line_edit_ui()
        layout.addWidget(self.select_what_btn, 0, 2)
        layout.addLayout(self._create_select_where_buttons(), 1, 2)
        layout.addLayout(self._random_scale_ui(), 2, 1)
        layout.addLayout(self._random_rotation_ui(), 3, 1)
        layout.addLayout(self._random_location_ui(), 4, 1)
        return layout

    def _create_select_where_buttons(self):
        self.select_where_objects_btn = QtWidgets.QPushButton("Selected Object(s)")
        self.select_where_vertices_btn = QtWidgets.QPushButton("Selected Vertices")
        self.select_where_obj_vert_btn = QtWidgets.QPushButton("Vertices on Selected Object(s)")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.select_where_objects_btn, 0, 0)
        layout.addWidget(self.select_where_vertices_btn, 1, 0)
        layout.addWidget(self.select_where_obj_vert_btn, 2, 0)
        return layout

    def _random_scale_ui(self):
        self.scale_x_lbl = QtWidgets.QLabel("x")
        self.scale_y_lbl = QtWidgets.QLabel("y")
        self.scale_z_lbl = QtWidgets.QLabel("z")
        self.scale_min_lbl = QtWidgets.QLabel("Min")
        self.scale_max_lbl = QtWidgets.QLabel("Max")
        self.scale_min_x_btn = QtWidgets.QDoubleSpinBox()
        self.scale_min_x_btn.setRange(0.1, 100)
        self.scale_min_y_btn = QtWidgets.QDoubleSpinBox()
        self.scale_min_y_btn.setRange(0.1, 100)
        self.scale_min_z_btn = QtWidgets.QDoubleSpinBox()
        self.scale_min_z_btn.setRange(0.1, 100)
        self.scale_max_x_btn = QtWidgets.QDoubleSpinBox()
        self.scale_max_x_btn.setRange(0.1, 100)
        self.scale_max_y_btn = QtWidgets.QDoubleSpinBox()
        self.scale_max_y_btn.setRange(0.1, 100)
        self.scale_max_z_btn = QtWidgets.QDoubleSpinBox()
        self.scale_max_z_btn.setRange(0.1, 100)
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
        self.rotation_min_x_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_min_x_btn.setRange(0, 360)
        self.rotation_min_y_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_min_y_btn.setRange(0, 360)
        self.rotation_min_z_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_min_z_btn.setRange(0, 360)
        self.rotation_max_x_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_max_x_btn.setRange(0, 360)
        self.rotation_max_y_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_max_y_btn.setRange(0, 360)
        self.rotation_max_z_btn = QtWidgets.QDoubleSpinBox()
        self.rotation_max_z_btn.setRange(0, 360)
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


class ScatterTool(object):
    """Gets an object and place to scatter and gives random rotation and scale to them"""

    def __init__(self):
        self.selected_object = "pCube1"
        self.selected_location = ["pCube1"]
        self.scale_x_min = 1.0
        self.scale_y_min = 1.0
        self.scale_z_min = 1.0
        self.scale_x_max = 10.0
        self.scale_y_max = 10.0
        self.scale_z_max = 10.0
        self.rotation_x_min = 0.0
        self.rotation_y_min = 0.0
        self.rotation_z_min = 0.0
        self.rotation_x_max = 360.0
        self.rotation_y_max = 360.0
        self.rotation_z_max = 360.0
        self.percent_to_scatter = 100
        self.normal_aligned = False
        self.location_x_min = 0.0
        self.location_y_min = 0.0
        self.location_z_min = 0.0
        self.location_x_max = 0.0
        self.location_y_max = 0.0
        self.location_z_max = 0.0
        self.x_location_offset = 0.0
        self.y_location_offset = 0.0
        self.z_location_offset = 0.0
        self.vertices_selected = True

    def create(self, scatter_location):
        instance_object = cmds.instance(self.selected_object, name=self.selected_object)
        self.get_xyz_location(scatter_location)
        cmds.move(self.x_location, self.y_location, self.z_location, instance_object)
        if self.normal_aligned:
            constraint = cmds.normalConstraint(scatter_location, instance_object, aimVector=[0.0, 1.0, 0.0])
            #cmds.delete(constraint)
        self.randomize()
        cmds.scale(self.scale_x, self.scale_y, self.scale_z, instance_object)
        cmds.rotate(self.rotation_x, self.rotation_y, self.rotation_z, instance_object)
        cmds.move(self.x_location + self.x_location_offset, self.y_location + self.y_location_offset,
                  self.z_location + self.z_location_offset, instance_object)

    def randomize(self):
        """Randomizes the scale, rotation, and location within the range"""
        self.scale_x = random.uniform(self.scale_x_min, self.scale_x_max)
        self.scale_y = random.uniform(self.scale_y_min, self.scale_y_max)
        self.scale_z = random.uniform(self.scale_z_min, self.scale_z_max)
        self.rotation_x = random.uniform(self.rotation_x_min, self.rotation_x_max)
        self.rotation_y = random.uniform(self.rotation_y_min, self.rotation_y_max)
        self.rotation_z = random.uniform(self.rotation_z_min, self.rotation_z_max)
        self.x_location_offset = random.uniform(self.location_x_min, self.location_x_max)
        self.y_location_offset = random.uniform(self.location_y_min, self.location_y_max)
        self.y_location_offset = random.uniform(self.location_z_min, self.location_z_max)

    def get_xyz_location(self, location):
        if(self.vertices_selected):
            pointPos = cmds.pointPosition(location)
            self.x_location = pointPos[0]
            self.y_location = pointPos[1]
            self.z_location = pointPos[2]
        else:
            self.x_location = cmds.getAttr(location + ".translateX")
            self.y_location = cmds.getAttr(location + ".translateY")
            self.z_location = cmds.getAttr(location + ".translateZ")


    def scatter_each(self):
        multiplier = self.percent_to_scatter/100.0
        amount = int(round(len(self.selected_location) * multiplier))
        selected_verts = random.sample(self.selected_location, k=amount)
        for location in selected_verts:
            self.create(location)
