from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QComboBox, QFrame
from PyQt5.QtCore import Qt


class PlannerQDialog(QDialog):
    def __init__(self, app, window_name: str, rows: int):
        super().__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setMinimumWidth(700)
        self.app = app
        self.setWindowTitle(window_name)
        self.row_count = 0

        with open("assets/stylesheet.qss") as ss:
            self.setStyleSheet(ss.read())

        # Message Box
        self.message_box = QLabel()
        self.message_box.setObjectName("Message")

        # Ok Button
        self.button_ok = QPushButton("Ok")
        self.button_ok.clicked.connect(self.ok_clicked)
        self.button_ok.setDefault(True)
        self.button_ok.setDisabled(True)
        self.button_ok.setCursor(Qt.PointingHandCursor)

        # Cancel Button
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)
        button_cancel.setCursor(Qt.PointingHandCursor)

        # Configure Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.message_box, rows + 1, 1, 1, 2)

        # Button Box
        button_box = QHBoxLayout()
        button_box.addWidget(button_cancel)
        button_box.addWidget(self.button_ok)

        self.layout.addLayout(button_box, rows + 2, 2)
        self.setLayout(self.layout)

    def add_widget(self, text: str, widget: QWidget):
        """Add more widgets along with a label. This keeps track
        of the row count to make adding more widgets easier
        """
        if type(widget) == QComboBox:
            # Remove Drop Shadow Effect on QComboBox's menu
            # Daegun Kim / Philip Nelson
            # https://stackoverflow.com/questions/27739536/remove-qcombobox-listview-shadow-effect
            widget.findChild(QFrame).setWindowFlags(Qt.Popup | Qt.NoDropShadowWindowHint)

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
            self.button_ok.setDisabled(False)
        else:
            self.button_ok.setDisabled(True)

    def set_message(self, text: str):
        """Sets a message to display more info"""
        self.message_box.setText(text)

    def ok_clicked(self):
        """Implement this method"""
        pass
