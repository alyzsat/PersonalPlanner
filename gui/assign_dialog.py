from PyQt5.QtWidgets import QLineEdit, QComboBox

from gui.PlannerQDialog import PlannerQDialog


class AssignmentDialog(PlannerQDialog):
    def __init__(self):
        super().__init__("Create New Assignment", 3)

        months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]

        days = [str(i+1) for i in range(31)]

        # Create Widgets
        self.name_box = QLineEdit()
        self.name_box.textChanged.connect(self.check_text)
        self.month_box = QComboBox()
        self.month_box.addItems(months)
        self.day_box = QComboBox()
        self.day_box.addItems(days)

        # Add the Widgets
        self.add_widget("Name", self.name_box)
        self.add_widget("Month", self.month_box)
        self.add_widget("Day", self.day_box)

    def check_text(self, text):
        """Disable ok button if field is empty"""
        if text.strip() != "":
            self.ok_button.setDisabled(False)
        else:
            self.ok_button.setDisabled(True)

    def get_info(self) -> (str, int, int):
        """Returns a tuple holding the name, month number, and day"""
        return self.name_box.text(), self.month_box.currentIndex(), self.day_box.currentIndex()

    def load_info(self, info: list) -> None:
        """Loads assignment information into dialog to edit"""
        name, month, day = info
        self.name_box.setText(name)
        self.month_box.setCurrentIndex(month)
        self.day_box.setCurrentIndex(day)

    def set_message(self, text: str):
        """Sets a message to display more info"""
        self.message_box.setText(text)
