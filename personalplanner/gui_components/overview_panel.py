from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QListWidget, QLabel

from personalplanner.custom_widgets.calendar import PlannerCalendar


class OverviewPanel(QFrame):
    def __init__(self, app, size_widgets: int):
        super().__init__()
        self.app = app

        # Initialize widgets
        self.label_term = QLabel()
        self.widget_calendar = PlannerCalendar(self.app)
        self.listwidget_upcoming = QListWidget()

        # Add Widgets to layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label_term)
        layout.addWidget(self.widget_calendar)
        layout.addWidget(self.listwidget_upcoming)

        # Configure Widgets
        self.setup_term(app.settings.current_term())
        self.setup_calendar(int(size_widgets))
        self.setup_upcoming(int(size_widgets))

        self.setLayout(layout)
        self.setObjectName("OverviewPanel")

    def setup_term(self, term: (str, int)):
        s, y = term
        self.label_term.setText(f"Current Term: {s} {y}")
        self.label_term.setObjectName("LabelTerm")
        self.label_term.setAlignment(Qt.AlignCenter)

    def setup_calendar(self, width: int):
        self.widget_calendar.setFixedWidth(width)
        self.widget_calendar.setObjectName("Calendar")

    def setup_upcoming(self, width: int):
        self.listwidget_upcoming.setFixedWidth(width)
        self.listwidget_upcoming.setObjectName("Upcoming")