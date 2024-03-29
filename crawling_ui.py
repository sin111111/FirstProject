import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import crawling


class MyApp(QMainWindow):

    global s_part # 남자부,여자부
    global s_season
    global s_pr
    global e_season
    global e_pr
    global part

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Crawling FirstProject')  # self: MyApp 객체

        labeltitle = QLabel('팀 누적 기록', self)
        font = labeltitle.font()
        font.setBold(True) # 왜 안되지
        # labeltitle.setAlignment(Qt.AlignVCenter)

        rbtnMale = QRadioButton('남자부')
        rbtnMale.setChecked(True) # 기본 설정
        rbtnMale.checkedvalue = '1'
        rbtnMale.toggled.connect(self.rbtnclicked)

        self.s_part = '1'

        rbtnFemale = QRadioButton('여자부')
        rbtnFemale.checkedvalue = '2'
        rbtnFemale.toggled.connect(self.rbtnclicked)

        titlelayout = QHBoxLayout()
        titlelayout.addWidget(labeltitle)
        titlelayout.addSpacing(50)
        titlelayout.addWidget(rbtnMale)
        titlelayout.addWidget(rbtnFemale)
        titlelayout.addStretch(3)

        self.top = QFrame()
        self.top.setLayout(titlelayout)

        labelFromTo = QLabel('기간', self)
        labelTilde = QLabel('~', self)

        cb1 = QComboBox(self)
        cb1.value = 's_season'

        for key,value in crawling.s_season_dict.items():
            cb1.addItem(value, key)
        
        self.s_season = cb1.currentData()
        cb1.currentIndexChanged.connect(self.cmbselectionchanged)

        self.cb2 = QComboBox(self)
        self.cb2.value = 's_pr'
        self.cb2.currentIndexChanged.connect(self.cmbselectionchanged)

        cb3 = QComboBox(self)
        cb3.value = 'e_season'
        for key,value in crawling.e_season_dict.items():
            cb3.addItem(value, key)
        
        self.e_season = cb3.currentData()
        
        cb3.currentIndexChanged.connect(self.cmbselectionchanged)

        self.cb4 = QComboBox(self)
        self.cb4.value = 'e_pr'
        self.cb4.currentIndexChanged.connect(self.cmbselectionchanged)

        
        FromTolayout = QHBoxLayout()
        FromTolayout.addWidget(labelFromTo)
        FromTolayout.addSpacing(50)
        FromTolayout.addWidget(cb1)
        FromTolayout.addWidget(self.cb2)
        FromTolayout.addWidget(labelTilde)
        FromTolayout.addWidget(cb3)
        FromTolayout.addWidget(self.cb4)

        labelCategory = QLabel('유형', self)
        labelCategory.resize(150,10)

        cb5 = QComboBox(self)
        cb5.value = 'e_season'
        for key,value in crawling.part_dict.items():
            cb5.addItem(value, key)
        
        self.part = cb5.currentData()        
        cb5.currentIndexChanged.connect(self.cmbselectionchanged)        

        btnInquiry = QPushButton('&Button1', self)
        btnInquiry.setText('crawling 실행')
        btnInquiry.clicked.connect(self.btnInquiryclicked)

        Categorylayout = QHBoxLayout()
        Categorylayout.addWidget(labelCategory)
        Categorylayout.addSpacing(50)
        Categorylayout.addWidget(cb5)
        Categorylayout.addStretch(4)
        Categorylayout.addWidget(btnInquiry)

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

    def rbtnclicked(self):
        radiobutton = self.sender()
        if(radiobutton.isChecked()):
            self.s_part = radiobutton.checkedvalue
            print(radiobutton.text() + "is selected")
            print('s_part is ' + self.s_part)        


    def cmbselectionchanged(self):
        combobox = self.sender()
        comboData = combobox.currentData()

        if(combobox.value == 's_season'):
            self.s_season = comboData
            spr_dict = crawling.round_param_get({'spart':'s', 's_season':self.s_season, 'e_season':self.e_season })
            for key,value in spr_dict.items():
                self.cb2.addItem(value, key)


        elif(combobox.value == 's_pr'):
            self.s_pr = comboData


        elif(combobox.value == 'e_season'):
            self.e_season = comboData
            epr_dict = crawling.round_param_get({'spart':'e', 's_season':self.s_season, 'e_season':self.e_season })
            for key,value in epr_dict.items():
                self.cb4.addItem(value, key)
                

        elif(combobox.value == 'e_pr'):
            self.e_pr = comboData
        
        
        else:
            self.part = comboData


    def btnInquiryclicked(self):
        returndict = crawling.param_validate({'s_part': self.s_part, 's_season': self.s_season, 's_pr': self.s_pr, 'e_season': self.e_season, 'e_pr': self.e_pr, 'part': self.part})
        table = crawling.param_call(returndict)
        self.textbox.setText(str(table))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyApp()
    mainWindow.show()
    sys.exit(app.exec_())