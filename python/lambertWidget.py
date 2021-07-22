from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
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

        self.initUI()

    def initUI(self):
        # 레이저 제어부
        lambertBox = QHBoxLayout()

        gb = QGroupBox('')
        lambertBox.addWidget(gb)

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

        # 가시거리
        visibilityBox = QHBoxLayout()
        parameterBox.addLayout(visibilityBox)
        self.visibilityLabel = QLabel(self)
        self.visibilityLabel.setText('가시 거리 [km]')
        self.visibilityLabel.setFixedWidth(130)
        self.visibilityLabel.setStyleSheet("background-color: lightgray")
        visibilityBox.addWidget(self.visibilityLabel)

        visibilityValueBox = QVBoxLayout()
        visibilityBox.addLayout(visibilityValueBox)
        self.visibility1Edit = QTextEdit(self)
        self.visibility1Edit.setFixedWidth(70)
        self.visibility1Edit.setFixedHeight(24)
        self.visibility1Edit.setText('5')
        self.visibility2Edit = QTextEdit(self)
        self.visibility2Edit.setFixedWidth(70)
        self.visibility2Edit.setFixedHeight(24)
        self.visibility2Edit.setText('10')
        self.visibility3Edit = QTextEdit(self)
        self.visibility3Edit.setFixedWidth(70)
        self.visibility3Edit.setFixedHeight(24)
        self.visibility3Edit.setText('20')
        visibilityValueBox.addWidget(self.visibility1Edit)
        visibilityValueBox.addWidget(self.visibility2Edit)
        visibilityValueBox.addWidget(self.visibility3Edit)

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
        vbox.addLayout(lambertBox)
        self.setLayout(vbox)

        self.show()

    def calculate(self):
        self.divergence = 0
        self.beamArea = 0
        self.q = []
        self.u1 = []
        self.u2 = []
        self.u3 = []
        self.spotSize = []
        self.spotArea = []
        self.area = []
        self.transmittance1 = []
        self.transmittance2 = []
        self.transmittance3 = []
        self.pTarget1 = []
        self.pTarget2 = []
        self.pTarget3 = []
        if (self.ax):
            self.ax.clear()
        self.divergence = float(self.waveLengthEdit.toPlainText())/(np.pi * float(self.inputDiameterEdit.toPlainText()) * 1000)
        self.beamArea = pow(float(self.outputDiameterEdit.toPlainText())*0.001/2, 2)*np.pi
        self.divergenceEdit.setText(str(round(self.divergence, 8)))
        self.beamAreaEdit.setText(str(round(self.beamArea, 8)))

        self.x = np.arange(0, int(self.distanceEdit.toPlainText())+100, 100)
        self.x[0] = 1

        for i in range(len(self.x)):
            self.q.append(0.585*pow(self.x[i] * 0.001, 1/3))
            self.u1.append((3.912 / float(self.visibility1Edit.toPlainText())) * (
                pow(0.55 / float(self.waveLengthEdit.toPlainText()), self.q[i])))
            self.u2.append((3.912 / float(self.visibility2Edit.toPlainText())) * (
                pow(0.55 / float(self.waveLengthEdit.toPlainText()), self.q[i])))
            self.u3.append((3.912 / float(self.visibility3Edit.toPlainText())) * (
                pow(0.55 / float(self.waveLengthEdit.toPlainText()), self.q[i])))

            self.spotSize.append(self.x[i] * self.divergence)
            self.spotArea.append(pow(self.spotSize[i], 2))

            if self.spotArea[i] > self.beamArea:
                self.area.append(self.spotArea[i])
            else:
                self.area.append(self.beamArea)

            self.transmittance1.append(np.exp(-self.u1[i] * self.x[i] * 0.001))
            self.transmittance2.append(np.exp(-self.u2[i] * self.x[i] * 0.001))
            self.transmittance3.append(np.exp(-self.u3[i] * self.x[i] * 0.001))

            self.pTarget1.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.transmittance1[i])
            self.pTarget2.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.transmittance2[i])
            self.pTarget3.append(
                float(self.laserPowerEdit.toPlainText()) * (self.beamArea / self.area[i]) * self.transmittance3[i])

        self.ax.plot(self.x, self.pTarget1, label=self.visibility1Edit.toPlainText())
        self.ax.plot(self.x, self.pTarget2, label=self.visibility2Edit.toPlainText())
        self.ax.plot(self.x, self.pTarget3, label=self.visibility3Edit.toPlainText())

        self.ax.legend()
        self.ax.grid(True)
        self.ax.set_xlabel('Time[s]')
        self.ax.set_ylabel('Power[W]')
        self.ax.set_ylim([min(self.pTarget1)-100, float(self.laserPowerEdit.toPlainText())+100])
        self.canvas.mpl_connect('button_press_event', DataCursor(self.ax))
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())