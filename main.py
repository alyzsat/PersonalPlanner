import sys

from PyQt5.QtWidgets import QApplication

from personal_planner import PersonalPlanner
from stylesheet_processor import StyleSheetProcessor

if __name__ == "__main__":
    StyleSheetProcessor().run()
    app = QApplication(sys.argv)
    window = PersonalPlanner(app.primaryScreen().size())
    sys.exit(app.exec_())
