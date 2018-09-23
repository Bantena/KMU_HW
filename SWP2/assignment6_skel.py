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
        self.showScoreDB()

    def initUI(self):

        # Interface Labels
        self.nameLabel = QLabel("Name : ")
        self.ageLabel = QLabel("Age : ")
        self.scoreLabel = QLabel("Score : ")
        self.amountLabel = QLabel("Amount : ")
        self.sortLabel = QLabel("Key : ")
        self.resultLabel = QLabel("Result : ")

        # Interface TextBox
        self.nameTextBox = QLineEdit()
        self.ageTextBox = QLineEdit()
        self.scoreTextBox = QLineEdit()
        self.amountTextBox = QLineEdit()

        # Interface ComboBox
        self.sortComboBox = QComboBox()
        self.sortComboBox.addItems(['Name', 'Age', 'Score'])

        # Interface Buttons
        self.addButton = QPushButton("Add")
        self.delButton = QPushButton('Delete')
        self.findButton = QPushButton('Find')
        self.incButton = QPushButton('Increase')
        self.showButton = QPushButton('Show')

        # Interface TextEdit
        self.resultTextEdit = QTextEdit()
        self.resultTextEdit.setReadOnly(True)

        # Interface Layout
        horizentalLayout1 = QHBoxLayout()
        horizentalLayout1.addStretch(1)
        horizentalLayout1.addWidget(self.nameLabel)
        horizentalLayout1.addWidget(self.nameTextBox)
        horizentalLayout1.addWidget(self.ageLabel)
        horizentalLayout1.addWidget(self.ageTextBox)
        horizentalLayout1.addWidget(self.scoreLabel)
        horizentalLayout1.addWidget(self.scoreTextBox)

        horizentalLayout2 = QHBoxLayout()
        horizentalLayout2.addStretch(1)
        horizentalLayout2.addWidget(self.amountLabel)
        horizentalLayout2.addWidget(self.amountTextBox)
        horizentalLayout2.addWidget(self.sortLabel)
        horizentalLayout2.addWidget(self.sortComboBox)

        horizentalLayout3 = QHBoxLayout()
        horizentalLayout3.addStretch(1)
        horizentalLayout3.addWidget(self.addButton)
        horizentalLayout3.addWidget(self.delButton)
        horizentalLayout3.addWidget(self.findButton)
        horizentalLayout3.addWidget(self.incButton)
        horizentalLayout3.addWidget(self.showButton)

        horizentalLayout4 = QHBoxLayout()
        horizentalLayout4.addStretch(1)
        horizentalLayout4.addWidget(self.resultLabel)

        horizentalLayout5 = QHBoxLayout()
        horizentalLayout5.addStretch(1)
        horizentalLayout5.addWidget(self.resultTextEdit)

        verticalLayout = QVBoxLayout()
        verticalLayout.addStretch(1)
        verticalLayout.addLayout(horizentalLayout1)
        verticalLayout.addLayout(horizentalLayout2)
        verticalLayout.addLayout(horizentalLayout3)
        verticalLayout.addLayout(horizentalLayout4)
        verticalLayout.addLayout(horizentalLayout5)

        # Set Interace Layout
        self.setLayout(verticalLayout)

        # Event Handle
        self.addButton.clicked.connect(self.addScoreDB)
        self.delButton.clicked.connect(self.delScoreDB)
        self.showButton.clicked.connect(self.showScoreDB)
        self.findButton.clicked.connect(self.findScoreDB)
        self.incButton.clicked.connect(self.increasScoreDB)

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

    def showScoreDB(self):
        dashboard = ''
        keyname = self.sortComboBox.currentText()

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

        self.resultTextEdit.setPlainText(dashboard)

    def addScoreDB(self):
        record = {'Name': self.nameTextBox.text().strip(), 'Age': int(self.ageTextBox.text().strip()), 'Score': int(self.scoreTextBox.text().strip())}
        self.scoredb += [record]

        self.showScoreDB()

    def delScoreDB(self):
        new_scdb = []

        for p in self.scoredb:
            if p['Name'] == self.nameTextBox.text().strip():
                pass

            else:
                new_scdb.append(p)

        self.scoredb.clear()

        for p in new_scdb:
            self.scoredb.append(p)

        self.showScoreDB()

    def increasScoreDB(self):

        value = self.amountTextBox.text()

        try:
            if value in '.':
                value = float(value)

            else:
                value = int(value)

        except:
            print("Value must be an Integer or Float")
            return True

        for p in self.scoredb:
            if p['Name'] == self.nameTextBox.text().strip():
                p['Score'] += int(value)

        # 아직 구현이 덜 됨
        self.showScoreDB()

    def findScoreDB(self):
        wanted = ''
        for p in self.scoredb:
            if p['Name'] == self.nameTextBox.text().strip():
                for attr in p:
                    if attr == "Age" or attr == "Score":
                        wanted += str(attr) + "=" + str(p[attr]) + '\t'

                    else:
                        wanted += str(attr) + "=" + p[attr] + '\t'

                wanted += '\n'

        self.resultTextEdit.setPlainText(wanted)

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

