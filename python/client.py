from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import laser_client
import struct
import numpy as np
import threading
from time import sleep
import csv
from struct import *
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

port = 5000
ip = '192.168.0.99' #'127.0.1.1'

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.x_start = 50
        self.x_end = 50
        self.initUI()

    def __del__(self):
        print('End')

    def initUI(self):
        self.setWindowTitle('레이저 효과도 분석')

        # 레이저 제어부
        laserBox = QHBoxLayout()

        gb = QGroupBox('레이저 제어부')
        laserBox.addWidget(gb)

        box = QHBoxLayout()

        laserIpBox = QVBoxLayout()
        box.addLayout(laserIpBox)

        # QComboBox 위젯 생성
        self.combo = QComboBox(self)
        self.combo.currentTextChanged.connect(self.combobox_select)
        laserIpBox.addWidget(self.combo)

        # QLabel 에서 선택한 값 표시
        self.combo_label = QLabel(self)
        laserIpBox.addWidget(self.combo_label)

        # 콤보박스에 추가할 데이터 입력
        self.input_text = QLineEdit(self)
        laserIpBox.addWidget(self.input_text)

        # 콤보박스에 데이터 추가
        self.add_button = QPushButton('Add', self)
        self.add_button.clicked.connect(self.add_data_combobox)
        laserIpBox.addWidget(self.add_button)

        # 삭제 버튼
        self.Remove_button = QPushButton('Remove', self)
        self.Remove_button.clicked.connect(self.remove_data_combobox)
        laserIpBox.addWidget(self.Remove_button)

        graphBox = QVBoxLayout()
        box.addLayout(graphBox)

        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        graphBox.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(laserBox)
        self.setLayout(vbox)

        self.show()

    def combobox_select(self):
        # QLabel 에 표시
        self.combo_label.setText(self.combo.currentText())
        print(self.combo.currentText())
        print(self.combo.currentIndex())

    def add_data_combobox(self):
        self.combo.addItem(self.input_text.text())
        print(self.input_text.text())
        self.input_text.clear()

    def remove_data_combobox(self):
        self.combo.removeItem(self.combo.currentIndex())

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.x_start += 1
            self.x = np.arange(self.x_start, self.x_end, 1)
            self.y = np.sin(self.x)
            self.ax.plot(self.x, self.y, '-')
            self.canvas.draw()
        elif event.angleDelta().y() < 0:
            self.x_start -= 1
            self.x = np.arange(self.x_start, self.x_end, 1)
            self.y = np.sin(self.x)
            self.ax.plot(self.x, self.y, '-')
            self.canvas.draw()

    def closeEvent(self, e):
        print('close')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())