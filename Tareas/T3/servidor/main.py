from servidor import Servidor
import sys
from PyQt5.QtWidgets import QApplication


def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    HOST = "localhost"
    PORT = 47365
    Servidor(HOST, PORT)
    app.exec()
