from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QWidget


class PlannerQDialog(QDialog):
    def __init__(self, window_name: str, rows: int):
        super().__init__()
        self.row_count = 0
        self.layout = QGridLayout()

        # Default Widgets
        self.message_box = QLabel()
        self.layout.addWidget(self.message_box, rows+1, 1)
        self.ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)
        self.ok_button.setDisabled(True)
        cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.ok_button, rows+2, 1)
        self.layout.addWidget(cancel_button, rows+2, 2)

        self.setWindowTitle(window_name)
        self.setLayout(self.layout)

    def add_widget(self, text: str, widget: QWidget):
        """Add more widgets along with a label. This keeps track
        of the row count to make adding more widgets easier
        """
        self.row_count += 1
        print(text, self.row_count)
        self.layout.addWidget(QLabel(text), self.row_count, 1)
        self.layout.addWidget(widget, self.row_count, 2)

    def get_info(self) -> tuple:
        """Returns filled out fields"""
        pass

    def load_info(self, info: list) -> None:
        """Load info into fields to edit"""
        pass

    def set_message(self, text: str):
        """Sets a message to display more info"""
        self.message_box.setText(text)

    def check_text(self, text) -> None:
        """Disable ok button if text is empty"""
        if text.strip() != "":
            self.ok_button.setDisabled(False)
        else:
            self.ok_button.setDisabled(True)
