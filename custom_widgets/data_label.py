from PyQt5.QtWidgets import QLabel


class DataLabel(QLabel):
    def __init__(self, text: str, data=None):
        super().__init__(text)
        if data is not None:
            self._data = data

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data
