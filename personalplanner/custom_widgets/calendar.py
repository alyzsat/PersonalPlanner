import calendar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QGridLayout
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
        self.current_day = None

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

    def selected_date(self) -> str or None:
        if self.current_day is not None:
            return f"{self.current_year}-{self.current_month}-{self.current_day}"

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
        for i in range(6):
            for j in range(7):
                slot = QPushButton(str())
                slot.setObjectName("CalendarSlot")
                slot.clicked.connect(lambda x, s=slot: self.day_clicked(s))
                self.calendar.addWidget(slot, i, j)

        self.refresh_slots()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.current_day = None
        self.app.overview_panel.refresh()

    def previous_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.current_day = None
        self.app.overview_panel.refresh()

    def refresh(self):
        self.refresh_label()
        self.refresh_slots()

    def refresh_label(self):
        self.label_month.setText(f"{self.months[self.current_month - 1]} {self.current_year}")

    def refresh_slots(self):
        first_day, num_days = calendar.monthrange(self.current_year, self.current_month)
        count = 0
        self.clear_slots()

        while count < num_days + first_day:
            count += 1
            # Shift calendar days up one week if month
            # starts on a Sunday
            week = int(count / 7) - int(first_day == 6)
            day = int(count % 7)

            if count > first_day:
                slot = self.calendar.itemAtPosition(week, day).widget()
                slot.setText(str(count - first_day))
                slot.setObjectName("CalendarDay")
                slot.setEnabled(True)
                slot.setCursor(Qt.PointingHandCursor)

        # Highlight today's slot
        if self.current_month == datetime.now().month and self.current_year == datetime.now().year:
            n = first_day + datetime.now().day
            week = int(n / 7) - int(first_day == 6)
            day = int(n % 7)
            today = self.calendar.itemAtPosition(week, day).widget()
            if self.current_day == datetime.now().day:
                today.setObjectName("CalendarTodaySelected")
            else:
                today.setObjectName("CalendarToday")

        # Highlight selected day if today's slot isn't highlighted
        if not (self.current_month == datetime.now().month
                and self.current_year == datetime.now().year
                and self.current_day == datetime.now().day)\
                and self.current_day is not None:
            n = first_day + self.current_day
            week = int(n / 7) - int(first_day == 6)
            day = int(n % 7)
            today = self.calendar.itemAtPosition(week, day).widget()
            today.setObjectName("CalendarSelected")

        self.app.set_theme(self.app.settings.current_theme(), self)

    def clear_slots(self):
        for i in range(7):
            for j in range(6):
                slot = self.calendar.itemAtPosition(j, i).widget()
                slot.setObjectName("CalendarSlot")
                slot.setText("")
                slot.setEnabled(False)
                slot.setCursor(Qt.PointingHandCursor)

    def day_clicked(self, slot: QPushButton):
        day = int(slot.text())
        if day == self.current_day:
            self.current_day = None
        else:
            self.current_day = day
        self.app.overview_panel.refresh()

    def days_until_due(self, due_date: str) -> int:
        """Return the number of days until the assignment is due"""
        y, m, d = due_date.split("-")
        d1 = datetime(int(y), int(m), int(d))
        d2 = datetime.now()
        if d1.date() == d2.date():
            return 0
        days_str = str(d1 - d2).split()[0]
        if ":" in days_str:
            if "-" in days_str:
                days_str = -1
            else:
                days_str = 0
        return int(days_str) + 1
