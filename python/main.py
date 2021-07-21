import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
import efficientWidget

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tab1 = efficientWidget.CWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, '레이저 효과도')
        tabs.addTab(tab2, 'Lamberts Low')
        tabs.addTab(tab3, 'Modtran')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('레이저 효과도 분석 프로그램')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())