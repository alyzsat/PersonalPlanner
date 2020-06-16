from PyQt5.QtWidgets import QComboBox

from dialogs.dialog import PlannerQDialog


class SettingsDialog(PlannerQDialog):
    def __init__(self, app):
        super().__init__(app, "Settings", 1)
        self.ok_button.setEnabled(True)

        themes = ["Default", "DefaultLight", "Mint", "MintLight"]
        self.old_theme = app.current_theme

        # Create widgets
        self.combobox_theme = QComboBox()
        self.combobox_theme.addItems(themes)
        self.combobox_theme.setCurrentText(self.old_theme)
        self.combobox_theme.currentIndexChanged.connect(self.test_theme)

        # Add widgets
        self.add_widget("Theme", self.combobox_theme)

        # Set theme back if canceled
        self.rejected.connect(self.reset_theme)

    def reset_theme(self):
        self.app.set_theme(self.old_theme)

    def set_planner_theme(self, theme: str) -> None:
        self.app.set_theme(theme.lower())

    def test_theme(self, index: int):
        theme = self.combobox_theme.itemText(index)
        self.set_planner_theme(theme)

    def ok_clicked(self):
        theme = self.combobox_theme.currentText()
        self.app.current_theme = theme
        self.accept()
