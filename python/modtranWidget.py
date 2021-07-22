from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import csv
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.figure import Figure

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class DataCursor(object):
    text_template = 'x: %0.2f\ny: %0.2f'
    x, y = 0.0, 0.0
    xoffset, yoffset = 0, 20
    text_template = 'x: %0.2f\ny: %0.2f'

    def __init__(self, ax):
        self.ax = ax
        self.annotation = ax.annotate(self.text_template,
                xy=(self.x, self.y), xytext=(self.xoffset, self.yoffset),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                )
        self.annotation.set_visible(False)

    def __call__(self, event):
        self.event = event
        self.x, self.y = event.xdata, event.ydata
        if self.x is not None:
            self.annotation.xy = self.x, self.y
            self.annotation.set_text(self.text_template % (self.x, self.y))
            self.annotation.set_visible(True)
            event.canvas.draw()

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.data_list = []

        self.initUI()
        self.readData()

    def initUI(self):
        # 레이저 제어부
        modtranBox = QHBoxLayout()

        gb = QGroupBox('')
        modtranBox.addWidget(gb)

        box = QHBoxLayout()

        parameterBox = QVBoxLayout()
        box.addLayout(parameterBox)

        # 레이저 출력
        laserPowerBox = QHBoxLayout()
        parameterBox.addLayout(laserPowerBox)
        self.laserPowerLabel = QLabel(self)
        self.laserPowerLabel.setText('출력[watt]')
        self.laserPowerLabel.setFixedWidth(130)
        self.laserPowerEdit = QTextEdit(self)
        self.laserPowerEdit.setFixedWidth(70)
        self.laserPowerEdit.setFixedHeight(24)
        self.laserPowerEdit.setText('1000')
        laserPowerBox.addWidget(self.laserPowerLabel)
        laserPowerBox.addWidget(self.laserPowerEdit)

        # 레이저 파장
        waveLengthBox = QHBoxLayout()
        parameterBox.addLayout(waveLengthBox)
        self.waveLengthLabel = QLabel(self)
        self.waveLengthLabel.setText('파장[um]')
        self.waveLengthLabel.setFixedWidth(130)
        self.waveLengthEdit = QTextEdit(self)
        self.waveLengthEdit.setFixedWidth(70)
        self.waveLengthEdit.setFixedHeight(24)
        self.waveLengthEdit.setText('1.064')
        waveLengthBox.addWidget(self.waveLengthLabel)
        waveLengthBox.addWidget(self.waveLengthEdit)

        # 입력 빔 직경
        inputDiameterBox = QHBoxLayout()
        parameterBox.addLayout(inputDiameterBox)
        self.inputDiameterLabel = QLabel(self)
        self.inputDiameterLabel.setText('입력빔 직경[mm]')
        self.inputDiameterLabel.setFixedWidth(130)
        self.inputDiameterEdit = QTextEdit(self)
        self.inputDiameterEdit.setFixedWidth(70)
        self.inputDiameterEdit.setFixedHeight(24)
        self.inputDiameterEdit.setText('50')
        inputDiameterBox.addWidget(self.inputDiameterLabel)
        inputDiameterBox.addWidget(self.inputDiameterEdit)

        # 출력 빔 직경
        outputDiameterBox = QHBoxLayout()
        parameterBox.addLayout(outputDiameterBox)
        self.outputDiameterLabel = QLabel(self)
        self.outputDiameterLabel.setText('타겟빔 직경[mm]')
        self.outputDiameterLabel.setFixedWidth(130)
        self.outputDiameterEdit = QTextEdit(self)
        self.outputDiameterEdit.setFixedWidth(70)
        self.outputDiameterEdit.setFixedHeight(24)
        self.outputDiameterEdit.setText('20')
        outputDiameterBox.addWidget(self.outputDiameterLabel)
        outputDiameterBox.addWidget(self.outputDiameterEdit)

        # 거리
        distanceBox = QHBoxLayout()
        parameterBox.addLayout(distanceBox)
        self.distanceLabel = QLabel(self)
        self.distanceLabel.setText('거리[m]')
        self.distanceLabel.setFixedWidth(130)
        self.distanceEdit = QTextEdit(self)
        self.distanceEdit.setFixedWidth(70)
        self.distanceEdit.setFixedHeight(24)
        self.distanceEdit.setText('1000')
        distanceBox.addWidget(self.distanceLabel)
        distanceBox.addWidget(self.distanceEdit)

        # QComboBox 위젯 생성
        comboBox = QHBoxLayout()
        parameterBox.addLayout(comboBox)
        self.comboLabel = QLabel(self)
        self.comboLabel.setText('Altitude[km]')
        self.comboLabel.setFixedWidth(130)
        self.combo = QComboBox(self)
        self.combo.setFixedWidth(70)
        self.combo.currentTextChanged.connect(self.comboSelect)
        comboBox.addWidget(self.comboLabel)
        comboBox.addWidget(self.combo)

        # Summer κm [km-1]
        summerKmBox = QHBoxLayout()
        parameterBox.addLayout(summerKmBox)
        self.summerKmLabel = QLabel(self)
        self.summerKmLabel.setText('Summer κm [km-1]')
        self.summerKmLabel.setFixedWidth(130)
        self.summerKmEdit = QTextEdit(self)
        self.summerKmEdit.setFixedWidth(70)
        self.summerKmEdit.setFixedHeight(24)
        summerKmBox.addWidget(self.summerKmLabel)
        summerKmBox.addWidget(self.summerKmEdit)

        # Summer σm [km-1]
        summerSigmaBox = QHBoxLayout()
        parameterBox.addLayout(summerSigmaBox)
        self.summerSigmaLabel = QLabel(self)
        self.summerSigmaLabel.setText('Summer σm [km-1]')
        self.summerSigmaLabel.setFixedWidth(130)
        self.summerSigmaEdit = QTextEdit(self)
        self.summerSigmaEdit.setFixedWidth(70)
        self.summerSigmaEdit.setFixedHeight(24)
        summerSigmaBox.addWidget(self.summerSigmaLabel)
        summerSigmaBox.addWidget(self.summerSigmaEdit)

        # Winter κm [km-1]
        winterKmBox = QHBoxLayout()
        parameterBox.addLayout(winterKmBox)
        self.winterKmLabel = QLabel(self)
        self.winterKmLabel.setText('Winter κm [km-1]')
        self.winterKmLabel.setFixedWidth(130)
        self.winterKmEdit = QTextEdit(self)
        self.winterKmEdit.setFixedWidth(70)
        self.winterKmEdit.setFixedHeight(24)
        winterKmBox.addWidget(self.winterKmLabel)
        winterKmBox.addWidget(self.winterKmEdit)

        # Winter σm [km-1]
        winterSigmaBox = QHBoxLayout()
        parameterBox.addLayout(winterSigmaBox)
        self.winterSigmaLabel = QLabel(self)
        self.winterSigmaLabel.setText('Winter σm [km-1]')
        self.winterSigmaLabel.setFixedWidth(130)
        self.winterSigmaEdit = QTextEdit(self)
        self.winterSigmaEdit.setFixedWidth(70)
        self.winterSigmaEdit.setFixedHeight(24)
        winterSigmaBox.addWidget(self.winterSigmaLabel)
        winterSigmaBox.addWidget(self.winterSigmaEdit)

        # Clear κa [km-1]
        clearKaBox = QHBoxLayout()
        parameterBox.addLayout(clearKaBox)
        self.clearKaLabel = QLabel(self)
        self.clearKaLabel.setText('Clear κa [km-1]')
        self.clearKaLabel.setFixedWidth(130)
        self.clearKaEdit = QTextEdit(self)
        self.clearKaEdit.setFixedWidth(70)
        self.clearKaEdit.setFixedHeight(24)
        clearKaBox.addWidget(self.clearKaLabel)
        clearKaBox.addWidget(self.clearKaEdit)

        # Clear σa [km-1]
        clearSigmaBox = QHBoxLayout()
        parameterBox.addLayout(clearSigmaBox)
        self.clearSigmaLabel = QLabel(self)
        self.clearSigmaLabel.setText('Clear σa [km-1]')
        self.clearSigmaLabel.setFixedWidth(130)
        self.clearSigmaEdit = QTextEdit(self)
        self.clearSigmaEdit.setFixedWidth(70)
        self.clearSigmaEdit.setFixedHeight(24)
        clearSigmaBox.addWidget(self.clearSigmaLabel)
        clearSigmaBox.addWidget(self.clearSigmaEdit)

        # Hazy κa [km-1]
        hazyKaBox = QHBoxLayout()
        parameterBox.addLayout(hazyKaBox)
        self.hazyKaLabel = QLabel(self)
        self.hazyKaLabel.setText('Hazy κa [km-1]')
        self.hazyKaLabel.setFixedWidth(130)
        self.hazyKaEdit = QTextEdit(self)
        self.hazyKaEdit.setFixedWidth(70)
        self.hazyKaEdit.setFixedHeight(24)
        hazyKaBox.addWidget(self.hazyKaLabel)
        hazyKaBox.addWidget(self.hazyKaEdit)

        # Hazy σa [km-1]
        hazySigmaBox = QHBoxLayout()
        parameterBox.addLayout(hazySigmaBox)
        self.hazySigmaLabel = QLabel(self)
        self.hazySigmaLabel.setText('Hazy σa [km-1]')
        self.hazySigmaLabel.setFixedWidth(130)
        self.hazySigmaEdit = QTextEdit(self)
        self.hazySigmaEdit.setFixedWidth(70)
        self.hazySigmaEdit.setFixedHeight(24)
        hazySigmaBox.addWidget(self.hazySigmaLabel)
        hazySigmaBox.addWidget(self.hazySigmaEdit)

        # 계산
        self.calculateBtn = QPushButton(self)
        self.calculateBtn.setText('계산')
        self.calculateBtn.clicked.connect(self.calculate)
        parameterBox.addWidget(self.calculateBtn)

        # 발산각
        divergenceBox = QHBoxLayout()
        parameterBox.addLayout(divergenceBox)
        self.divergenceLabel = QLabel(self)
        self.divergenceLabel.setText('발산각 [rad]')
        self.divergenceLabel.setFixedWidth(130)
        self.divergenceEdit = QTextEdit(self)
        self.divergenceEdit.setFixedWidth(70)
        self.divergenceEdit.setFixedHeight(24)
        divergenceBox.addWidget(self.divergenceLabel)
        divergenceBox.addWidget(self.divergenceEdit)

        # 빔 면적
        beamAreaBox = QHBoxLayout()
        parameterBox.addLayout(beamAreaBox)
        self.beamAreaLabel = QLabel(self)
        self.beamAreaLabel.setText('빔 면적[m2]')
        self.beamAreaLabel.setFixedWidth(130)
        self.beamAreaEdit = QTextEdit(self)
        self.beamAreaEdit.setFixedWidth(70)
        self.beamAreaEdit.setFixedHeight(24)
        beamAreaBox.addWidget(self.beamAreaLabel)
        beamAreaBox.addWidget(self.beamAreaEdit)

        # Summer Clear
        summerClearBox = QHBoxLayout()
        parameterBox.addLayout(summerClearBox)
        self.summerClearLabel = QLabel(self)
        self.summerClearLabel.setText('Summer Clear')
        self.summerClearLabel.setFixedWidth(130)
        self.summerClearEdit = QTextEdit(self)
        self.summerClearEdit.setFixedWidth(70)
        self.summerClearEdit.setFixedHeight(24)
        summerClearBox.addWidget(self.summerClearLabel)
        summerClearBox.addWidget(self.summerClearEdit)

        # Summer Hazy
        summerHazyBox = QHBoxLayout()
        parameterBox.addLayout(summerHazyBox)
        self.summerHazyLabel = QLabel(self)
        self.summerHazyLabel.setText('Summer Hazy')
        self.summerHazyLabel.setFixedWidth(130)
        self.summerHazyEdit = QTextEdit(self)
        self.summerHazyEdit.setFixedWidth(70)
        self.summerHazyEdit.setFixedHeight(24)
        summerHazyBox.addWidget(self.summerHazyLabel)
        summerHazyBox.addWidget(self.summerHazyEdit)

        # Winter Clear
        winterClearBox = QHBoxLayout()
        parameterBox.addLayout(winterClearBox)
        self.winterClearLabel = QLabel(self)
        self.winterClearLabel.setText('Winter Clear')
        self.winterClearLabel.setFixedWidth(130)
        self.winterClearEdit = QTextEdit(self)
        self.winterClearEdit.setFixedWidth(70)
        self.winterClearEdit.setFixedHeight(24)
        winterClearBox.addWidget(self.winterClearLabel)
        winterClearBox.addWidget(self.winterClearEdit)

        # Winter Hazy
        winterHazyBox = QHBoxLayout()
        parameterBox.addLayout(winterHazyBox)
        self.winterHazyLabel = QLabel(self)
        self.winterHazyLabel.setText('Winter Hazy')
        self.winterHazyLabel.setFixedWidth(130)
        self.winterHazyEdit = QTextEdit(self)
        self.winterHazyEdit.setFixedWidth(70)
        self.winterHazyEdit.setFixedHeight(24)
        winterHazyBox.addWidget(self.winterHazyLabel)
        winterHazyBox.addWidget(self.winterHazyEdit)

        self.Label = QLabel(self)
        parameterBox.addWidget(self.Label)

        # 그래프
        graphBox = QHBoxLayout()
        box.addLayout(graphBox)

        self.canvas = FigureCanvas(Figure(figsize=(100, 100)))

        graphBox.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(modtranBox)
        self.setLayout(vbox)

        self.show()

    def calculate(self):
        self.spotSize = []
        self.spotArea = []
        self.area = []
        self.summerClearList = []
        self.summerHazyList = []
        self.winterClearList = []
        self.winterHazyList = []
        self.summerClearPower = []
        self.summerHazyPower = []
        self.winterClearPower = []
        self.winterHazyPower = []

        if (self.ax):
            self.ax.clear()

        self.divergence = float(self.waveLengthEdit.toPlainText())/(np.pi * float(self.inputDiameterEdit.toPlainText()) * 1000)
        self.beamArea = pow(float(self.outputDiameterEdit.toPlainText())*0.001/2, 2)*np.pi
        self.divergenceEdit.setText(str(round(self.divergence, 8)))
        self.beamAreaEdit.setText(str(round(self.beamArea, 8)))

        self.summerClear = float(self.summerSigmaEdit.toPlainText()) + float(self.clearSigmaEdit.toPlainText()) + float(
            self.summerKmEdit.toPlainText()) + float(self.clearKaEdit.toPlainText())
        self.summerHazy = float(self.summerSigmaEdit.toPlainText()) + float(self.hazySigmaEdit.toPlainText()) + float(
            self.summerKmEdit.toPlainText()) + float(self.hazyKaEdit.toPlainText())
        self.winterClear = float(self.winterSigmaEdit.toPlainText()) + float(self.clearSigmaEdit.toPlainText()) + float(
            self.winterKmEdit.toPlainText()) + float(self.clearKaEdit.toPlainText())
        self.winterHazy = float(self.winterSigmaEdit.toPlainText()) + float(self.hazySigmaEdit.toPlainText()) + float(
            self.winterKmEdit.toPlainText()) + float(self.hazyKaEdit.toPlainText())
        self.summerClearEdit.setText(str(round(self.summerClear, 8)))
        self.summerHazyEdit.setText(str(round(self.summerHazy, 8)))
        self.winterClearEdit.setText(str(round(self.winterClear, 8)))
        self.winterHazyEdit.setText(str(round(self.winterHazy, 8)))

        self.x = np.arange(0, int(self.distanceEdit.toPlainText())+100, 100)

        self.x[0] = 1

        for i in range(len(self.x)):
            self.spotSize.append(self.x[i] * self.divergence)
            self.spotArea.append(pow(self.spotSize[i], 2))

            if self.spotArea[i] > self.beamArea:
                self.area.append(self.spotArea[i])
            else:
                self.area.append(self.beamArea)

            self.summerClearList.append(np.exp(-self.summerClear * self.x[i] * 0.001))
            self.summerHazyList.append(np.exp(-self.summerHazy * self.x[i] * 0.001))
            self.winterClearList.append(np.exp(-self.winterClear * self.x[i] * 0.001))
            self.winterHazyList.append(np.exp(-self.winterHazy * self.x[i] * 0.001))

            self.summerClearPower.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.summerClearList[i])
            self.summerHazyPower.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.summerHazyList[i])
            self.winterClearPower.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.winterClearList[i])
            self.winterHazyPower.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.winterHazyList[i])

        self.ax.plot(self.x, self.summerClearPower, label='Summer Clear')
        self.ax.plot(self.x, self.summerHazyPower, label='Summer Hazy')
        self.ax.plot(self.x, self.winterClearPower, label='Winter Clear')
        self.ax.plot(self.x, self.winterHazyPower, label='Winter Hazy')

        self.ax.legend()
        self.ax.grid(True)
        self.ax.set_xlabel('Time[s]')
        self.ax.set_ylabel('Power[W]')
        self.ax.set_ylim([min(self.winterHazyPower)-100, float(self.laserPowerEdit.toPlainText())+100])
        self.canvas.mpl_connect('button_press_event', DataCursor(self.ax))
        self.canvas.draw()

    def comboSelect(self):
        self.summerKmEdit.setText(self.data_list[self.combo.currentIndex()][1])
        self.summerSigmaEdit.setText(self.data_list[self.combo.currentIndex()][2])
        self.winterKmEdit.setText(self.data_list[self.combo.currentIndex()][3])
        self.winterSigmaEdit.setText(self.data_list[self.combo.currentIndex()][4])
        self.clearKaEdit.setText(self.data_list[self.combo.currentIndex()][5])
        self.clearSigmaEdit.setText(self.data_list[self.combo.currentIndex()][6])
        self.hazyKaEdit.setText(self.data_list[self.combo.currentIndex()][7])
        self.hazySigmaEdit.setText(self.data_list[self.combo.currentIndex()][8])

    def readData(self):
        with open('condition.csv', 'r') as raw:
            reader = csv.reader(raw)
            for lines in reader:
                self.data_list.append(lines)

        for i in range(len(self.data_list)):
            self.combo.addItem(self.data_list[i][0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())