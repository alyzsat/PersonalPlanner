from PyQt5.QtWidgets import QLineEdit, QComboBox
from datetime import datetime
from math import floor
from custom_widgets.dialogs.dialog import PlannerQDialog


class CourseDialog(PlannerQDialog):
    def __init__(self, app, title: str):
        super().__init__(app, title, 3)
        self.old_info = None
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

    def load_info(self, info: [int, str, str, int]) -> None:
        """Loads the course name to edit course"""
        id, name, season, year = info
        self.old_info = info
        self.lineedit_name.setText(name)
        self.combobox_season.setCurrentText(season)
        self.combobox_year.setCurrentText(str(year))

    def get_info(self) -> (str, str, int):
        """Return name, season, year"""
        return self.old_info[0], \
               self.lineedit_name.text(), \
               self.combobox_season.currentText(), \
               int(self.combobox_year.currentText())

    def ok_clicked(self):
        """Check if course name already exists for creating new course, or
        edit course and change name
        """
        name = self.lineedit_name.text()
        season = self.combobox_season.currentText()
        year = self.combobox_year.currentText()
        if self.old_info is not None and name.lower() == self.old_info[1].lower():
            self.accept()
        elif self.app.planner.has_course(name, season, year):
            self.set_message("Course Already Exists")
        else:
            self.accept()
