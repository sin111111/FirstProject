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

        rbtn1 = QRadioButton('남자부', self)
        rbtn1.setChecked(True) # 기본 설정

        rbtn2 = QRadioButton('여자부', self)

        titlelayout = QHBoxLayout()
        titlelayout.addWidget(labeltitle)
        titlelayout.addWidget(rbtn1)
        titlelayout.addWidget(rbtn2)

        self.top = QFrame()
        self.top.setLayout(titlelayout)

        cb1 = QComboBox(self)
        cb1.addItem('Option1')

        cb2 = QComboBox(self)
        cb2.addItem('Option2')

        cb3 = QComboBox(self)
        cb3.addItem('Option3')

        cb4 = QComboBox(self)
        cb4.addItem('Option4')

        cb5 = QComboBox(self)
        cb5.addItem('Option5')

        cmblayout = QHBoxLayout()
        cmblayout.addWidget(cb1)
        cmblayout.addWidget(cb2)
        cmblayout.addWidget(cb3)
        cmblayout.addWidget(cb4)
        cmblayout.addWidget(cb5)

        self.middle = QFrame()
        self.middle.setLayout(cmblayout)

        btn1 = QPushButton('&Button1', self)
        btn1.setText('crawling 실행')
        btn1.clicked.connect(self.btn1clicked)

        self.textbox = QTextEdit()
        self.textbox.setAcceptRichText(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.textbox)
        hbox.addWidget(btn1)
        hbox.addStretch()

        self.bottom = QFrame()
        self.bottom.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.top)
        vbox.addWidget(self.middle)
        vbox.addWidget(self.bottom)

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