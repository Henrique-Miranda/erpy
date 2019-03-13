import sys, os
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog, QTableWidgetItem
from PySide2 import QtCore, Qt
from database import Database
from login import Ui_Login
from home import Ui_Home
from clients import Ui_ClientEdit
from sorder import Ui_SOrderEdit
from viacep import ViaCEP
from pysqlcipher3 import dbapi2 as sqlite3
from pycpfcnpj import cpfcnpj as cpfcnpjv

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

    def loadSearch(self, data, local):
        banco = Database('database.db')
        if local == 'Cliente': local = 'clients'
        if local == 'Ordem de Serviço': local = 'service_order'
        sql = f"SELECT * FROM '{local}' WHERE name LIKE '{data}%'"
        resultado = banco.queryDB(sql)
        print('sql: ', sql)
        print(resultado)
        self.home.tableWidget.setRowCount(len(resultado))
        self.home.tableWidget.setColumnCount(len(resultado[0]))
        self.home.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome', 'Nascimento', 'Sexo', 'CPF', 'RG', 'Celular 1',
        'Celular 2', 'Telefone 3', 'E-Mail', 'CEP', 'Endereço', 'Número', 'Complemento', 'Bairro', 'Cidade', 'Estado', 'País'])
        for column, item in enumerate(resultado):
            self.home.tableWidget.setItem(column, 0, QTableWidgetItem(str(item[0])))
            self.home.tableWidget.setItem(column, 1, QTableWidgetItem(str(item[5])))
            self.home.tableWidget.setItem(column, 2, QTableWidgetItem(str(item[6])))
            self.home.tableWidget.setItem(column, 3, QTableWidgetItem(str(item[7])))
            self.home.tableWidget.setItem(column, 4, QTableWidgetItem(str(item[8])))
            self.home.tableWidget.setItem(column, 5, QTableWidgetItem(str(item[9])))
        self.home.tableWidget.itemDoubleClicked.connect(lambda: self.openCliEdit(data = int(resultado[self.home.tableWidget.currentRow()][0])))

    def openHome(self):
        print('Abrindo Home')
        self.Home = QMainWindow()
        self.home = Ui_Home()
        self.home.setupUi(self.Home)
        self.home.pbClient.clicked.connect(self.openCliEdit)
        self.home.pbSo.clicked.connect(self.openSO)
        self.home.leSearch.returnPressed.connect(lambda: self.loadSearch(self.home.leSearch.text(), self.home.cbSearch.currentText()))
        self.Home.show()

    def openCliEdit(self, data = 0):
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

        def loadCli(data, field = "id"):
            banco = Database('database.db')
            sql = f"""SELECT * FROM clients WHERE {field}='{data}'"""
            print('SQL:', sql)
            banco.queryDB(sql)
            resultado = banco.queryDB(sql)
            print('Resultado: ', resultado)
            self.cliedit.leCodCli.setText(str(resultado[0][0]))
            self.cliedit.dateTimeCad.setEnabled(True)
            self.cliedit.dateTimeCad.setDateTime(QtCore.QDateTime.fromString(resultado[0][1], QtCore.Qt.ISODate))
            self.cliedit.dateTimeAlt.setEnabled(True)
            self.cliedit.dateTimeAlt.setDateTime(QtCore.QDateTime.fromString(resultado[0][2], QtCore.Qt.ISODate))
            if resultado[0][3] == 'PF':
                self.cliedit.radioButton.setChecked(True)
            else:
                self.cliedit.radioButton_2.setChecked(False)
            if resultado[0][4] and not self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(True)
            elif not resultado[0][4] and self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(False)
            self.cliedit.leName.setText(resultado[0][5])
            self.cliedit.deBirthFun.setDate(QtCore.QDate.fromString(resultado[0][6], QtCore.Qt.ISODate))
            if resultado[0][7] == 'F':
                self.cliedit.rbF.setChecked(True)
            else:
                self.cliedit.rbM.setChecked(True)
            self.cliedit.leCpfCnpj.setText(resultado[0][8])
            self.cliedit.leRgIe.setText(resultado[0][9])
            self.cliedit.leCell1.setText(resultado[0][10])
            self.cliedit.leCell2.setText(resultado[0][11])
            self.cliedit.leTel.setText(resultado[0][12])
            self.cliedit.leMail.setText(resultado[0][13])
            self.cliedit.leCep.setText(resultado[0][14])
            self.cliedit.leStreet.setText(resultado[0][15])
            self.cliedit.leNumber.setText(resultado[0][16])
            self.cliedit.leComp.setText(resultado[0][17])
            self.cliedit.leDistrict.setText(resultado[0][18])
            self.cliedit.leCity.setText(resultado[0][19])
            self.cliedit.leState.setText(resultado[0][20])
            self.cliedit.leContry.setText(resultado[0][21])
            self.cliedit.leCodCli.setEnabled(True)
            self.cliedit.pbDelete.setEnabled(True)
            self.cliedit.pbNew.setEnabled(True)

        def saveCli():
            try:
                banco = Database('database.db')
                name = self.cliedit.leName.text().title()
                assert name != '', 'Digite o nome do cliente!'
                birth = self.cliedit.deBirthFun.date().toString(QtCore.Qt.ISODate)
                idade = int(QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)[0:4]) - int(birth[0:4])
                assert idade >= 18, 'Este cliente tem menos de 18 anos!'
                cpfcnpj = self.cliedit.leCpfCnpj.text().strip()
                assert cpfcnpjv.validate(cpfcnpj) == True, 'CPF/CNPJ inválido!'
                rgie = self.cliedit.leRgIe.text().strip()
                if rgie == '':
                    rgie = None
                email = self.cliedit.leMail.text().strip()

                sql = f"""INSERT INTO clients (regdate, altdate, regtype, blocked,
                name, birthFun, sex, cpfcnpj, rgie, tel1, tel2, tel3, email, cep,
                adress, number, adress2, district, city, state, contry)
                VALUES ('{QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)}',
                '{QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)}',
                '{self.cliedit.buttonGroup.checkedButton().text()}',
                '{int(self.cliedit.checkBox.isChecked())}', '{name}', '{birth}',
                '{self.cliedit.buttonGroup_2.checkedButton().text()}',
                '{cpfcnpj}', '{rgie}', '{self.cliedit.leCell1.text()}', '{self.cliedit.leCell2.text()}',
                '{self.cliedit.leTel.text()}', '{email}',
                '{self.cliedit.leCep.text()}', '{self.cliedit.leStreet.text()}',
                '{self.cliedit.leNumber.text()}', '{self.cliedit.leComp.text()}',
                '{self.cliedit.leDistrict.text()}', '{self.cliedit.leCity.text()}',
                '{self.cliedit.leState.text()}', '{self.cliedit.leContry.text()}')"""
                loadCli()

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
            except AssertionError as e:
                msg = QMessageBox()
                msg.setWindowTitle('Falha ao salvar.')
                print(e.args)
                msg.setText(e.args[0])
                msg.exec_()

        print('Abrindo Cli edit')
        self.CliEdit = QDialog()
        self.cliedit = Ui_ClientEdit()
        self.cliedit.setupUi(self.CliEdit)
        def cnpj():
            self.cliedit.lbCpfCnpj.setText('CNPJ:')
            self.cliedit.lbRgIe.setText('IE:')
            self.cliedit.leRgIe.setInputMask(QApplication.translate("ClientEdit", "", None, -1))
            self.cliedit.leCpfCnpj.setInputMask(QApplication.translate("ClientEdit", "00.000.000/0000-00", None, -1))
            self.cliedit.lbBirthFun.setText('Fundação:')
            self.cliedit.lbSex.hide()
            self.cliedit.rbF.hide()
            self.cliedit.rbM.hide()

        def cpf():
            self.cliedit.lbCpfCnpj.setText('CPF:')
            self.cliedit.lbRgIe.setText('RG:')
            self.cliedit.leRgIe.setInputMask(QApplication.translate("ClientEdit", "00.000.000-0", None, -1))
            self.cliedit.leCpfCnpj.setInputMask(QApplication.translate("ClientEdit", "000.000.000-00", None, -1))
            self.cliedit.lbBirthFun.setText('Nascimento:')
            self.cliedit.lbSex.show()
            self.cliedit.rbF.show()
            self.cliedit.rbM.show()

        self.cliedit.radioButton_2.clicked.connect(cnpj)
        self.cliedit.radioButton.clicked.connect(cpf)
        self.cliedit.leCep.editingFinished.connect(lambda: setAdress(self.cliedit.leCep.text()))
        self.cliedit.pbSave.clicked.connect(lambda: saveCli())
        self.CliEdit.show()
        if data != 0:
            loadCli(data)

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
