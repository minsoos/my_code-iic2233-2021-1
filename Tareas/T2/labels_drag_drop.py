import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
import parametros as p


# Fuente
# https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/

class DragLabel(QLabel):

    def __init__(self, parent, nombre):
        super().__init__(parent)
        self.nombre = nombre

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not(event.buttons() & Qt.LeftButton):
            return
        else:
            drag = QDrag(self)

            mimedata = QMimeData()
            mimedata.setText(self.nombre)
            drag.setMimeData(mimedata)

            # createing the dragging effect
            # createing the dragging effect
            pixmap = QPixmap(self.size()) # label size

            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()

            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

class DropLabel(QLabel):

    senal_poner_personaje = pyqtSignal(str, tuple)

    def __init__(self, label, parent):
        super().__init__(label, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        # QPoint: fuente: https://doc.qt.io/qt-5/qpoint.html
        r = p.RECTANGULO_TABLERO_PREPARACION
        pos_x = pos.x() + self.x()
        pos_y = pos.y() + self.y() # Se suma lo de abajo para que no tope con ningún edificio
        if r[0] < pos_x < r[0] + r[2] and r[1] + 20 < pos_y < r[1] + r[3]:
            llamador = event.mimeData().text()
            self.senal_poner_personaje.emit(llamador, (pos_x, pos_y))
        else:
            # print(f"No puedes entrar, porque estás en {pos}")
            pass

# Fuente: https://stackoverflow.com/questions/55636860/drag-and-drop-qlabels-with-pyqt5-pixmap-and-text

class DraggableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(args[0])
        self._text = None
        self.setAcceptDrops(True)
        print("my text in init ", self.text())


    def setPixmap(self, pixmap):
        if pixmap.isNull():
            self._text = None
        else:
            self._text = self.text()
        super().setPixmap(pixmap)

    def text(self):
        if self._text:
            return self._text
        return super().text()

