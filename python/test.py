from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import csv

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        # self.default()

    def initUI(self):
        self.setWindowTitle('휴대용 레이저 제어 프로그램')

        # 레이저 제어부
        laserBox = QHBoxLayout()

        gb = QGroupBox('레이저 제어부')
        laserBox.addWidget(gb)

        box = QVBoxLayout()

        laserIpBox = QHBoxLayout()
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

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(laserBox)
        self.setLayout(vbox)

    def default(self):
        data_list = []

        with open('write.csv', 'r') as raw:
            reader = csv.reader(raw)
            for lines in reader:
                data_list.append(lines)

        for i in range(len(data_list)):
            print(data_list[i][0])

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())



