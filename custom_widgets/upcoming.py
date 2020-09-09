from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class UpcomingAssignments(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.layout = QVBoxLayout()
        self.setup_layout()

    def setup_layout(self):
        self.layout.addWidget(QLabel())

    def refresh(self):
        pass