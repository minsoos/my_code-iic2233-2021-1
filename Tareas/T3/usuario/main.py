import sys
from PyQt5.QtWidgets import QApplication
from cliente import Cliente


def hook(type_error, traceback):
    print(type_error)
    print(traceback)


if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    HOST = "localhost"
    PORT = 47365
    Cliente(HOST, PORT)

    app.exec()

