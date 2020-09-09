from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from custom_widgets.dialogs.popup import PlannerPopUp


class PlannerQDialog(PlannerPopUp):
    def __init__(self, app, window_name: str, rows: int):
        super().__init__(app, window_name)

        # Ok Button
        self.button_ok = QPushButton("Ok")
        self.button_ok.clicked.connect(self.ok_clicked)
        self.button_ok.setDefault(True)
        self.button_ok.setDisabled(True)
        self.button_ok.setCursor(Qt.PointingHandCursor)
        self.button_ok.setFixedWidth(55)

        # Cancel Button
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)
        button_cancel.setCursor(Qt.PointingHandCursor)
        button_cancel.setFixedWidth(55)

        # Configure Fields Layout
        self.fields = QGridLayout()
        self.fields.addWidget(self.message_box, rows + 3, 1, 1, 2, alignment=Qt.AlignRight)
        self.fields.setContentsMargins(20, 20, 20, 20)

        # Button Box
        self.button_box = QHBoxLayout()
        self.button_box.addWidget(button_cancel)
        self.button_box.addWidget(self.button_ok)
        self.fields.addLayout(self.button_box, rows + 4, 2)
        self.fields.setAlignment(Qt.AlignCenter)

        self.layout.addLayout(self.fields)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, text: str, widget: QWidget):
        """Add more widgets along with a label. This keeps track
        of the row count to make adding more widgets easier
        """
        widget.setFixedWidth(120)
        self.row_count += 1
        self.fields.addWidget(QLabel(text), self.row_count, 1)
        self.fields.addWidget(widget, self.row_count, 2)

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
