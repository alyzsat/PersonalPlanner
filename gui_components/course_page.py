from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QDateEdit, \
    QLabel

from custom_widgets.data_label import DataLabel
from custom_widgets.dialogs.assign_dialog import AssignmentDialog
from custom_widgets.dialogs.course_dialog import CourseDialog
from custom_widgets.dialogs.settings_dialog import SettingsDialog


class CoursePage(QWidget):
    def __init__(self, app, width: int):
        super().__init__()
        self.app = app
        self.setFixedWidth(width)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Initialize Widgets
        self.tablewidget_assignments = QTableWidget()
        self.label_current_course = DataLabel("")
        self.button_course_options = QPushButton()
        self.button_add_assign = QPushButton()
        self.button_settings = QPushButton()

        # Sizes for Widgets
        size_add_assign = int(width / 4)
        size_course_options = int(width / 10)
        size_settings = int(width / 8)
        size_assignments = width

        # Create course bar sublayout and add to layout
        course_bar = QHBoxLayout()
        self.layout.addLayout(course_bar)

        # Add Widgets
        course_bar.addWidget(self.label_current_course)
        course_bar.addWidget(self.button_course_options)
        course_bar.addStretch()
        course_bar.addWidget(self.button_add_assign)
        course_bar.addWidget(self.button_settings)
        self.layout.addWidget(self.tablewidget_assignments)

        # Configure Widgets
        self.setFixedWidth(int(9 * width / 10))
        self.setup_assignments(size_assignments)
        self.setup_current_course()
        self.setup_course_options(size_course_options)
        self.setup_add_assignment(size_add_assign)
        self.setup_settings(size_settings)

    def setup_current_course(self) -> None:
        """Label placed at the top of the window to represent
        the current course to display
        """
        self.label_current_course.setObjectName("LabelCourseName")

    def setup_course_options(self, width: int) -> None:
        """Button that, when clicked, opens a dialog to edit
        the course name
        """
        self.button_course_options.setFixedWidth(width)
        self.button_course_options.setObjectName("CourseOptions")
        self.button_course_options.setCursor(Qt.PointingHandCursor)

        # Moved connection to PersonalPlanner to be able to refresh the sidebar
        # self.button_course_options.clicked.connect(self.course_options_clicked)

    def setup_settings(self, width: int):
        self.button_settings.setObjectName("Settings")
        self.button_settings.setText("Settings")
        self.button_settings.setCursor(Qt.PointingHandCursor)
        self.button_settings.setFixedWidth(width)
        self.button_settings.clicked.connect(self.settings_clicked)

    def setup_assignments(self, width: int) -> None:
        """QListWidget that displays all of the assignments for
        the current course that is selected
        """
        self.tablewidget_assignments.setObjectName("Assignments")
        self.tablewidget_assignments.verticalHeader().hide()
        self.tablewidget_assignments.horizontalHeader().hide()
        self.tablewidget_assignments.itemChanged.connect(self.item_changed)
        self.tablewidget_assignments.setColumnCount(5)
        self.tablewidget_assignments.setColumnWidth(0, int(width / 20))
        self.tablewidget_assignments.setColumnWidth(1, int(3 * width / 7))
        self.tablewidget_assignments.setColumnWidth(2, int(width / 9))
        self.tablewidget_assignments.setColumnWidth(3, int(width / 8))
        self.tablewidget_assignments.setColumnWidth(4, int(width / 12))

    def setup_add_assignment(self, width: int) -> None:
        """Button that, when clicked, opens a dialog to add
        a new assignment to the current course
        """
        if self.app.planner.is_empty():
            self.button_add_assign.setDisabled(True)
        self.button_add_assign.setFixedWidth(width)
        self.button_add_assign.setText("Add Assignment +")
        self.button_add_assign.setCursor(Qt.PointingHandCursor)
        self.button_add_assign.clicked.connect(self.add_assignment_clicked)

    def refresh(self):
        """Refreshes the list of assignments for the current or
        newly selected course. Also changes the course name at
        the top of the page if the course has changed.
        """
        self.tablewidget_assignments.clear()
        if self.app.planner.is_empty():
            self._enable_course_page(False)
        else:
            self._enable_course_page(True)
            self.tablewidget_assignments.disconnect()
            current_course = self.app.planner.get_current_course()

            assignments = self.app.planner.get_assignments(current_course[0], self.app.show_completed)
            n_items = len(assignments)
            self.tablewidget_assignments.setRowCount(n_items)

            for i in range(n_items):
                _id, _name, _course, _completed, _due_date = assignments[i]

                # Completed Column
                completed = QTableWidgetItem()
                completed.setCheckState(2 if _completed else 0)
                self.tablewidget_assignments.setItem(i, 0, completed)

                # Name Column
                name = DataLabel(_name)
                name.setObjectName("AssignmentLabel")
                name.set_data(_id)
                self.tablewidget_assignments.setCellWidget(i, 1, name)

                # Due Date Column
                y, m, d = _due_date.split("-")
                due_date = QLabel(f"{m}/{d}")
                due_date.setObjectName("AssignmentLabel")
                self.tablewidget_assignments.setCellWidget(i, 2, due_date)

                # Edit Column
                edit = QPushButton("•••")
                edit.setObjectName("AssignmentEdit")
                edit.setCursor(Qt.PointingHandCursor)
                edit.clicked.connect(lambda clicked, id=_id: self.update_assignment(id))
                self.tablewidget_assignments.setCellWidget(i, 3, edit)

                # Delete Column
                delete = QPushButton("x")
                delete.setObjectName("AssignmentDelete")
                delete.setCursor(Qt.PointingHandCursor)
                delete.clicked.connect(lambda clicked, id=_id: self.delete_assignment(id))
                self.tablewidget_assignments.setCellWidget(i, 4, delete)

            self.tablewidget_assignments.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QTableWidgetItem):
        """Update the planner to mark whether or not the assignment
        is completed
        """
        assignment_id = int(self.tablewidget_assignments.cellWidget(item.row(), 1).get_data())

        # If the checkbox is checked / Unchecked
        if item.column() == 0:
            self.app.planner.update_assignment(assignment_id, "completed", int(item.checkState() == 2))
            self.refresh()

    def update_assignment(self, assignment_id: int):
        """Open the assignment dialog to update the assignment name and/or due date"""
        dialog = AssignmentDialog(self.app, "Edit Assignment: ", assignment_id)
        dialog.exec_()
        self.refresh()

    def delete_assignment(self, assignment_id: int):
        """Deletes the assignment from the planner"""
        self.app.planner.delete_assignment(assignment_id)
        self.refresh()

    def course_options_clicked(self):
        """Opens a dialog to edit the course name"""
        dialog = CourseDialog(self.app, f"Edit Course", self.label_current_course.get_data())
        dialog.exec_()
        self.refresh()

    def add_assignment_clicked(self):
        """Called when Add Assignment button is clicked, adds a
        new assignment to the current course
        """
        dialog = AssignmentDialog(self.app, "Create New Assignment")
        dialog.exec_()
        self.refresh()

    def settings_clicked(self):
        """Called when the Settings button is clicked, opens
        a QDialog box to change program settings
        """
        dialog = SettingsDialog(self.app)
        dialog.exec_()

    def _enable_course_page(self, enable: bool):
        """Show course label and settings button and enable add
        assignment button
        """
        if enable:
            id, name, _, _ = self.app.planner.get_current_course()
            self.label_current_course.setText(name)
            self.label_current_course.set_data(id)
            self.button_course_options.setText("•••")
        else:
            self.label_current_course.setText("")
            self.label_current_course.set_data(-1)
            self.button_course_options.setText("")

        self.button_add_assign.setEnabled(enable)
        self.button_course_options.setEnabled(enable)
