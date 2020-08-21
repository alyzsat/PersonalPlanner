import calendar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, \
    QGridLayout
from datetime import datetime


class PlannerCalendar(QWidget):
    def __init__(self, app):
        # Not using QCalendarWidget because of styling limitations
        # -> Building a custom calendar from QGridLayout of QPushButtons
        super().__init__()
        self.app = app

        # "Current" as in which month is currently being viewed, not the
        # current month or year in time
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        self.layout = QVBoxLayout()
        self.months = [
            "January", "February", "March",
            "April", "May", "June", "July",
            "August", "September", "October",
            "November", "December"
        ]
        self.calendar = QGridLayout()
        self.button_previous = QPushButton("<")
        self.button_next = QPushButton(">")
        self.label_month = QLabel()

        self.setup_layout()
        self.setup_table()
        self.setup_slots()

    def setup_layout(self):
        calendar_bar = QHBoxLayout()
        calendar_bar.addWidget(self.button_previous)
        calendar_bar.addStretch()
        calendar_bar.addWidget(self.label_month)
        calendar_bar.addStretch()
        calendar_bar.addWidget(self.button_next)

        self.layout.addLayout(calendar_bar)
        self.layout.addLayout(self.calendar)
        self.setLayout(self.layout)

    def setup_table(self):
        self.label_month.setObjectName("Month")
        self.refresh_label()

        self.button_next.setObjectName("CalendarArrow")
        self.button_next.setCursor(Qt.PointingHandCursor)
        self.button_next.clicked.connect(self.next_month)

        self.button_previous.setObjectName("CalendarArrow")
        self.button_previous.setCursor(Qt.PointingHandCursor)
        self.button_previous.clicked.connect(self.previous_month)

        self.calendar.setSpacing(1)

    def setup_slots(self):
        first_day, num_days = calendar.monthrange(self.current_year, self.current_month)
        count = 0
        for i in range(6):
            for j in range(7):
                slot = QPushButton(str())
                slot.setObjectName("CalendarSlot")
                self.calendar.addWidget(slot, i, j)

        self.refresh_slots()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.refresh_label()
        self.refresh_slots()

    def previous_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.refresh_label()
        self.refresh_slots()

    def refresh_label(self):
        self.label_month.setText(f"{self.months[self.current_month - 1]} {self.current_year}")

    def refresh_slots(self):
        first_day, num_days = calendar.monthrange(self.current_year, self.current_month)
        count = 0

        while count < 41:
            count += 1
            week = int(count / 7)
            day = int(count % 7)

            if count <= first_day or count - first_day > num_days:
                slot = self.calendar.itemAtPosition(week, day).widget()
                slot.setObjectName("CalendarSlot")
                slot.setText("")

            elif count > first_day:
                slot = self.calendar.itemAtPosition(week, day).widget()
                slot.setText(str(count - first_day))
                slot.setObjectName("CalendarDay")

        self.app.set_theme(self.app.current_theme, self)


