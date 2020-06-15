from PyQt5.QtWidgets import QPushButton, QDialog, QLabel, QVBoxLayout


class PlannerPopUp(QDialog):
    def __init__(self, message: str):
        super().__init__()

        # Message Popup
        message_label = QLabel(message)

        # Click ok or press enter to close
        ok_button = QPushButton("Ok")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self.accept)

        # Configure Layout
        layout = QVBoxLayout()
        layout.addWidget(message_label)
        layout.addWidget(ok_button)
        self.setLayout(layout)
