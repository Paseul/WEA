from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.figure import Figure

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

        self.x_start = 50
        self.x_end = 50
        self.data_list = []
        self.targetArea = 0
        self.targetMass = 0
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.q4 = 0
        self.qTotal = 0
        self.lines = []

        self.initUI()
        self.readData()

    def initUI(self):
        # 레이저 제어부
        laserBox = QHBoxLayout()

        gb = QGroupBox('')
        laserBox.addWidget(gb)

        box = QHBoxLayout()

        parameterBox = QVBoxLayout()
        box.addLayout(parameterBox)

        # 레이저 빔 직경
        laserDiameterBox = QHBoxLayout()
        parameterBox.addLayout(laserDiameterBox)
        self.laserDiameterLabel = QLabel(self)
        self.laserDiameterLabel.setText('레이저 빔 직경[cm]')
        self.laserDiameterLabel.setFixedWidth(130)
        self.laserDiameterEdit = QTextEdit(self)
        self.laserDiameterEdit.setFixedWidth(70)
        self.laserDiameterEdit.setFixedHeight(24)
        self.laserDiameterEdit.setText('2')
        laserDiameterBox.addWidget(self.laserDiameterLabel)
        laserDiameterBox.addWidget(self.laserDiameterEdit)

        # 레이저 조사 시간
        laserTimeBox = QHBoxLayout()
        parameterBox.addLayout(laserTimeBox)
        self.laserTimeLabel = QLabel(self)
        self.laserTimeLabel.setText('레이저 조사 시간[s]')
        self.laserTimeLabel.setFixedWidth(130)
        self.laserTimeEdit = QTextEdit(self)
        self.laserTimeEdit.setFixedWidth(70)
        self.laserTimeEdit.setFixedHeight(24)
        self.laserTimeEdit.setText('30')
        laserTimeBox.addWidget(self.laserTimeLabel)
        laserTimeBox.addWidget(self.laserTimeEdit)

        # QComboBox 위젯 생성
        self.combo = QComboBox(self)
        self.combo.currentTextChanged.connect(self.comboSelect)
        parameterBox.addWidget(self.combo)

        # 표적 두께 [mm]
        targetThickBox = QHBoxLayout()
        parameterBox.addLayout(targetThickBox)
        self.targetThickLabel = QLabel(self)
        self.targetThickLabel.setText('표적 두께 [mm]')
        self.targetThickLabel.setFixedWidth(130)
        self.targetThickEdit = QTextEdit(self)
        self.targetThickEdit.setFixedWidth(70)
        self.targetThickEdit.setFixedHeight(24)
        self.targetThickEdit.setText('1')
        targetThickBox.addWidget(self.targetThickLabel)
        targetThickBox.addWidget(self.targetThickEdit)

        # 표적 밀도
        targetDensityBox = QHBoxLayout()
        parameterBox.addLayout(targetDensityBox)
        self.targetDensityLabel = QLabel(self)
        self.targetDensityLabel.setText('표적 밀도 ρ [gm/cm3]')
        self.targetDensityLabel.setFixedWidth(130)
        self.targetDensityEdit = QTextEdit(self)
        self.targetDensityEdit.setFixedWidth(70)
        self.targetDensityEdit.setFixedHeight(24)
        targetDensityBox.addWidget(self.targetDensityLabel)
        targetDensityBox.addWidget(self.targetDensityEdit)

        # 비열
        specificHeatBox = QHBoxLayout()
        parameterBox.addLayout(specificHeatBox)
        self.specificHeatLabel = QLabel(self)
        self.specificHeatLabel.setText('비열 C [J/gm.℃]')
        self.specificHeatLabel.setFixedWidth(130)
        self.specificHeatEdit = QTextEdit(self)
        self.specificHeatEdit.setFixedWidth(70)
        self.specificHeatEdit.setFixedHeight(24)
        specificHeatBox.addWidget(self.specificHeatLabel)
        specificHeatBox.addWidget(self.specificHeatEdit)

        # 용융점
        meltingPointBox = QHBoxLayout()
        parameterBox.addLayout(meltingPointBox)
        self.meltingPointLabel = QLabel(self)
        self.meltingPointLabel.setText('용융점 [℃]')
        self.meltingPointLabel.setFixedWidth(130)
        self.meltingPointEdit = QTextEdit(self)
        self.meltingPointEdit.setFixedWidth(70)
        self.meltingPointEdit.setFixedHeight(24)
        meltingPointBox.addWidget(self.meltingPointLabel)
        meltingPointBox.addWidget(self.meltingPointEdit)

        # 기화점
        vaporPointBox = QHBoxLayout()
        parameterBox.addLayout(vaporPointBox)
        self.vaporPointLabel = QLabel(self)
        self.vaporPointLabel.setText('기화점 [℃]')
        self.vaporPointLabel.setFixedWidth(130)
        self.vaporPointEdit = QTextEdit(self)
        self.vaporPointEdit.setFixedWidth(70)
        self.vaporPointEdit.setFixedHeight(24)
        vaporPointBox.addWidget(self.vaporPointLabel)
        vaporPointBox.addWidget(self.vaporPointEdit)

        # 용융잠열
        meltingLatentBox = QHBoxLayout()
        parameterBox.addLayout(meltingLatentBox)
        self.meltingLatentLabel = QLabel(self)
        self.meltingLatentLabel.setText('용융잠열 Lm [J/gm]')
        self.meltingLatentLabel.setFixedWidth(130)
        self.meltingLatentEdit = QTextEdit(self)
        self.meltingLatentEdit.setFixedWidth(70)
        self.meltingLatentEdit.setFixedHeight(24)
        meltingLatentBox.addWidget(self.meltingLatentLabel)
        meltingLatentBox.addWidget(self.meltingLatentEdit)

        # 기화잠열
        vaporLatentBox = QHBoxLayout()
        parameterBox.addLayout(vaporLatentBox)
        self.vaporLatentLabel = QLabel(self)
        self.vaporLatentLabel.setText('기화잠열 Lv [J/gm]')
        self.vaporLatentLabel.setFixedWidth(130)
        self.vaporLatentEdit = QTextEdit(self)
        self.vaporLatentEdit.setFixedWidth(70)
        self.vaporLatentEdit.setFixedHeight(24)
        vaporLatentBox.addWidget(self.vaporLatentLabel)
        vaporLatentBox.addWidget(self.vaporLatentEdit)

        # 대기 온도
        airTempBox = QHBoxLayout()
        parameterBox.addLayout(airTempBox)
        self.airTempLabel = QLabel(self)
        self.airTempLabel.setText('대기온도[℃]')
        self.airTempLabel.setFixedWidth(130)
        self.airTempEdit = QTextEdit(self)
        self.airTempEdit.setFixedWidth(70)
        self.airTempEdit.setFixedHeight(24)
        self.airTempEdit.setText('20')
        airTempBox.addWidget(self.airTempLabel)
        airTempBox.addWidget(self.airTempEdit)

        # 대기에 의한 손실
        turbulenceBox = QHBoxLayout()
        parameterBox.addLayout(turbulenceBox)
        self.trubulenceLabel = QLabel(self)
        self.trubulenceLabel.setText('대기에 의한 손실 [%]')
        self.trubulenceLabel.setFixedWidth(130)
        self.trubulenceLabel.setStyleSheet("background-color: lightgray")
        turbulenceBox.addWidget(self.trubulenceLabel)

        trubulenceValueBox = QVBoxLayout()
        turbulenceBox.addLayout(trubulenceValueBox)
        self.turbulence1Edit = QTextEdit(self)
        self.turbulence1Edit.setFixedWidth(70)
        self.turbulence1Edit.setFixedHeight(24)
        self.turbulence1Edit.setText('10')
        self.turbulence2Edit = QTextEdit(self)
        self.turbulence2Edit.setFixedWidth(70)
        self.turbulence2Edit.setFixedHeight(24)
        self.turbulence2Edit.setText('20')
        self.turbulence3Edit = QTextEdit(self)
        self.turbulence3Edit.setFixedWidth(70)
        self.turbulence3Edit.setFixedHeight(24)
        self.turbulence3Edit.setText('30')
        self.turbulence4Edit = QTextEdit(self)
        self.turbulence4Edit.setFixedWidth(70)
        self.turbulence4Edit.setFixedHeight(24)
        self.turbulence4Edit.setText('40')
        self.turbulence5Edit = QTextEdit(self)
        self.turbulence5Edit.setFixedWidth(70)
        self.turbulence5Edit.setFixedHeight(24)
        self.turbulence5Edit.setText('50')
        trubulenceValueBox.addWidget(self.turbulence1Edit)
        trubulenceValueBox.addWidget(self.turbulence2Edit)
        trubulenceValueBox.addWidget(self.turbulence3Edit)
        trubulenceValueBox.addWidget(self.turbulence4Edit)
        trubulenceValueBox.addWidget(self.turbulence5Edit)

        self.calculateBtn = QPushButton(self)
        self.calculateBtn.setText('계산')
        self.calculateBtn.clicked.connect(self.calculate)
        parameterBox.addWidget(self.calculateBtn)

        # Q1
        calculatedQ1Box = QHBoxLayout()
        parameterBox.addLayout(calculatedQ1Box)
        self.calculatedQ1Label = QLabel(self)
        self.calculatedQ1Label.setText('Q1 [J/cm²]')
        self.calculatedQ1Label.setFixedWidth(130)
        self.calculatedQ1Edit = QTextEdit(self)
        self.calculatedQ1Edit.setFixedWidth(70)
        self.calculatedQ1Edit.setFixedHeight(24)
        calculatedQ1Box.addWidget(self.calculatedQ1Label)
        calculatedQ1Box.addWidget(self.calculatedQ1Edit)

        # Q2
        calculatedQ2Box = QHBoxLayout()
        parameterBox.addLayout(calculatedQ2Box)
        self.calculatedQ2Label = QLabel(self)
        self.calculatedQ2Label.setText('Q2 [J/cm²]')
        self.calculatedQ2Label.setFixedWidth(130)
        self.calculatedQ2Edit = QTextEdit(self)
        self.calculatedQ2Edit.setFixedWidth(70)
        self.calculatedQ2Edit.setFixedHeight(24)
        calculatedQ2Box.addWidget(self.calculatedQ2Label)
        calculatedQ2Box.addWidget(self.calculatedQ2Edit)

        # Q3
        calculatedQ3Box = QHBoxLayout()
        parameterBox.addLayout(calculatedQ3Box)
        self.calculatedQ3Label = QLabel(self)
        self.calculatedQ3Label.setText('Q3 [J/cm²]')
        self.calculatedQ3Label.setFixedWidth(130)
        self.calculatedQ3Edit = QTextEdit(self)
        self.calculatedQ3Edit.setFixedWidth(70)
        self.calculatedQ3Edit.setFixedHeight(24)
        calculatedQ3Box.addWidget(self.calculatedQ3Label)
        calculatedQ3Box.addWidget(self.calculatedQ3Edit)

        # Q4
        calculatedQ4Box = QHBoxLayout()
        parameterBox.addLayout(calculatedQ4Box)
        self.calculatedQ4Label = QLabel(self)
        self.calculatedQ4Label.setText('Q4 [J/cm²]')
        self.calculatedQ4Label.setFixedWidth(130)
        self.calculatedQ4Edit = QTextEdit(self)
        self.calculatedQ4Edit.setFixedWidth(70)
        self.calculatedQ4Edit.setFixedHeight(24)
        calculatedQ4Box.addWidget(self.calculatedQ4Label)
        calculatedQ4Box.addWidget(self.calculatedQ4Edit)

        # Qtotal
        calculatedQtotalBox = QHBoxLayout()
        parameterBox.addLayout(calculatedQtotalBox)
        self.calculatedQtotalLabel = QLabel(self)
        self.calculatedQtotalLabel.setText('Qtotal [J/cm²]')
        self.calculatedQtotalLabel.setFixedWidth(130)
        self.calculatedQtotalEdit = QTextEdit(self)
        self.calculatedQtotalEdit.setFixedWidth(70)
        self.calculatedQtotalEdit.setFixedHeight(24)
        calculatedQtotalBox.addWidget(self.calculatedQtotalLabel)
        calculatedQtotalBox.addWidget(self.calculatedQtotalEdit)

        graphBox = QHBoxLayout()
        box.addLayout(graphBox)

        self.slider = QSlider(self)
        self.slider.setRange(0, 1000)
        self.slider.setSingleStep(50)
        self.slider.setValue(1000)
        self.slider.valueChanged[int].connect(self.changeValue)
        graphBox.addWidget(self.slider)

        self.canvas = FigureCanvas(Figure(figsize=(100, 100)))

        graphBox.addWidget(self.canvas)

        self.ax = self.canvas.figure.subplots()

        gb.setLayout(box)

        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(laserBox)
        self.setLayout(vbox)

        self.show()

    def calculate(self):
        self.powerT = []
        self.pNeed1 = []
        self.pNeed2 = []
        self.pNeed3 = []
        self.pNeed4 = []
        self.pNeed5 = []
        if(self.ax):
            self.ax.clear()

        self.targetArea = pow(float(self.laserDiameterEdit.toPlainText())/2, 2)*np.pi
        self.targetMass = float(self.targetDensityEdit.toPlainText()) * self.targetArea * float(self.targetThickEdit.toPlainText()) * 0.1

        self.q1 = self.targetMass * float(self.specificHeatEdit.toPlainText()) * (float(self.meltingPointEdit.toPlainText()) - float(self.airTempEdit.toPlainText()))
        self.calculatedQ1Edit.setText(str(round(self.q1,4)))
        self.q2 = self.targetMass * float(self.meltingLatentEdit.toPlainText())
        self.calculatedQ2Edit.setText(str(round(self.q2, 4)))
        self.q3 = self.targetMass * float(self.specificHeatEdit.toPlainText()) * (float(self.vaporPointEdit.toPlainText()) - float(self.airTempEdit.toPlainText())) - self.q1
        self.calculatedQ3Edit.setText(str(round(self.q3, 4)))
        self.q4 = self.targetMass * float(self.vaporLatentEdit.toPlainText())
        self.calculatedQ4Edit.setText(str(round(self.q4, 4)))
        self.qTotal = self.q1 + self.q2 + self.q3 + self.q4
        self.calculatedQtotalEdit.setText(str(round(self.qTotal, 4)))

        for i in range(int(self.laserTimeEdit.toPlainText())):
            self.powerT.append(self.qTotal / (i+1))
            self.pNeed1.append(self.powerT[i]/(1-float(self.turbulence1Edit.toPlainText())*0.01))
            self.pNeed2.append(self.powerT[i] / (1 - float(self.turbulence2Edit.toPlainText()) * 0.01))
            self.pNeed3.append(self.powerT[i] / (1 - float(self.turbulence3Edit.toPlainText()) * 0.01))
            self.pNeed4.append(self.powerT[i] / (1 - float(self.turbulence4Edit.toPlainText()) * 0.01))
            self.pNeed5.append(self.powerT[i] / (1 - float(self.turbulence5Edit.toPlainText()) * 0.01))

        self.x = np.arange(0, int(self.laserTimeEdit.toPlainText()), 1)
        self.ax.plot(self.x, self.pNeed1, label=self.turbulence1Edit.toPlainText())
        self.ax.plot(self.x, self.pNeed2, label=self.turbulence2Edit.toPlainText())
        self.ax.plot(self.x, self.pNeed3, label=self.turbulence3Edit.toPlainText())
        self.ax.plot(self.x, self.pNeed4, label=self.turbulence4Edit.toPlainText())
        self.ax.plot(self.x, self.pNeed5, label=self.turbulence5Edit.toPlainText())

        self.slider.setRange(0, int(max(self.pNeed5)))
        self.ax.legend()
        self.ax.grid(True)
        self.ax.set_ylim([0, 1000])
        self.ax.set_xlabel('Time[s]')
        self.ax.set_ylabel('Power[W]')
        self.canvas.mpl_connect('button_press_event', DataCursor(self.ax))
        self.canvas.draw()

    def comboSelect(self):
        self.targetDensityEdit.setText(self.data_list[self.combo.currentIndex()][1])
        self.specificHeatEdit.setText(self.data_list[self.combo.currentIndex()][2])
        self.meltingPointEdit.setText(self.data_list[self.combo.currentIndex()][3])
        self.vaporPointEdit.setText(self.data_list[self.combo.currentIndex()][4])
        self.meltingLatentEdit.setText(self.data_list[self.combo.currentIndex()][5])
        self.vaporLatentEdit.setText(self.data_list[self.combo.currentIndex()][6])

    def readData(self):
        with open('material.csv', 'r') as raw:
            reader = csv.reader(raw)
            for lines in reader:
                self.data_list.append(lines)

        for i in range(len(self.data_list)):
            self.combo.addItem(self.data_list[i][0])

    def changeValue(self, value):
        self.ax.set_ylim([0, value])
        self.canvas.draw()