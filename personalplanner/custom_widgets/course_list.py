from PyQt5.QtCore import Qt
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QListWidget, QMenu

from personalplanner.custom_widgets.dialogs.course_dialog import CourseDialog


class CourseList(QListWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.item = None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setObjectName("Courses")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu()
        self.app.set_theme(self.app.settings.current_theme(), menu)
        edit = menu.addAction("Edit")
        delete = menu.addAction("Delete")

        action = menu.exec_(self.mapToGlobal(event.pos()))
        course_id = self.itemAt(event.pos()).data(1)
        if action == edit:
            CourseDialog(self.app, "Edit Course", course_id).exec_()
            self.app.refresh()
        elif action == delete:
            self.app.planner.delete_course(course_id)
            self.app.refresh()
