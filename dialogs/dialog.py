from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QWidget, QHBoxLayout, QComboBox, QFrame, \
    QVBoxLayout
from PyQt5.QtCore import Qt


class PlannerQDialog(QDialog):
    def __init__(self, app, window_name: str, rows: int):
        super().__init__()
        # self.setModal(False)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.app = app
        self.row_count = 1
        self.dragging = False
        self.local_position = None
        self.setMinimumWidth(self.app.width() / 4)

        # Align dialog with main window
        x = app.pos().x() + app.width() / 2 - self.width() / 2
        y = app.pos().y() + app.height() / 2 - self.height() / 2
        self.move(x, y)

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

        # X / close Button
        button_x = QPushButton("X")
        button_x.setFixedSize(80, 80)
        button_x.clicked.connect(self.reject)
        button_x.setCursor(Qt.PointingHandCursor)
        button_x.setObjectName("Close")

        # Name of Dialog / Title Bar
        label_name = QLabel(window_name)
        label_name.setObjectName("Name")
        label_name.setAlignment(Qt.AlignCenter)
        label_name.setFixedHeight(80)
        bar_name = QWidget()
        bar_name.setFixedSize(self.width(), 80)
        bar_name.setObjectName("NameBar")
        layout_name = QHBoxLayout()
        layout_name.addWidget(label_name)
        layout_name.addWidget(button_x)
        layout_name.setSpacing(0)
        layout_name.setContentsMargins(0, 0, 0, 0)
        bar_name.setLayout(layout_name)

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

        # Piece layout together
        layout = QVBoxLayout()
        layout.addWidget(bar_name)
        layout.addLayout(self.fields)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create frame to contain widgets to allow for rounded
        # corners without making all the widgets transparent
        frame = QFrame()
        frame.setLayout(layout)

        # Create the final layout to set for the dialog
        base = QVBoxLayout()
        base.setContentsMargins(0, 0, 0, 0)
        base.addWidget(frame)
        self.setLayout(base)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        # Click is at the top portion of dialog
        if (0 < a0.x() < self.width()) and (0 < a0.y() < 80):
            self.dragging = True
            self.local_position = a0.localPos()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.dragging = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.dragging:
            self.move(a0.globalPos().x() - self.local_position.x(), a0.globalPos().y() - self.local_position.y())

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
