import sys, os, sqlite3, socket
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog, QTableWidgetItem
from PySide2 import QtCore
from database import Database
from login import Ui_Login
from home import Ui_Home
from clients import Ui_ClientEdit
from sorder import Ui_SOrderEdit
from viacep import ViaCEP
from pycpfcnpj import cpfcnpj as cpfcnpjv

class App(Ui_Login):
    def __ini__(self):
        self.userId = None
        self.userName = None
        self.fullName = None
        self.hostName = None
        self.userIP = None
        self.logged = False
    # Start login
    def loginCheck(self):
        banco = Database('database.db')
        if 'database.db' not in os.listdir():
            banco.createDB()
        user = self.leuser.text()
        passwd = self.lepass.text()
        sql = f"SELECT * FROM users WHERE login='{user}' AND passwd='{passwd}'"
        result = banco.queryDB(sql)
        if result:
            self.userId = result[0][0]
            self.fullName = result[0][1]
            self.user = result[0][2]
            self.hostName = socket.gethostname()
            self.userIP = socket.gethostbyname(self.hostName)
            self.logged = True
            self.openHome()
            Login.hide()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Falha no Login')
            msg.setText('Dados incorretos, tente novamente.')
            msg.exec_()
    # End login
    # Start openHome
    def openHome(self):
        self.Home = QMainWindow()
        self.home = Ui_Home()
        self.home.setupUi(self.Home)
        self.home.pbClient.clicked.connect(self.openCliEdit)
        self.home.actionClient.triggered.connect(self.openCliEdit)
        self.home.leSearch.returnPressed.connect(lambda: self.loadSearch(self.home.leSearch.text(), self.home.cbSearch.currentText()))
        self.home.pbSearch.clicked.connect(lambda: self.loadSearch(self.home.leSearch.text(), self.home.cbSearch.currentText()))
        self.home.tableWidget.setColumnCount(12)
        self.home.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome',
        'Nascimento', 'Sexo', 'CPF/CNPJ', 'RG/IE', 'Operadora 1', 'Celular 1',
        'Operadora 2', 'Celular 2', 'Telefone', 'E-Mail'])
        self.home.statusbar.showMessage(f'Usuário: {self.fullName}          IP: {self.userIP}          Hostname: {self.hostName}')
        self.Home.show()
    # End openHome
    # Start loadSearch
    def loadSearch(self, data, local):
        if len(data) == 11 and cpfcnpjv.validate(data):
            data = f'{data[0:3]}.{data[3:6]}.{data[6:9]}-{data[9:]}'

        banco = Database('database.db')
        if local == 'Cliente':
            sql = f"SELECT * FROM clients WHERE name LIKE '{data}%' OR cpfcnpj LIKE '{data}%' ORDER BY id DESC LIMIT 100"
            result = banco.queryDB(sql)
            self.home.tableWidget.setRowCount(len(result))
            self.home.tableWidget.setColumnCount(12)
            self.home.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome',
            'Nascimento', 'Sexo', 'CPF/CNPJ', 'RG/IE', 'Operadora 1', 'Celular 1',
            'Operadora 2', 'Celular 2', 'Telefone', 'E-Mail'])

            for column, item in enumerate(result):
                self.home.tableWidget.setItem(column, 0, QTableWidgetItem(str(item[0])))
                self.home.tableWidget.setItem(column, 1, QTableWidgetItem(item[6]))
                self.home.tableWidget.setItem(column, 2, QTableWidgetItem(f'{item[7][8:10]}/{item[7][5:7]}/{item[7][0:4]}'))
                self.home.tableWidget.setItem(column, 3, QTableWidgetItem(item[8]))
                self.home.tableWidget.setItem(column, 4, QTableWidgetItem(item[9]))
                self.home.tableWidget.setItem(column, 5, QTableWidgetItem(item[10]))
                self.home.tableWidget.setItem(column, 6, QTableWidgetItem(item[11]))
                self.home.tableWidget.setItem(column, 7, QTableWidgetItem(item[12]))
                self.home.tableWidget.setItem(column, 8, QTableWidgetItem(item[13]))
                self.home.tableWidget.setItem(column, 9, QTableWidgetItem(item[14]))
                self.home.tableWidget.setItem(column, 10, QTableWidgetItem(item[15]))
                self.home.tableWidget.setItem(column, 11, QTableWidgetItem(item[16]))
                self.home.tableWidget.setItem(column, 12, QTableWidgetItem(item[17]))

        if local == 'Ordem de Serviço':
            try:
                data = int(data)
                sql = f"""SELECT service_order.id, clients.name, clients.cpfcnpj, \
                    service_order.deviceType, service_order.brand, service_order.model, \
                    service_order.color, clients.cell1op, clients.cell1, clients.cell2op, \
                    clients.cell2, clients.tel FROM service_order INNER JOIN clients ON \
                    clients.id=service_order.idCli WHERE service_order.id={data}"""
            except:
                sql = f"""SELECT service_order.id, clients.name, service_order.entryDate, \
                    clients.cpfcnpj, service_order.deviceType, service_order.brand, service_order.model, \
                    service_order.color, clients.cell1op, clients.cell1, clients.cell2op, \
                    clients.cell2, clients.tel FROM service_order INNER JOIN clients ON \
                    clients.id=service_order.idCli WHERE clients.cpfcnpj LIKE '{data}%' OR \
                    clients.name LIKE '{data}%' OR service_order.brand LIKE '{data}%' OR \
                    service_order.model LIKE '{data}%' ORDER BY regdate DESC LIMIT 100"""

            result = banco.queryDB(sql)
            self.home.tableWidget.setRowCount(len(result))
            self.home.tableWidget.setColumnCount(13)
            self.home.tableWidget.setHorizontalHeaderLabels(['OS', 'Cliente',
            'Data de entrada', 'CPF/CNPJ', 'Aparelho', 'Marca', 'Modelo', 'Cor',
            'Operadora 1', 'Celular 1', 'Operadora 2', 'Celular 2', 'Telefone'])

            for column, item in enumerate(result):
                self.home.tableWidget.setItem(column, 0, QTableWidgetItem(str(item[0])))
                self.home.tableWidget.setItem(column, 1, QTableWidgetItem(item[1]))
                self.home.tableWidget.setItem(column, 2, QTableWidgetItem(f'{item[2][8:10]}/{item[2][5:7]}/{item[2][0:4]} {item[2].split()[1]}'))
                self.home.tableWidget.setItem(column, 3, QTableWidgetItem(item[3]))
                self.home.tableWidget.setItem(column, 4, QTableWidgetItem(item[4]))
                self.home.tableWidget.setItem(column, 5, QTableWidgetItem(item[5]))
                self.home.tableWidget.setItem(column, 6, QTableWidgetItem(item[6]))
                self.home.tableWidget.setItem(column, 7, QTableWidgetItem(item[7]))
                self.home.tableWidget.setItem(column, 8, QTableWidgetItem(item[8]))
                self.home.tableWidget.setItem(column, 9, QTableWidgetItem(item[9]))
                self.home.tableWidget.setItem(column, 10, QTableWidgetItem(item[10]))
                self.home.tableWidget.setItem(column, 11, QTableWidgetItem(item[11]))
                self.home.tableWidget.setItem(column, 12, QTableWidgetItem(item[12]))
        try:
            self.home.tableWidget.itemDoubleClicked.disconnect()
        except:
            pass
        if local == 'Ordem de Serviço':
            self.home.tableWidget.itemDoubleClicked.connect(lambda: self.openSO(int(result[self.home.tableWidget.currentRow()][0])))
        if local == 'Cliente':
            self.home.tableWidget.itemDoubleClicked.connect(lambda: self.openCliEdit(int(result[self.home.tableWidget.currentRow()][0])))
        print('SQL Search: ', sql)
        print('Result OS: ', result)
    # End loadSearch
    # Start openCliEdit
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

        def loadCli(data):
            banco = Database('database.db')
            sql = f'SELECT * FROM clients WHERE id={data}'
            print('SQL loadcli:', sql)
            result = banco.queryDB(sql)
            print('Resultado loadcli: ', result)
            self.cliedit.leCodCli.setText(str(result[0][0]))
            self.cliedit.dateTimeCad.setEnabled(True)
            self.cliedit.dateTimeCad.setDateTime(QtCore.QDateTime.fromString(result[0][1], 'yyyy-MM-dd hh:mm:ss'))
            self.cliedit.dateTimeAlt.setEnabled(True)
            self.cliedit.dateTimeAlt.setDateTime(QtCore.QDateTime.fromString(result[0][2], 'yyyy-MM-dd hh:mm:ss'))
            if result[0][4] == 'PF':
                self.cliedit.radioButton.setChecked(True)
                self.cliedit.leCpfCnpj.setMaxLength(14)
            else:
                self.cliedit.lbCpfCnpj.setText('CNPJ')
                self.cliedit.lbRgIe.setText('IE')
                self.cliedit.lbBirthFun.setText('Fundação')
                self.cliedit.rbF.hide()
                self.cliedit.rbM.hide()
                self.cliedit.lbSex.hide()
                self.cliedit.radioButton_2.setChecked(True)
                self.cliedit.leCpfCnpj.setMaxLength(18)
            if result[0][5] and not self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(True)
            elif not result[0][5] and self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(False)
            self.cliedit.leName.setText(result[0][6])
            self.cliedit.deBirthFun.setDate(QtCore.QDate.fromString(result[0][7], 'yyyy-MM-dd'))
            if result[0][8] == 'F':
                self.cliedit.rbF.setChecked(True)
            else:
                self.cliedit.rbM.setChecked(True)
            self.cliedit.leCpfCnpj.setText(result[0][9])
            self.cliedit.leRgIe.setText(result[0][10])
            self.cliedit.cbCell1.setCurrentText(result[0][11])
            self.cliedit.leCell1.setText(result[0][12])
            self.cliedit.cbCell2.setCurrentText(result[0][13])
            self.cliedit.leCell2.setText(result[0][14])
            self.cliedit.leTel.setText(result[0][15])
            self.cliedit.leMail.setText(result[0][16])
            self.cliedit.leCep.setText(result[0][17])
            self.cliedit.leStreet.setText(result[0][18])
            self.cliedit.leNumber.setText(result[0][19])
            self.cliedit.leComp.setText(result[0][20])
            self.cliedit.leDistrict.setText(result[0][21])
            self.cliedit.leCity.setText(result[0][22])
            self.cliedit.leState.setText(result[0][23])
            self.cliedit.leContry.setText(result[0][24])
            self.cliedit.leCodCli.setEnabled(True)
            self.cliedit.pbDelete.setEnabled(True)
            self.cliedit.pbNew.setEnabled(True)

        def delCli(id):
            banco = Database('database.db')
            sql = f"DELETE FROM clients WHERE id = '{id}'"
            try:
                banco.queryDB(sql)
                msg = QMessageBox()
                msg.setWindowTitle('Cliente foi excluído.')
                msg.setText('Este cliente foi deletado com sucesso!')
                msg.exec_()
                self.cliedit.pbExit.click()
            except:
                pass

        def saveCli():
            try:
                banco = Database('database.db')
                name = self.cliedit.leName.text().title()
                assert name, 'Digite o nome do cliente!'
                birth = self.cliedit.deBirthFun.date().toString('yyyy-MM-dd')
                idade = int(QtCore.QDate.currentDate().toString('yyyy-MM-dd')[0:4]) - int(birth[0:4])
                if self.cliedit.buttonGroup.checkedButton() == 'PF':
                    assert idade >= 18, 'Este cliente tem menos de 18 anos!'
                cpfcnpj = self.cliedit.leCpfCnpj.text().strip()
                assert cpfcnpjv.validate(cpfcnpj), 'CPF/CNPJ inválido!'
                rgie = self.cliedit.leRgIe.text().strip()
                email = self.cliedit.leMail.text().strip()
                if self.cliedit.leCodCli.text():
                    sql = f"""UPDATE clients SET altdate = '{QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")}', lastAlter={self.userId}, blocked = '{int(self.cliedit.checkBox.isChecked())}',
                    name = '{name}', birthFun = '{birth}', sex = '{self.cliedit.buttonGroup_2.checkedButton().text()}', cpfcnpj='{cpfcnpj}', rgie = '{rgie}',
                    cell1op = '{self.cliedit.cbCell1.currentText()}', cell1 = '{self.cliedit.leCell1.text()}', cell2op = '{self.cliedit.cbCell2.currentText()}',
                    cell2 = '{self.cliedit.leCell2.text()}', tel = '{self.cliedit.leTel.text()}', email = '{email}', cep = '{self.cliedit.leCep.text()}',
                    adress = '{self.cliedit.leStreet.text()}', number = '{self.cliedit.leNumber.text()}', adress2 = '{self.cliedit.leComp.text()}',
                    district = '{self.cliedit.leDistrict.text()}', city = '{self.cliedit.leCity.text()}', state = '{self.cliedit.leState.text()}', contry = '{self.cliedit.leContry.text()}' WHERE id={int(self.cliedit.leCodCli.text())}"""
                    banco.queryDB(sql)
                    loadCli(int(self.cliedit.leCodCli.text()))
                else:
                    sql = f"""INSERT INTO clients (regdate, altdate, lastAlter, regtype, blocked,
                    name, birthFun, sex, cpfcnpj, rgie, cell1op, cell1, cell2op, cell2, tel, email, cep,
                    adress, number, adress2, district, city, state, contry)
                    VALUES ('{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}',
                    '{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}',
                    {self.userId}, '{self.cliedit.buttonGroup.checkedButton().text()}',
                    '{int(self.cliedit.checkBox.isChecked())}', '{name}', '{birth}',
                    '{self.cliedit.buttonGroup_2.checkedButton().text()}',
                    '{cpfcnpj}', '{rgie}', '{self.cliedit.cbCell1.currentText()}',
                    '{self.cliedit.leCell1.text()}', '{self.cliedit.cbCell2.currentText() }', '{self.cliedit.leCell2.text()}',
                    '{self.cliedit.leTel.text()}', '{email}',
                    '{self.cliedit.leCep.text()}', '{self.cliedit.leStreet.text()}',
                    '{self.cliedit.leNumber.text()}', '{self.cliedit.leComp.text()}',
                    '{self.cliedit.leDistrict.text()}', '{self.cliedit.leCity.text()}',
                    '{self.cliedit.leState.text()}', '{self.cliedit.leContry.text()}')"""
                    print('SQL SaveCli: ', sql)
                    lrid = banco.queryDB(sql)
                    print('Last row id: ', lrid)
                    loadCli(lrid)

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
        def mask(widget, maskk = ''):
            if widget == self.cliedit.leCpfCnpj and self.cliedit.buttonGroup.checkedButton().text() == 'PJ' and not maskk:
                widget.setMaxLength(18)
                widget.setInputMask(maskk)
            if widget == self.cliedit.leCpfCnpj and self.cliedit.buttonGroup.checkedButton().text() == 'PF' and not maskk:
                widget.setMaxLength(14)
                widget.setInputMask(maskk)
            if widget == self.cliedit.leCpfCnpj and self.cliedit.buttonGroup.checkedButton().text() == 'PJ' and maskk == "000.000.000-00":
                widget.setMaxLength(18)
                if self.cliedit.leCpfCnpj.text():
                    widget.setInputMask('00.000.000/0000-00')
                else:
                    widget.setInputMask('')
            if widget == self.cliedit.leCpfCnpj and self.cliedit.buttonGroup.checkedButton().text() == 'PF' and maskk == "000.000.000-00":
                widget.setMaxLength(14)
                if self.cliedit.leCpfCnpj.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')

            if widget == self.cliedit.leRgIe and self.cliedit.buttonGroup.checkedButton().text() == 'PJ' and not maskk:
                widget.setMaxLength(18)
                widget.setInputMask(maskk)
            if widget == self.cliedit.leRgIe and self.cliedit.buttonGroup.checkedButton().text() == 'PF' and not maskk:
                widget.setMaxLength(12)
                widget.setInputMask(maskk)
            if widget == self.cliedit.leRgIe and self.cliedit.buttonGroup.checkedButton().text() == 'PJ' and maskk == "00.000.000-0":
                widget.setMaxLength(18)
                widget.setInputMask('')
            if widget == self.cliedit.leRgIe and self.cliedit.buttonGroup.checkedButton().text() == 'PF' and maskk == "00.000.000-0":
                widget.setMaxLength(12)
                if self.cliedit.leRgIe.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')

            if widget == self.cliedit.leCell1 or widget == self.cliedit.leCell2:
                widget.setMaxLength(15)
                if self.cliedit.leCell1.text() or self.cliedit.leCell2.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')

            if widget == self.cliedit.leTel:
                widget.setMaxLength(14)
                if self.cliedit.leTel.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')

            if widget == self.cliedit.leCep:
                widget.setMaxLength(9)
                if self.cliedit.leCep.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')


        def cnpj():
            self.cliedit.lbCpfCnpj.setText('CNPJ:')
            self.cliedit.lbRgIe.setText('IE:')
            self.cliedit.lbBirthFun.setText('Fundação:')
            self.cliedit.lbSex.hide()
            self.cliedit.rbF.hide()
            self.cliedit.rbM.hide()

        def cpf():
            self.cliedit.lbCpfCnpj.setText('CPF:')
            self.cliedit.lbRgIe.setText('RG:')
            self.cliedit.lbBirthFun.setText('Nascimento:')
            self.cliedit.lbSex.show()
            self.cliedit.rbF.show()
            self.cliedit.rbM.show()

        self.cliedit.radioButton_2.clicked.connect(cnpj)
        self.cliedit.radioButton.clicked.connect(cpf)
        self.cliedit.leCep.editingFinished.connect(lambda: setAdress(self.cliedit.leCep.text()))
        self.cliedit.pbSave.clicked.connect(saveCli)
        self.cliedit.pbNew.clicked.connect(self.cliedit.pbExit.click)
        self.cliedit.pbNew.clicked.connect(lambda: self.openSO(idC = int(self.cliedit.leCodCli.text())))
        self.cliedit.pbDelete.clicked.connect(lambda: delCli(int(self.cliedit.leCodCli.text())))
        self.cliedit.leCpfCnpj.textEdited.connect(lambda: mask(self.cliedit.leCpfCnpj))
        self.cliedit.leCpfCnpj.editingFinished.connect(lambda: mask(self.cliedit.leCpfCnpj, '000.000.000-00'))
        self.cliedit.leRgIe.textEdited.connect(lambda: mask(self.cliedit.leRgIe))
        self.cliedit.leRgIe.editingFinished.connect(lambda: mask(self.cliedit.leRgIe, '00.000.000-0'))
        self.cliedit.leCell1.textEdited.connect(lambda: mask(self.cliedit.leCell1))
        self.cliedit.leCell1.editingFinished.connect(lambda: mask(self.cliedit.leCell1, '(00)00000-0000'))
        self.cliedit.leCell2.textEdited.connect(lambda: mask(self.cliedit.leCell2))
        self.cliedit.leCell2.editingFinished.connect(lambda: mask(self.cliedit.leCell2, '(00)00000-0000'))
        self.cliedit.leTel.textEdited.connect(lambda: mask(self.cliedit.leTel))
        self.cliedit.leTel.editingFinished.connect(lambda: mask(self.cliedit.leTel, '(00)0000-0000'))
        self.cliedit.leCep.textEdited.connect(lambda: mask(self.cliedit.leCep))
        self.cliedit.leCep.editingFinished.connect(lambda: mask(self.cliedit.leCep, '00000-000'))
        self.CliEdit.show()

        if data:
            loadCli(data)
    # End openCliEdit
    # Start openSO
    def openSO(self, id = 0, idC = 0):
        def loadOs(id):
            banco = Database('database.db')
            if not idC:
                sql = f"""SELECT clients.name, clients.birthFun, clients.sex, clients.cpfcnpj, clients.rgie, clients.cell1op, clients.cell1, clients.cell2op, clients.cell2, clients.tel, clients.email, clients.adress, clients.number, clients.adress2, clients.cep, clients.district, clients.city, clients.state, clients.contry, service_order.* FROM service_order INNER JOIN clients ON clients.id=service_order.idCli WHERE service_order.id={id}"""
                print('SQL loadOS: ', sql)
                result = banco.queryDB(sql)
                print('Resultado: ', result)
                self.sorder.leName.setText(result[0][0])
                self.sorder.dtBirth.setDate(QtCore.QDate.fromString(result[0][1], 'yyyy-MM-dd'))
                if result[0][2] == 'M':
                    self.sorder.rbM.setChecked(True)
                else:
                    self.sorder.rbF.setChecked(True)
                self.sorder.leCpfCnpj.setText(result[0][3])
                self.sorder.leRgIe.setText(result[0][4])
                self.sorder.cbCell1.setCurrentText(result[0][5])
                self.sorder.leCell1.setText(result[0][6])
                self.sorder.cbCell2.setCurrentText(result[0][7])
                self.sorder.leCell2.setText(result[0][8])
                self.sorder.leTel.setText(result[0][9])
                self.sorder.leEmail.setText(result[0][10])
                self.sorder.leAdress.setText(result[0][11])
                self.sorder.leNumber.setText(result[0][12])
                self.sorder.leAdress2.setText(result[0][13])
                self.sorder.leCep.setText(result[0][14])
                self.sorder.leDistrict.setText(result[0][15])
                self.sorder.leCity.setText(result[0][16])
                self.sorder.leState.setText(result[0][17])
                self.sorder.leContry.setText(result[0][18])

                self.sorder.leOs.setEnabled(True)
                self.sorder.leOs.setText(str(result[0][19]))
                self.sorder.leCodCli.setEnabled(True)
                self.sorder.leCodCli.setText(str(result[0][20]))
                self.sorder.dtEntryDate.setEnabled(True)
                self.sorder.dtEntryDate.setDateTime(QtCore.QDateTime.fromString(result[0][21], 'yyyy-MM-dd hh:mm:ss'))
                self.sorder.dtAltDate.setEnabled(True)
                self.sorder.dtAltDate.setDateTime(QtCore.QDateTime.fromString(result[0][22], 'yyyy-MM-dd hh:mm:ss'))
                if result[0][23]:
                    self.sorder.dtOutDate.setEnabled(True)
                    self.sorder.dtOutDate.setDateTime(QtCore.QDateTime.fromString(result[0][23], 'yyyy-MM-dd hh:mm:ss'))
                self.sorder.cbType.setCurrentText(result[0][25])
                self.sorder.cbBrand.setCurrentText(result[0][26])
                self.sorder.leModel.setText(result[0][27])
                self.sorder.leColor.setText(result[0][28])
                self.sorder.leNs.setText(result[0][29])
                self.sorder.leBarCode.setText(result[0][30])
                self.sorder.leImei1.setText(result[0][31])
                self.sorder.leImei2.setText(result[0][32])
                self.sorder.leAcessories.setText(result[0][33])
                self.sorder.leDeviceStatus.setText(result[0][34])
                self.sorder.leDefect.setText(result[0][35])
                self.sorder.teObs1.setText(result[0][36])
                self.sorder.leDefectsFound.setText(result[0][37])
                self.sorder.leServiceDone.setText(result[0][38])
                tpartDescription = result[0][39]
                tpartAmount = result[0][40]
                tpartValue = result[0][41]
                tpartSubTotal = result[0][42]
                self.sorder.lePartsValue.setText(result[0][43])
                self.sorder.leServiceValue.setText(result[0][44])
                self.sorder.leTotalValue.setText(result[0][45])
                self.sorder.leObs2.setText(result[0][46])
                self.sorder.lbStatus2.setText(result[0][47])
            else:
                sql = f"""SELECT name, birthFun, sex, cpfcnpj, rgie, cell1op, cell1, cell2op, cell2, tel, email, adress, number, adress2, cep, district, city, state, contry FROM clients WHERE id={idC}"""
                print('SQL loadOS: ', sql)
                result = banco.queryDB(sql)
                print('Resultado: ', result)
                self.sorder.leCodCli.setText(str(idC))
                self.sorder.leName.setText(result[0][0])
                self.sorder.dtBirth.setDate(QtCore.QDate.fromString(result[0][1], 'yyyy-MM-dd'))
                if result[0][2] == 'M':
                    self.sorder.rbM.setChecked(True)
                else:
                    self.sorder.rbF.setChecked(True)
                self.sorder.leCpfCnpj.setText(result[0][3])
                self.sorder.leRgIe.setText(result[0][4])
                self.sorder.cbCell1.setCurrentText(result[0][5])
                self.sorder.leCell1.setText(result[0][6])
                self.sorder.cbCell2.setCurrentText(result[0][7])
                self.sorder.leCell2.setText(result[0][8])
                self.sorder.leTel.setText(result[0][9])
                self.sorder.leEmail.setText(result[0][10])
                self.sorder.leAdress.setText(result[0][11])
                self.sorder.leNumber.setText(result[0][12])
                self.sorder.leAdress2.setText(result[0][13])
                self.sorder.leCep.setText(result[0][14])
                self.sorder.leDistrict.setText(result[0][15])
                self.sorder.leCity.setText(result[0][16])
                self.sorder.leState.setText(result[0][17])
                self.sorder.leContry.setText(result[0][18])

        def saveOs():
            banco = Database('database.db')
            try:
                print('Salvando OS...')
                idCli = int(self.sorder.leCodCli.text())
                type = self.sorder.cbType.currentText()
                assert type != '', 'Selecione um tipo de aparelho!'
                brand = self.sorder.cbBrand.currentText()
                assert brand != '', 'Selecione uma Marca!'
                model = self.sorder.leModel.text()
                color = self.sorder.leColor.text()
                assert color != '', 'Selecione uma cor!'
                ns = self.sorder.leNs.text()
                br = self.sorder.leBarCode.text()
                imei1 = self.sorder.leImei1.text()
                imei2 = self.sorder.leImei2.text()
                acessories = self.sorder.leAcessories.text()
                deviceStatus = self.sorder.leDeviceStatus.text()
                defect = self.sorder.leDefect.text()
                assert defect != '', 'Descreva o defeito do aparelho!'
                obs1 = self.sorder.teObs1.toPlainText()
                defectFound = self.sorder.leDefectsFound.text()
                serviceDone = self.sorder.leServiceDone.text()
                partsValue = self.sorder.lePartsValue.text()
                serviceValue = self.sorder.leServiceValue.text()
                total = self.sorder.leTotalValue.text()
                obs2 = self.sorder.leObs2.text()
                status = self.sorder.lbStatus2.text()
            except AssertionError as e:
                msg = QMessageBox()
                msg.setWindowTitle('Falha ao salvar.')
                print(e.args)
                msg.setText(e.args[0])
                msg.exec_()

            if self.sorder.leOs.text():
                id = int(self.sorder.leOs.text())
                sql = f"""UPDATE service_order SET altDate='{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}', lastAlter={self.userId},
                deviceType='{type}', brand='{brand}', model='{model}', color='{color}', ns='{ns}', barCode='{br}', imei1='{imei1}', imei2='{imei2}',
                acessories='{acessories}', deviceStatus='{deviceStatus}', defect='{defect}', obs1='{obs1}', defectFound='{defectFound}', serviceDone='{serviceDone}',
                partTotalValue='{partsValue}', serviceValue='{serviceValue}', total='{total}', obs2='{obs2}', status='{status}' WHERE id={id}"""
                banco.queryDB(sql)
                loadOs(id)
            else:
                sql = f"""INSERT INTO service_order (idCli, entryDate, altDate, lastAlter,
                deviceType, brand, model, color, ns, barCode, imei1, imei2,
                acessories, deviceStatus, defect, obs1, defectFound, serviceDone,
                partTotalValue, serviceValue, total, obs2, status) VALUES ({idCli},
                datetime('now', 'localtime'), datetime('now', 'localtime'), {self.userId}, '{type}',
                '{brand}', '{model}', '{color}', '{ns}', '{br}', '{imei1}', '{imei2}',
                '{acessories}', '{deviceStatus}', '{defect}', '{obs1}', '{defectFound}',
                '{serviceDone}', '{partsValue}', '{serviceValue}', '{total}', '{obs2}', '{status}')"""
                print('SQL saveCli: ', sql)
                lrid = banco.queryDB(sql)
                self.openSO(lrid)

        print('Abrindo SO edit')
        self.SOrder = QDialog()
        self.sorder = Ui_SOrderEdit()
        self.sorder.setupUi(self.SOrder)
        self.sorder.pbSave.clicked.connect(saveOs)
        self.sorder.pbSearch.clicked.connect(self.sorder.pbExit.click)
        self.sorder.pbSearch.clicked.connect(lambda: self.openCliEdit(int(self.sorder.leCodCli.text())))
        self.sorder.rbAnalysis.clicked.connect(lambda: self.sorder.lbStatus2.setText('Em análise'))
        self.sorder.rbBudget.clicked.connect(lambda: self.sorder.lbStatus2.setText('Com orçamento'))
        self.sorder.rbApproved.clicked.connect(lambda: self.sorder.lbStatus2.setText('Aprovado'))
        self.sorder.rbRefused.clicked.connect(lambda: self.sorder.lbStatus2.setText('Recusado'))
        self.sorder.rbFixed.clicked.connect(lambda: self.sorder.lbStatus2.setText('Cosertado'))
        self.sorder.rbDelivery.clicked.connect(lambda: self.sorder.lbStatus2.setText('Devolver'))
        self.SOrder.show()
        loadOs(id)
    # End openSO

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = QDialog()
    w = App()
    w.setupUi(Login)
    QtCore.QObject.connect(w.buttonBox, QtCore.SIGNAL("accepted()"), w.loginCheck)
    Login.show()
    sys.exit(app.exec_())
