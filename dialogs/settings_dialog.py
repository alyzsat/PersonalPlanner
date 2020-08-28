from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QCheckBox

from dialogs.dialog import PlannerQDialog


class SettingsDialog(PlannerQDialog):
    def __init__(self, app):
        super().__init__(app, "Settings", 1)
        self.button_ok.setEnabled(True)

        themes = ["Default", "OrangeCreamsicle", "Mint", "MintLight"]
        self.old_theme = app.current_theme

        # Create widgets
        self.combobox_theme = QComboBox()
        self.combobox_theme.addItems(themes)
        self.combobox_theme.setCurrentText(self.old_theme)
        self.combobox_theme.currentIndexChanged.connect(self.test_theme)

        self.checkbox_completed = QCheckBox()
        self.checkbox_completed.setChecked(self.app.show_completed)
        self.checkbox_completed.clicked.connect(self.completed_clicked)

        # Add widgets
        self.add_widget("Theme", self.combobox_theme)
        self.add_widget("Show\nCompleted", self.checkbox_completed)

        # Set theme back if canceled
        self.rejected.connect(self.reset_theme)

    def reset_theme(self):
        self.app.set_theme(self.old_theme, self.app)
        self.app.set_theme(self.old_theme, self.app.overview_panel)

    def set_planner_theme(self, theme: str) -> None:
        self.app.set_theme(theme.lower(), self.app)
        self.app.set_theme(theme.lower(), self)
        self.app.set_theme(theme.lower(), self.app.overview_panel)

    def test_theme(self, index: int):
        theme = self.combobox_theme.itemText(index)
        self.set_planner_theme(theme)

    def ok_clicked(self):
        theme = self.combobox_theme.currentText()
        self.app.current_theme = theme
        self.accept()

    def completed_clicked(self):
        if self.checkbox_completed.isChecked():
            self.app.show_completed = True
        else:
            self.app.show_completed = False
        self.app.course_page.refresh()
