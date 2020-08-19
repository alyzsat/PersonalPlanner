from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget

from dialogs.assign_dialog import AssignmentDialog
from dialogs.course_dialog import CourseDialog
from dialogs.popup import PlannerPopUp
from dialogs.settings_dialog import SettingsDialog
from planner_parts.assignment import Assignment


class CoursePage(QWidget):
    def __init__(self, app, width: int):
        super().__init__()
        self.app = app
        self.setFixedWidth(width)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 50)
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        # Initialize Widgets
        self.tablewidget_assignments = QTableWidget()
        self.label_current_course = QLabel()
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
        self.button_course_options.setText("•••")
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
        self.tablewidget_assignments.setColumnCount(4)
        self.tablewidget_assignments.setColumnWidth(0, int(width / 10))
        self.tablewidget_assignments.setColumnWidth(1, int(11 * width / 20))
        self.tablewidget_assignments.setColumnWidth(2, int(width / 5))
        self.tablewidget_assignments.setColumnWidth(3, 1)

    def setup_add_assignment(self, width: int) -> None:
        """Button that, when clicked, opens a dialog to add
        a new assignment to the current course
        """
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
            self.label_current_course.setText("")
        else:
            self.tablewidget_assignments.disconnect()
            current_course = self.app.planner.get_current_course()
            self.label_current_course.setText(current_course.name())

            if self.app.show_completed:
                assignments = current_course.assignments()
            else:
                assignments = current_course.incomplete_assignments()

            n_items = len(assignments)
            self.tablewidget_assignments.setRowCount(n_items)

            for i in range(n_items):
                assignment = assignments[i]

                completed = QTableWidgetItem()
                completed.setCheckState(2 if assignment.is_completed() else 0)
                self.tablewidget_assignments.setItem(i, 0, completed)

                name = QTableWidgetItem(assignment.name())
                self.tablewidget_assignments.setItem(i, 1, name)

                due_date = QTableWidgetItem(f"{assignment.due_date()[0]}/{assignment.due_date()[1]}")
                self.tablewidget_assignments.setItem(i, 2, due_date)

                # Item ID
                item_id = QTableWidgetItem(str(assignment.get_id()))
                self.tablewidget_assignments.setItem(i, 3, item_id)

            self.tablewidget_assignments.itemChanged.connect(self.item_changed)

    def item_changed(self, item: QTableWidgetItem):
        """Update the planner to mark whether or not the assignment
        is completed
        """
        item_id = int(self.tablewidget_assignments.item(item.row(), 3).text())
        original_assignment = self.app.planner.get_current_course().find_assignment(item_id)

        # If the checkbox is checked
        if item.column() == 0:
            course_name = self.app.planner.get_current_course().name()
            status = True if item.checkState() == 2 else False
            original_assignment.mark_complete(status)

        # If the assignment name changes
        elif item.column() == 1:
            self.update_name(item, original_assignment)

        # If the date changes
        elif item.column() == 2:
            self.update_date(item, original_assignment)

    def update_name(self, item: QTableWidgetItem, original_assignment: Assignment):
        """If the assignment name was changed, update the planner to reflect
        the changes. If the assignment name is already in use, show a
        popup stating that.
        """
        new_name = item.text()

        # Change back to original name if assignment name already exists
        if self.app.planner.get_current_course().has_assignment(new_name):
            PlannerPopUp(self.app, "Error", "Assignment name already in use").show()

            name = original_assignment.name()
            # Prevent duplicate popup from showing when assignment name
            # is changed back
            self.tablewidget_assignments.itemChanged.disconnect()
            self.tablewidget_assignments.item(item.row(), item.column()).setText(name)
            self.tablewidget_assignments.itemChanged.connect(self.item_changed)

        # Otherwise, save new name into planner
        else:
            original_assignment.change_name(new_name)

    def update_date(self, item: QTableWidgetItem, original_assignment: Assignment):
        """Update the date for the assignment if the date seems valid"""
        original_due_date = original_assignment.due_date()
        date_str = item.text()
        regex = QRegExp("[01]?\d/[0123]?\d")
        validator = QRegExpValidator(regex)

        # If the date string seems like an acceptable date, save to planner
        if validator.validate(date_str, 0)[0] == 2:
            month, day = date_str.split("/")
            original_assignment.change_due_date(int(month), int(day))

        # Otherwise, change the date back to the original date
        else:
            # Show popup bubble stating invalid date error
            PlannerPopUp(self.app, "Error", "Invalid date").show()

            original_date_str = f"{original_due_date[0]}/{original_due_date[1]}"
            self.tablewidget_assignments.item(item.row(), item.column()).setText(original_date_str)

    def course_options_clicked(self):
        """Opens a dialog to edit the course name"""
        current_course_name = self.label_current_course.text()
        dialog = CourseDialog(self.app, f"Edit Course: {current_course_name}")
        dialog.load_info(current_course_name)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            new_name = dialog.get_info()
            self.app.planner.change_course_name(current_course_name, new_name)
            self.label_current_course.setText(new_name)

    def add_assignment_clicked(self):
        """Called when Add Assignment button is clicked, adds a
        new assignment to the current course
        """
        current_course = self.app.planner.get_current_course()
        dialog = AssignmentDialog(self.app, current_course.name(), "Create New Assignment")
        ok_clicked = dialog.exec_()

        if ok_clicked:
            name, month, day = dialog.get_info()
            current_course.add_assignment(name, int(month), int(day))
            self.refresh()

    def settings_clicked(self):
        """Called when the Settings button is clicked, opens
        a QDialog box to change program settings
        """
        dialog = SettingsDialog(self.app)
        dialog.exec_()
