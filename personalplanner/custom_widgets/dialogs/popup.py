from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame


class PlannerPopUp(QDialog):

    def __init__(self, app, window_name: str, message: str = None):
        super().__init__(parent=app)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.app = app
        self.row_count = 1
        self.dragging = False
        self.local_position = None
        self.setMinimumWidth(self.app.width() / 4)

        with open("personalplanner/assets/stylesheet.qss") as ss:
            self.setStyleSheet(ss.read())

        # Message Box
        self.message_box = QLabel()
        self.message_box.setObjectName("Message")

        # X / close Button
        button_x = QPushButton("X")
        button_x.setFixedSize(80, 40)
        button_x.clicked.connect(self.reject)
        button_x.setCursor(Qt.PointingHandCursor)
        button_x.setObjectName("Close")

        # Name of Dialog / Title Bar
        label_name = QLabel(window_name)
        label_name.setObjectName("Name")
        label_name.setAlignment(Qt.AlignCenter)
        label_name.setFixedHeight(40)
        self.bar_name = QWidget()
        self.bar_name.setFixedSize(self.width(), 40)
        self.bar_name.setObjectName("NameBar")

        layout_name = QHBoxLayout()
        layout_name.addStretch()
        layout_name.addWidget(label_name)
        layout_name.addStretch()
        layout_name.addWidget(button_x)
        layout_name.setSpacing(0)
        layout_name.setContentsMargins(0, 0, 0, 0)
        self.bar_name.setLayout(layout_name)

        # Piece layout together
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bar_name)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create frame to contain widgets to allow for rounded
        # corners without making all the widgets transparent
        frame = QFrame()
        frame.setLayout(self.layout)

        # Create the final layout to set for the dialog
        base = QVBoxLayout()
        base.setContentsMargins(0, 0, 0, 0)
        base.addWidget(frame)
        self.setLayout(base)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # If there is no message, then it's a simple popup and not a dialog
        if message is not None:
            msg = QLabel(message)
            msg.setAlignment(Qt.AlignCenter)
            msg.setContentsMargins(10, 20, 10, 50)
            self.layout.addWidget(msg)

        # Align dialog with main window
        x = app.pos().x() + app.width() / 3
        y = app.pos().y() + app.height() / 4
        self.move(x, y)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        # Click is at the top portion of dialog
        if (0 < a0.x() < self.width()) and (0 < a0.y() < 40):
            # Position of mouse at click relative to dialog
            self.local_position = a0.localPos()
            self.dragging = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.dragging = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.dragging:
            self.move(a0.globalPos().x() - self.local_position.x(), a0.globalPos().y() - self.local_position.y())
