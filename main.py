import sys, os
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog
from PySide2 import QtCore
from database import Database
from login import Ui_Login
from home import Ui_Home
from clients import Ui_ClientEdit
from sorder import Ui_SOrderEdit
from viacep import ViaCEP
from pysqlcipher3 import dbapi2 as sqlite3



class App(Ui_Login):
    def __ini__(self):
                pass

    def loginCheck(self):
        print('Checando login')
        banco = Database('database.db')
        if 'banco.db' not in os.listdir():
            banco.createDB()
        user = self.leuser.text()
        passwd = self.lepass.text()
        sql = f"SELECT * FROM users WHERE login='{user}' AND passwd='{passwd}'"
        resultado = banco.queryDB(sql)
        if len(resultado) >= 1:
            self.openHome()
            Login.hide()
            print('Logado.')
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Falha no Login')
            msg.setText('Dados incorretos, tente novamente.')
            msg.exec_()
            print('Dados inválidos.')

    def openHome(self):
        print('Abrindo Home')
        self.Home = QMainWindow()
        self.home = Ui_Home()
        self.home.setupUi(self.Home)
        self.home.pbClient.clicked.connect(self.openCliEdit)
        self.home.pbSo.clicked.connect(self.openSO)
        self.Home.show()

    def openCliEdit(self):
        def setAdress(cep):
            try:
                result = ViaCEP(cep)
                result = result.getDadosCEP()
                self.cliedit.leCep.setText(result['cep'])
                self.cliedit.leStreet.setText(result['logradouro'])
                self.cliedit.leDistrict.setText(result['bairro'])
                self.cliedit.leCity.setText(result['localidade'])
                self.cliedit.leState.setText(result['uf'])
                self.cliedit.leContry.setText('Brasil')
                self.cliedit.leNumber.setFocus()
            except:
                pass

        def saveCli():
            try:
                banco = Database('database.db')
                sql = f"""INSERT INTO clients (regdate, regtype, blocked,
                name, birth, sex, cpfcnpj, rgie, tel1, tel2, tel3, email, cep,
                adress, number, adress2, district, city, state, contry)
                VALUES (datetime('now'), '{self.cliedit.buttonGroup.checkedButton().text()}' ,
                '{self.cliedit.checkBox.isChecked()}', '{self.cliedit.leName.text()}',
                '{self.cliedit.dateEdit.date()}', '{self.cliedit.buttonGroup_2.checkedButton().text()}',
                '{self.cliedit.leCpf.text()}', '{self.cliedit.leRg.text()}',
                '{self.cliedit.leCell1.text()}', '{self.cliedit.leCell2.text()}',
                '{self.cliedit.leTel.text()}', '{self.cliedit.leMail.text()}',
                '{self.cliedit.leCep.text()}', '{self.cliedit.leStreet.text()}',
                '{self.cliedit.leNumber.text()}', '{self.cliedit.leComp.text()}',
                '{self.cliedit.leDistrict.text()}', '{self.cliedit.leCity.text()}',
                '{self.cliedit.leState.text()}', '{self.cliedit.leContry.text()}')"""
                banco.queryDB(sql)
                sql = f"SELECT * FROM clients WHERE cpfcnpj='{self.cliedit.leCpf.text()}' OR rgie='{self.cliedit.leRg.text()}' OR email='{self.cliedit.leMail.text()}'"
                resultado = banco.queryDB(sql)
                print('Resultado: ', resultado)
                self.cliedit.leCodCli.setText(str(resultado[0][0]))
                self.cliedit.dateEdit_2.setEnabled(True)
                self.cliedit.dateEdit_2.dateTimeFromText(resultado[0][1][:10])
                if resultado[0][2] == 'PF':
                    self.cliedit.radioButton.setChecked(True)
                else:
                    self.cliedit.radioButton_2.setChecked(False)
                if resultado[0][3] == 'True' and self.cliedit.checkBox.checkState() == False:
                    self.cliedit.checkBox.setChecked(True)
                elif resultado[0][3] == 'False' and self.cliedit.checkBox.checkState() == True:
                    self.cliedit.checkBox.setChecked(False)
                self.cliedit.leName.setText(resultado[0][4])
                self.cliedit.dateEdit.dateTimeFromText(resultado[0][5])
                if resultado[0][6] == 'F':
                    self.cliedit.rbF.setChecked(True)
                else:
                    self.cliedit.rbM.setChecked(True)
                self.cliedit.leCpf.setText(resultado[0][7])
                self.cliedit.leRg.setText(resultado[0][8])
                self.cliedit.leCell1.setText(resultado[0][9])
                self.cliedit.leCell2.setText(resultado[0][10])
                self.cliedit.leTel.setText(resultado[0][11])
                self.cliedit.leMail.setText(resultado[0][12])
                self.cliedit.leCep.setText(resultado[0][13])
                self.cliedit.leStreet.setText(resultado[0][14])
                self.cliedit.leNumber.setText(resultado[0][15])
                self.cliedit.leComp.setText(resultado[0][16])
                self.cliedit.leDistrict.setText(resultado[0][17])
                self.cliedit.leCity.setText(resultado[0][18])
                self.cliedit.leState.setText(resultado[0][19])
                self.cliedit.leContry.setText(resultado[0][20])
                self.cliedit.pbDelete.setEnabled(True)
                self.cliedit.pbNew.setEnabled(True)

            except sqlite3.IntegrityError as e:
                msg = QMessageBox()
                msg.setWindowTitle('Falha ao salvar.')
                print(e.args)
                if 'clients.email' in e.args[0]:
                    msg.setText(f'Este E-mail já está sendo utilizado.')
                if 'clients.cpfcnpj' in e.args[0]:
                    msg.setText(f'Este CPF/CNPJ já está sendo utilizado.')
                if 'clients.rgie' in e.args[0]:
                    msg.setText(f'Este RG/IE já está sendo utilizado.')
                msg.exec_()
                pass

        print('Abrindo Cli edit')
        self.CliEdit = QDialog()
        self.cliedit = Ui_ClientEdit()
        self.cliedit.setupUi(self.CliEdit)
        self.cliedit.radioButton_2.clicked.connect(lambda: self.cliedit.lbCpf.setText('CNPJ'))
        self.cliedit.radioButton_2.clicked.connect(lambda: self.cliedit.lbRg.setText('IE'))
        self.cliedit.radioButton.clicked.connect(lambda: self.cliedit.lbCpf.setText('CPF'))
        self.cliedit.radioButton.clicked.connect(lambda: self.cliedit.lbRg.setText('RG'))
        self.cliedit.leCep.editingFinished.connect(lambda: setAdress(self.cliedit.leCep.text()))
        self.cliedit.pbSave.clicked.connect(lambda: saveCli())
        self.CliEdit.show()

    def openSO(self):
        print('Abrindo SO edit')
        self.SOrder = QDialog()
        self.sorder = Ui_SOrderEdit()
        self.sorder.setupUi(self.SOrder)
        self.SOrder.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = QDialog()
    w = App()
    w.setupUi(Login)
    QtCore.QObject.connect(w.buttonBox, QtCore.SIGNAL("accepted()"),
                           w.loginCheck)
    Login.show()
    sys.exit(app.exec_())
