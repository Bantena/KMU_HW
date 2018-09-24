import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt

class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB(isFirst=True)

    def initUI(self):

        # Interface Labels
        self.label = {
            'name' : QLabel("Name : "),
            'age' : QLabel("Age : "),
            'score' : QLabel("Score : "),
            'amount' : QLabel("Amount : "),
            'sort' : QLabel("Key : "),
            'result' : QLabel("Result : ")
        }


        # Interface TextBoxes
        self.lineEdit = {
            'name' : QLineEdit(),
            'age' : QLineEdit(),
            'score' : QLineEdit(),
            'amount' : QLineEdit()
        }


        # Interface ComboBoxes
        self.comboBox = {
            'sort' : QComboBox()
        }

        self.comboBox['sort'].addItems(['Name', 'Age', 'Score'])

        # Interface Buttons
        self.pushButton = {
            'add' : QPushButton("Add"),
            'del' : QPushButton('Delete'),
            'find' : QPushButton('Find'),
            'inc' : QPushButton('Increase'),
            'show' : QPushButton('Show')
        }


        # Interface TextEdit
        self.textEdit = {
            'result' : QTextEdit()
        }

        self.textEdit['result'].setReadOnly(True)

        # Interface Layout
        self.boxLayout = {
            'horizon1' : QHBoxLayout(),
            'horizon2' : QHBoxLayout(),
            'horizon3' : QHBoxLayout(),
            'horizon4' : QHBoxLayout(),
            'horizon5' : QHBoxLayout(),
            'vertical1' : QVBoxLayout()
        }

        for key in self.boxLayout:
            self.boxLayout[key].addStretch(1)

        self.boxLayout['horizon4'].setDirection(1)
        self.boxLayout['horizon5'].setDirection(1)

        # layout setting
        layout_struct = [
            [self.label['name'], self.lineEdit['name'], self.label['age'], self.lineEdit['age'],
             self.label['score'], self.lineEdit['score']],
            [self.label['amount'], self.lineEdit['amount'], self.label['sort'],
             self.comboBox['sort']],
            [self.pushButton['add'], self.pushButton['del'], self.pushButton['find'],
             self.pushButton['inc'], self.pushButton['show']],
            [self.label['result']],
            [self.textEdit['result']],
            [self.boxLayout['horizon1'], self.boxLayout['horizon2'], self.boxLayout['horizon3'],
             self.boxLayout['horizon4'], self.boxLayout['horizon5']]
        ]

        for idx, layout in enumerate(self.boxLayout):
            for widget in layout_struct[idx]:
                if idx == len(self.boxLayout) - 1:
                    self.boxLayout[layout].addLayout(widget)

                else:
                    self.boxLayout[layout].addWidget(widget)

        # Set Interace Layout
        self.setLayout(self.boxLayout['vertical1'])
        self.setLayoutDirection(0)

        # Event Handle
        self.pushButton['add'].clicked.connect(self.addScoreDB)
        self.pushButton['del'].clicked.connect(self.delScoreDB)
        self.pushButton['show'].clicked.connect(self.showScoreDB)
        self.pushButton['find'].clicked.connect(self.findScoreDB)
        self.pushButton['inc'].clicked.connect(self.increasScoreDB)

        # Interface Position Setting
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Assignment6')
        self.show()

    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')

        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)

        except:
            print("Fail to loading scoredb...")

        else:

            # Casting Data Type 'String' to 'Integer'
            for target in self.scoredb:
                target['Score'], target['Age'] = int(target['Score']), int(target['Age'])

            print("Open DB: ", self.dbfilename)

        fH.close()


    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    # show the scoredb
    def showScoreDB(self, isFirst=False):

        # dashboard는 scoredb에 기록할 전체내용을 담은 문자열, keyname은 정렬 기준이 되는 값
        dashboard = ''
        keyname = ''

        # scoredb의 내용을 처음 보여주는게 아닌지 확인
        if not isFirst:

            # showButton을 눌러서 보여진게 아니라면 이름순으로 정렬
            if self.sender().text() != 'Show':
                keyname = 'Name'

            else :
                keyname = self.comboBox['sort'].currentText()
                #keyname = self.sortComboBox.currentText()

        else:
            keyname = self.comboBox['sort'].currentText()

        # scoredb를 타겟 키를 기준으로 정렬(오름차순)
        try:
            for p in sorted(self.scoredb, key=lambda person: person[keyname]):
                for attr in sorted(p):
                    if attr == "Age" or attr == "Score":
                        dashboard += str(attr) + "=" + str(p[attr]) + '\t'

                    else:
                        dashboard += str(attr) + "=" + p[attr] + '\t'

                dashboard += '\n'

        except KeyError as key_error:
            print("Please Input Valid Key!!!")

        # 결과창에 scoredb의 내용을 띄운다.
        self.textEdit['result'].setPlainText(dashboard)

    # add person to scoredb
    def addScoreDB(self):

        # 각각의 텍스트 입력창으로부터 값을 읽어와 디셔너리 형태로 저장한다.
        record = {'Name': self.lineEdit['name'].text().strip().capitalize(), 'Age': int(self.lineEdit['age'].text().strip()), 'Score': int(self.lineEdit['score'].text().strip())}
        self.scoredb += [record]

        # 추가가 성공적으로 이루어졌는지 확인한다.(정렬기준 : 이름)
        self.showScoreDB()

    # delete person in scoredb
    def delScoreDB(self):

        # 새로 등록할 DataBase를 생성
        new_scdb = []

        # 지울 이름에 해당하는 딕셔너리들을 제외한 나머지를 담는다.
        for p in self.scoredb:
            if p['Name'] == self.lineEdit['name'].text().strip().capitalize():
                pass

            else:
                new_scdb.append(p)

        # scoredb의 refernece를 읽지 않고 리스트를 비우기 위해 clear()를 사용
        self.scoredb.clear()

        for p in new_scdb:
            self.scoredb.append(p)

        # 삭제가 성공적으로 되었는지 확인(정렬기준 : 이름)
        self.showScoreDB()

    # increase target person's score
    def increasScoreDB(self):

        # 증가시킬 값을 amount 입력창으로부터 가져옴
        value = self.lineEdit['amount'].text().strip()

        # 문자열을 숫자데이터 타입으로 변환
        try:
            if value in '.':
                value = float(value)

            else:
                value = int(value)

        except:
            print("Value must be an Integer or Float")
            return True

        # value값 만큼 해당되는 사람들의 점수를 올린다.
        for p in self.scoredb:
            if p['Name'] == self.lineEdit['name'].text().strip():
                p['Score'] += int(value)

        # 증가가 성공적으로 이루어졌는지 확인(정렬기준 : 이름)
        self.showScoreDB()

    # find person
    def findScoreDB(self):

        # 결과 창에 보여질 전체 문자열
        wanted = ''

        # 찾고자 하는 이름에 해당하는 사람들을 출력
        for p in self.scoredb:
            if p['Name'] == self.lineEdit['name'].text().strip():
                for attr in p:
                    if attr == "Age" or attr == "Score":
                        wanted += str(attr) + "=" + str(p[attr]) + '\t'

                    else:
                        wanted += str(attr) + "=" + p[attr] + '\t'

                wanted += '\n'

        # 찾고자 하는 사람들을 출력
        self.resultTextEdit.setPlainText(wanted)

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())
