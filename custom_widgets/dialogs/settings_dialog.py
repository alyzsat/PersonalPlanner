from PyQt5.QtWidgets import QComboBox, QCheckBox

from custom_widgets.dialogs.dialog import PlannerQDialog


class SettingsDialog(PlannerQDialog):
    def __init__(self, app):
        super().__init__(app, "Settings", 3)
        self.button_ok.setEnabled(True)

        themes = ["Default", "OrangeCreamsicle", "Mint", "MintLight"]
        self.old_theme = app.current_theme

        # Create widgets
        self.combobox_theme = QComboBox()
        self.combobox_theme.addItems(themes)
        self.combobox_theme.setCurrentText(self.old_theme)
        self.combobox_theme.currentIndexChanged.connect(self.test_theme)

        # self.combobox_term = QComboBox()
        # self.combobox_term.addItems(terms)
        # self.combobox_term.

        self.checkbox_completed = QCheckBox()
        self.checkbox_completed.setChecked(self.app.show_completed)
        self.checkbox_completed.clicked.connect(self.completed_clicked)

        self.checkbox_current = QCheckBox()
        self.checkbox_current.setChecked(self.app.show_current)
        self.checkbox_current.clicked.connect(self.current_clicked)

        self.checkbox_term_labels = QCheckBox()
        self.checkbox_term_labels.setChecked(self.app.show_term_labels)
        self.checkbox_term_labels.clicked.connect(self.term_labels_clicked)

        # Add widgets
        self.add_widget("Theme", self.combobox_theme)
        self.add_widget("Show\nCompleted", self.checkbox_completed)
        self.add_widget("Show Current\nCourses Only", self.checkbox_current)
        self.add_widget("Show Term\nLabels", self.checkbox_term_labels)

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
        self.app.show_completed = self.checkbox_completed.isChecked()
        self.app.course_page.refresh()

    def current_clicked(self):
        self.app.show_current = self.checkbox_current.isChecked()
        self.app.sidebar.refresh()

    def term_labels_clicked(self):
        self.app.show_term_labels = self.checkbox_term_labels.isChecked()
        self.app.sidebar.refresh()
