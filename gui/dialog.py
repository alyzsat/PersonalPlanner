from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt
from planner import Planner


class PlannerQDialog(QDialog):
    def __init__(self, planner: Planner, window_name: str, rows: int):
        super().__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon("logo.png"))
        self.planner = planner
        self.setWindowTitle(window_name)
        self.row_count = 0

        # Message Box
        self.message_box = QLabel()

        # Ok Button
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.ok_clicked)
        self.ok_button.setDefault(True)
        self.ok_button.setDisabled(True)

        # Cancel Button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        # Configure Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.message_box, rows + 1, 1, 1, 2)
        self.layout.addWidget(self.ok_button, rows + 2, 1)
        self.layout.addWidget(cancel_button, rows + 2, 2)
        self.setLayout(self.layout)

    def add_widget(self, text: str, widget: QWidget):
        """Add more widgets along with a label. This keeps track
        of the row count to make adding more widgets easier
        """
        self.row_count += 1
        self.layout.addWidget(QLabel(text), self.row_count, 1)
        self.layout.addWidget(widget, self.row_count, 2)

    def load_info(self, info: list) -> None:
        """Load info into fields to edit"""
        pass

    def get_info(self) -> tuple:
        """Return info from fields"""
        pass

    def check_text(self, text) -> None:
        """Disable ok button if text is empty, clear message box
        if text is empty
        """
        if text == "":
            self.message_box.clear()
        if text.strip() != "":
            self.ok_button.setDisabled(False)
        else:
            self.ok_button.setDisabled(True)

    def set_message(self, text: str):
        """Sets a message to display more info"""
        self.message_box.setText(text)

    def ok_clicked(self):
        """Implement this method"""
        pass
