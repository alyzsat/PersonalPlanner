from PyQt5.QtWidgets import QTableWidget

from planner_parts.calendar import Calendar


class PlannerCalendar(QTableWidget):
    def __init__(self):
        super().__init__()
        # Not using QCalendarWidget because of styling limitations
        # -> Building a custom calendar from QTableWidget
        self.calendar = Calendar()
        pass
