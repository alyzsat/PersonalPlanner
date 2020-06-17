from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel


class OverviewPanel(QVBoxLayout):
    def __init__(self, app, planner_width: int):
        super().__init__()
        self.app = app
        # self.addWidget(QLabel("Placeholder"), Qt.AlignCenter)
