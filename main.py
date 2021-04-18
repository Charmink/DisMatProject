import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QSpinBox
from PyQt5.QtWidgets import QLCDNumber, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, qBlue
import func
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 600, 400)
        self.setWindowTitle('Maximum graph matching')

        self.AddEdgeBtn = QPushButton('Add an edge', self)
        self.AddEdgeBtn.resize(self.AddEdgeBtn.sizeHint())
        self.AddEdgeBtn.move(75, 10)

        self.ExitBtn = QPushButton("Exit", self)
        self.ExitBtn.resize(self.ExitBtn.sizeHint())
        self.ExitBtn.move(10, 10)
        self.ExitBtn.clicked.connect(self.exit)

        self.NameLbl = QLabel(self)
        self.NameLbl.setText("Graph")
        self.NameLbl.move(140, 60)

        self.CntLcd = QLCDNumber(self)
        self.CntLcd.resize(100, 50)
        self.CntLcd.move(400, 100)

        self.LcdLbl = QLabel(self)
        self.LcdLbl.setText("Maximum of matching pairs")
        self.LcdLbl.resize(self.LcdLbl.sizeHint())
        self.LcdLbl.move(365, 60)

        self.N, self.K = self.get_size_of_graph()
        self.nodeCoords = self.node_coords_init()

        self.mt = func.find_edges(self.nodeCoords, self.N, self.K)

        self.AddEdgeBtn.clicked.connect(self.add_edge)

    def exit(self):
        exit()

    def update_display(self):
        cnt = 0
        self.mt = func.find_edges(self.nodeCoords, self.N, self.K)
        for i in range(self.K):
            if self.mt[i] != -1:
                cnt += 1
        self.CntLcd.display(cnt)

    def paintEvent(self, event):

        self.update_display()

        qp = QPainter()
        qp.begin(self)
        self.draw_graph(qp)
        qp.end()

    def draw_graph(self, qp):
        pen = QPen(Qt.red, 3)
        qp.setPen(pen)
        for key, value in self.nodeCoords["left"].items():
            qp.drawEllipse(value[1][0], value[1][1], 20, 20)
            for node in value[0]:
                if self.mt[node] == key:
                    pen.setColor(Qt.green)
                    qp.setPen(pen)
                else:
                    pen.setColor(Qt.red)
                    qp.setPen(pen)
                qp.drawLine(value[1][0] + 20, value[1][1] + 10, self.nodeCoords["right"][node][1][0],
                            self.nodeCoords["right"][node][1][1] + 10)
            pen.setColor(Qt.red)
            qp.setPen(pen)
        for key, value in self.nodeCoords["right"].items():
            qp.drawEllipse(value[1][0], value[1][1], 20, 20)


    def node_coords_init(self):
        nodeCoords = {"left": {}, "right": {}}
        step = 100
        for i in range(self.N):
            nodeCoords["left"][i] = ([], (50, step))
            step += 50
        step = 100
        for i in range(self.K):
            nodeCoords["right"][i] = ([], (250, step))
            step += 50
        return nodeCoords

    def get_size_of_graph(self):
        n, ok_pressed = QInputDialog.getInt(
            self, "Graph size",
            "Select the number of vertices in the right-hand side of the graph?",
            5, 0, 10, 1)
        if not ok_pressed:
            exit()

        k, ok_pressed = QInputDialog.getInt(
            self, "Graph size",
            "Select the number of vertices in the left-hand side of the graph?",
            5, 0, 10, 1)
        if not ok_pressed:
            exit()

        return n, k

    def add_edge(self):
        self.second_form = AddEdge(self)
        self.second_form.show()


class AddEdge(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(400, 200, 430, 230)
        self.setWindowTitle('Add an edge')
        self.spnBoxN = QSpinBox(self)
        self.spnBoxN.move(100, 60)
        self.spnBoxN.resize(self.spnBoxN.sizeHint())
        self.spnBoxN.setMaximum(ex.N - 1)
        self.lblN = QLabel(self)
        self.lblN.setText("Select left node!")
        self.lblN.move(70, 30)
        self.spnBoxK = QSpinBox(self)
        self.spnBoxK.move(300, 60)
        self.spnBoxK.resize(self.spnBoxN.sizeHint())
        self.spnBoxK.setMaximum(ex.K - 1)
        self.lblK = QLabel(self)
        self.lblK.setText("Select right node!")
        self.lblK.move(270, 30)

        self.AppendBtn = QPushButton("Create!", self)
        self.AppendBtn.resize(self.AppendBtn.sizeHint())
        self.AppendBtn.move(170, 130)
        self.AppendBtn.clicked.connect(self.create_edge)

    def create_edge(self):
        ex.nodeCoords["left"][int(self.spnBoxN.text())][0].append(int(self.spnBoxK.text()))
        ex.second_form.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
