import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import crawling


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Crawling FirstProject')  # self: MyApp 객체

        labeltitle = QLabel('팀 누적 기록', self)
        font = labeltitle.font()
        font.setBold(True) # 왜 안되지
        # labeltitle.setAlignment(Qt.AlignVCenter)

        rbtn1 = QRadioButton('남자부', self)
        rbtn1.setChecked(True) # 기본 설정

        rbtn2 = QRadioButton('여자부', self)

        titlelayout = QHBoxLayout()
        titlelayout.addWidget(labeltitle)
        titlelayout.addSpacing(50)
        titlelayout.addWidget(rbtn1)
        titlelayout.addWidget(rbtn2)
        titlelayout.addStretch(3)

        self.top = QFrame()
        self.top.setLayout(titlelayout)

        labelFromTo = QLabel('기간', self)
        labelTilde = QLabel('~', self)

        cb1 = QComboBox(self)
        cb1.addItem('Option1')

        cb2 = QComboBox(self)
        cb2.addItem('Option2')

        cb3 = QComboBox(self)
        cb3.addItem('Option3')

        cb4 = QComboBox(self)
        cb4.addItem('Option4')

        FromTolayout = QHBoxLayout()
        FromTolayout.addWidget(labelFromTo)
        FromTolayout.addSpacing(50)
        FromTolayout.addWidget(cb1)
        FromTolayout.addWidget(cb2)
        FromTolayout.addWidget(labelTilde)
        FromTolayout.addWidget(cb3)
        FromTolayout.addWidget(cb4)

        labelCategory = QLabel('유형', self)
        labelCategory.resize(150,10)

        cb5 = QComboBox(self)
        cb5.addItem('Option5')

        btn1 = QPushButton('&Button1', self)
        btn1.setText('crawling 실행')
        btn1.clicked.connect(self.btn1clicked)

        Categorylayout = QHBoxLayout()
        Categorylayout.addWidget(labelCategory)
        Categorylayout.addSpacing(50)
        Categorylayout.addWidget(cb5)
        Categorylayout.addStretch(4)
        Categorylayout.addWidget(btn1)

        cmblayout = QVBoxLayout()
        cmblayout.addLayout(FromTolayout)
        cmblayout.addLayout(Categorylayout)

        self.middle = QFrame()
        self.middle.setLayout(cmblayout)

        self.textbox = QTextEdit()
        self.textbox.setAcceptRichText(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.textbox)

        self.bottom = QFrame()
        self.bottom.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.top)
        vbox.addWidget(self.middle)
        vbox.addWidget(self.bottom)

        mainwidget = QWidget()
        mainwidget.setLayout(vbox)

        self.setCentralWidget(mainwidget)
        self.move(300,300)
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