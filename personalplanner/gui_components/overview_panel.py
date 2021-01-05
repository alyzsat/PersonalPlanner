from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QListWidget, QListWidgetItem

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
        self.listwidget_upcoming.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listwidget_upcoming.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.refresh_upcoming()

    def refresh_upcoming(self):
        self.listwidget_upcoming.clear()

        # If there is no day selected, show assignments that will be due soon
        if self.widget_calendar.selected_date() is None:
            # Show all assignments or just the current term's assignments
            assignments = self.app.planner.assignments(self.app.settings.show_current())

        # Otherwise, show assignments due on that day
        else:
            assignments = self.app.planner.get_assignments_due(self.widget_calendar.selected_date())

        for id, name, course_id, completed, due_date in assignments:
            days_until_due = self.widget_calendar.days_until_due(due_date)
            if len(name) > 15:
                name = name[:15] + "...\t"
            else:
                name = name + "\t\t"
            if days_until_due < 0:
                due = f"due {-days_until_due} day{'s' if -days_until_due != 1 else ''} ago"
            elif days_until_due > 0:
                due = f"due in {days_until_due} day{'s' if days_until_due != 1 else ''}"
            else:
                due = "due Today"

            item = QListWidgetItem(name + due)
            # item.setIcon(QIcon("personalplanner/assets/logo.png"))
            self.listwidget_upcoming.addItem(item)

    def refresh(self):
        self.widget_calendar.refresh()
        self.refresh_upcoming()
