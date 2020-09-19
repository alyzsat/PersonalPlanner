from PyQt5.QtWidgets import QLineEdit, QComboBox
from datetime import datetime
from math import floor
from personalplanner.custom_widgets.dialogs.dialog import PlannerQDialog


class CourseDialog(PlannerQDialog):
    def __init__(self, app, title: str, course_id: int = None):
        super().__init__(app, title, 4)
        y = datetime.now().year
        seasons = ["Winter", "Spring", "Summer", "Fall"]
        years = [str(year) for year in range(y + 1, y - 5, -1)]

        # Create Widgets
        self.lineedit_name = QLineEdit()
        self.lineedit_name.textChanged.connect(self.check_text)

        self.combobox_season = QComboBox()
        i = floor(datetime.now().month / 4)
        self.combobox_season.addItems(seasons)
        self.combobox_season.setCurrentIndex(i)

        self.combobox_year = QComboBox()
        self.combobox_year.addItems(years)
        self.combobox_year.setCurrentText(str(y))

        # Add the widgets to dialog
        self.add_widget("Name", self.lineedit_name)
        self.add_widget("Season", self.combobox_season)
        self.add_widget("Year", self.combobox_year)

        self.lineedit_name.setFocus()

        self.old_info = None
        if course_id is not None:
            self.load_info(course_id)

    def load_info(self, course_id: int) -> None:
        """Loads the course name to edit course"""
        self.old_info = self.app.planner.get_course(course_id)
        id, name, season, year = self.old_info
        self.lineedit_name.setText(name)
        self.combobox_season.setCurrentText(season)
        self.combobox_year.setCurrentText(str(year))

    def add_course(self, name: str, season: str, year: int) -> None:
        """Add the new course to planner"""
        self.app.planner.add_course(name, season, year)

    def save_changes(self, name: str, season: str, year: int) -> None:
        """Update the planner to reflect changes made to the course"""
        self.app.planner.update_course(self.old_info[0], "name", name)
        self.app.planner.update_course(self.old_info[0], "season", season)
        self.app.planner.update_course(self.old_info[0], "year", year)

    def ok_clicked(self) -> None:
        """Check if course name already exists for creating new course, or
        edit course and change name
        """
        name = self.lineedit_name.text()
        season = self.combobox_season.currentText()
        year = int(self.combobox_year.currentText())

        # If the course is being edited and the name is the same
        # except with capitalization changes, accept change
        # Also applies for if only the season and/or year change
        if self.old_info is not None and name.lower() == self.old_info[1].lower():
            self.save_changes(name, season, year)
            self.accept()

        # If the course name is already being used for that term, set message
        elif self.app.planner.has_course(name, season, year):
            self.set_message("Course Already Exists")

        # If the course is being edited and the name is changed to
        # an available name, update course
        elif self.old_info is not None:
            self.save_changes(name, season, year)
            self.accept()

        # Otherwise, the course is new and needs to be added
        else:
            self.add_course(name, season, year)
            self.accept()
