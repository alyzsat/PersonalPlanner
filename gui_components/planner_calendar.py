from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from planner_parts.calendar import Calendar


class PlannerCalendar(QTableWidget):
    def __init__(self):
        super().__init__()
        # Not using QCalendarWidget because of styling limitations
        # -> Building a custom calendar from QTableWidget
        self.calendar = Calendar()

        self.setup_layout()
        self.setup_slots()

    def setup_layout(self):
        self.setColumnCount(7)
        self.setRowCount(5)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        for i in range(7):
            self.setColumnWidth(i, 20)

    def setup_slots(self):
        count = 0
        for week in range(5):
            for day in range(7):
                count += 1
                item = QTableWidgetItem(str(count))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(week, day, item)
