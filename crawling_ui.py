import sys
from PyQt5.QtWidgets import *
import crawling


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        btn1 = QPushButton('&Button1', self)
        btn1.setText('crawling 실행')
        btn1.clicked.connect(self.btn1clicked)

        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.setWindowTitle('Crawling FirstProject')  # self: MyApp 객체

        hbox = QHBoxLayout()
        hbox.addWidget(self.te)
        hbox.addWidget(btn1)
        hbox.addStretch()

        self.setLayout(hbox)    

        self.move(300,300)
        self.resize(500, 200)
        self.show()

    def btn1clicked(self):
        returndict = crawling.param_validate({'s_season':'018', 's_pr':'201|1', 'e_season':'018', 'e_pr':'201|1', 'part':'point'})
        table = crawling.param_call(returndict)
        self.te.setText(str(table))


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())