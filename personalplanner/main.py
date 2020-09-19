import sys

from PyQt5.QtWidgets import QApplication

from personalplanner.personal_planner import PersonalPlanner

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonalPlanner(app.primaryScreen().size())
    sys.exit(app.exec_())
