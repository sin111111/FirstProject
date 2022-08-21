import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import crawling


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        labeltitle = QLabel('팀 누적 기록', self)
        # labeltitle.setAlignment(Qt.AlignVCenter)

        titlelayout = QHBoxLayout()
        titlelayout.addWidget(labeltitle)

        self.top = QFrame()
        self.top.setLayout(titlelayout)

        btn1 = QPushButton('&Button1', self)
        btn1.setText('crawling 실행')
        btn1.clicked.connect(self.btn1clicked)

        self.textbox = QTextEdit()
        self.textbox.setAcceptRichText(False)

        hbox = QHBoxLayout()
        hbox.addWidget(labeltitle)
        hbox.addWidget(self.textbox)
        hbox.addWidget(btn1)
        hbox.addStretch()

        self.middle = QFrame()
        self.middle.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.top)
        vbox.addWidget(self.middle)

        mainwidget = QWidget()
        mainwidget.setLayout(vbox)

        self.setCentralWidget(mainwidget)
        self.setWindowTitle('Crawling FirstProject')  # self: MyApp 객체
        self.move(300,300)
        self.resize(500, 200)
        self.show()


    def btn1clicked(self):
        returndict = crawling.param_validate({'s_season':'018', 's_pr':'201|1', 'e_season':'018', 'e_pr':'201|1', 'part':'point'})
        table = crawling.param_call(returndict)
        self.textbox.setText(str(table))


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyApp()
    mainWindow.show()
    sys.exit(app.exec_())