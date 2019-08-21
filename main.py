from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog, QTableWidgetItem, QHeaderView

from database import Database
from viacep import ViaCEP
from pycpfcnpj import cpfcnpj as cpfcnpjv
import sys, os, sqlite3, socket

class App(object):
    def __init__(self):
        self.userId = None
        self.userName = None
        self.fullName = None
        self.hostName = None
        self.userIP = None
        self.logged = False
        self.dbConn = Database('database.db')
        if 'database.db' not in os.listdir():
            self.dbConn.createDB()
            print('Criado')

        self.loginW = self.loadUI('login.ui')
        self.loginW.buttonBox.accepted.connect(self.loginCheck)
        self.loginW.show()

    def loadUI(self, fileName):
        file = QtCore.QFile(f'ui_forms/{fileName}')
        file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        return loader.load(file)


    # Start login
    def loginCheck(self):
        user = self.loginW.leuser.text()
        passwd = self.loginW.lepass.text()
        sql = f"SELECT * FROM staff WHERE login='{user}' AND passwd='{passwd}'"
        result = self.dbConn.queryDB(sql)
        if result:
            self.userId = result[0][0]
            self.fullName = result[0][1]
            self.user = result[0][2]
            self.hostName = socket.gethostname()
            self.userIP = socket.gethostbyname(self.hostName)
            self.logged = True
            self.openHome()
            self.loginW.hide()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Falha no Login')
            msg.setText('Dados incorretos, tente novamente.')
            msg.exec_()
    # End login
    # Start openHome
    def openHome(self):
        self.homeW = self.loadUI('home.ui')
        self.homeW.pbClient.clicked.connect(self.openCliEdit)
        self.homeW.actionSair.triggered.connect(app.exit)
        self.homeW.actionClient.triggered.connect(self.openCliEdit)
        self.homeW.leSearch.returnPressed.connect(lambda: self.loadSearch(self.homeW.leSearch.text(), self.homeW.cbSearch.currentText()))
        self.homeW.pbSo.clicked.connect(self.openSO)
        self.homeW.pbSearch.clicked.connect(lambda: self.loadSearch(self.homeW.leSearch.text(), self.homeW.cbSearch.currentText()))
        self.homeW.tableWidget.setColumnCount(12)
        self.homeW.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome',
        'Nascimento', 'Sexo', 'CPF/CNPJ', 'RG/IE', 'Operadora 1', 'Celular 1',
        'Operadora 2', 'Celular 2', 'Telefone', 'E-Mail'])
        self.homeW.statusbar.showMessage(f'Usuário: {self.fullName}          IP: {self.userIP}          Hostname: {self.hostName}')
        self.homeW.show()
    # End openHome
    # Start loadSearch
    def loadSearch(self, data, local):
        if len(data) == 11 and cpfcnpjv.validate(data):
            data = f'{data[0:3]}.{data[3:6]}.{data[6:9]}-{data[9:]}'

        if local == 'Cliente':
            sql = f"SELECT * FROM clients WHERE name LIKE '{data}%' OR cpfcnpj LIKE '{data}%' ORDER BY id DESC LIMIT 100"
            result = self.dbConn.queryDB(sql)
            self.homeW.tableWidget.setRowCount(len(result))
            self.homeW.tableWidget.setColumnCount(12)
            self.homeW.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome',
            'Nascimento', 'Sexo', 'CPF/CNPJ', 'RG/IE', 'Operadora 1', 'Celular 1',
            'Operadora 2', 'Celular 2', 'Telefone', 'E-Mail'])

            for row, item in enumerate(result):
                self.homeW.tableWidget.setItem(row, 0, QTableWidgetItem(str(item[0])))
                self.homeW.tableWidget.setItem(row, 1, QTableWidgetItem(item[6]))
                self.homeW.tableWidget.setItem(row, 2, QTableWidgetItem(item[7]))
                self.homeW.tableWidget.setItem(row, 3, QTableWidgetItem(item[8]))
                self.homeW.tableWidget.setItem(row, 4, QTableWidgetItem(item[9]))
                self.homeW.tableWidget.setItem(row, 5, QTableWidgetItem(item[10]))
                self.homeW.tableWidget.setItem(row, 6, QTableWidgetItem(item[11]))
                self.homeW.tableWidget.setItem(row, 7, QTableWidgetItem(item[12]))
                self.homeW.tableWidget.setItem(row, 8, QTableWidgetItem(item[13]))
                self.homeW.tableWidget.setItem(row, 9, QTableWidgetItem(item[14]))
                self.homeW.tableWidget.setItem(row, 10, QTableWidgetItem(item[15]))
                self.homeW.tableWidget.setItem(row, 11, QTableWidgetItem(item[16]))
                self.homeW.tableWidget.setItem(row, 12, QTableWidgetItem(item[17]))

        if local == 'Ordem de Serviço':
            try:
                data = int(data)
                sql = f"""SELECT serviceOrders.id, clients.name, clients.cpfcnpj, \
                    serviceOrders.deviceType, serviceOrders.brand, serviceOrders.model, \
                    serviceOrders.color, clients.phone1op, clients.phone1, clients.phone1op, \
                    clients.phone2, clients.phone1 FROM serviceOrders INNER JOIN clients ON \
                    clients.id=serviceOrders.idCli WHERE serviceOrders.id={data}"""
            except:
                sql = f"""SELECT serviceOrders.id, clients.name, serviceOrders.entryDate, \
                    clients.cpfcnpj, serviceOrders.deviceType, serviceOrders.brand, serviceOrders.model, \
                    serviceOrders.color, clients.phone1op, clients.phone1, clients.phone1op, \
                    clients.phone2, clients.phone1 FROM serviceOrders INNER JOIN clients ON \
                    clients.id=serviceOrders.idCli WHERE clients.cpfcnpj LIKE '{data}%' OR \
                    clients.name LIKE '{data}%' OR serviceOrders.brand LIKE '{data}%' OR \
                    serviceOrders.model LIKE '{data}%' ORDER BY regdate DESC LIMIT 100"""

            result = self.dbConn.queryDB(sql)
            self.homeW.tableWidget.setRowCount(len(result))
            self.homeW.tableWidget.setColumnCount(13)
            self.homeW.tableWidget.setHorizontalHeaderLabels(['OS', 'Cliente',
            'Data de entrada', 'CPF/CNPJ', 'Aparelho', 'Marca', 'Modelo', 'Cor',
            'Operadora 1', 'Celular 1', 'Operadora 2', 'Celular 2', 'Telefone'])

            for row, item in enumerate(result):
                self.homeW.tableWidget.setItem(row, 0, QTableWidgetItem(str(item[0])))
                self.homeW.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
                self.homeW.tableWidget.setItem(row, 2, QTableWidgetItem(item[2]))
                self.homeW.tableWidget.setItem(row, 3, QTableWidgetItem(item[3]))
                self.homeW.tableWidget.setItem(row, 4, QTableWidgetItem(item[4]))
                self.homeW.tableWidget.setItem(row, 5, QTableWidgetItem(item[5]))
                self.homeW.tableWidget.setItem(row, 6, QTableWidgetItem(item[6]))
                self.homeW.tableWidget.setItem(row, 7, QTableWidgetItem(item[7]))
                self.homeW.tableWidget.setItem(row, 8, QTableWidgetItem(item[8]))
                self.homeW.tableWidget.setItem(row, 9, QTableWidgetItem(item[9]))
                self.homeW.tableWidget.setItem(row, 10, QTableWidgetItem(item[10]))
                self.homeW.tableWidget.setItem(row, 11, QTableWidgetItem(item[11]))
                self.homeW.tableWidget.setItem(row, 12, QTableWidgetItem(item[12]))
        try:
            self.homeW.tableWidget.itemDoubleClicked.disconnect()
        except:
            pass
        if local == 'Ordem de Serviço':
            self.homeW.tableWidget.itemDoubleClicked.connect(lambda: self.openSO(int(result[self.homeW.tableWidget.currentRow()][0])))
        if local == 'Cliente':
            self.homeW.tableWidget.itemDoubleClicked.connect(lambda: self.openCliEdit(int(result[self.homeW.tableWidget.currentRow()][0])))
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

            sql = f'SELECT * FROM clients WHERE id={data}'
            print('SQL loadcli:', sql)
            result = self.dbConn.queryDB(sql)
            print('Resultado loadcli: ', result)
            self.cliedit.leCodCli.setText(str(result[0][0]))
            self.cliedit.dateTimeCad.setEnabled(True)
            self.cliedit.dateTimeCad.setDateTime(QtCore.QDateTime.fromString(result[0][1], 'dd/MM/yyyy hh:mm:ss'))
            self.cliedit.dateTimeAlt.setEnabled(True)
            self.cliedit.dateTimeAlt.setDateTime(QtCore.QDateTime.fromString(result[0][2], 'dd/MM/yyyy hh:mm:ss'))
            self.cliedit.buttonGroup.button(result[0][4]).setChecked(True)
            if self.cliedit.buttonGroup.button(result[0][4]).text() == 'PF':
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
            self.cliedit.leName.setText(result[0][6])
            self.cliedit.deBirthFun.setDate(QtCore.QDate.fromString(result[0][7], 'dd/MM/yyyy'))
            self.cliedit.buttonGroup_2.button(result[0][8]).setChecked(True)
            self.cliedit.leCpfCnpj.setText(result[0][9])
            self.cliedit.leRgIe.setText(result[0][10])
            self.cliedit.cbPhone1.setCurrentText(result[0][11])
            self.cliedit.lePhone1.setText(result[0][12])
            self.cliedit.cbPhone2.setCurrentText(result[0][13])
            self.cliedit.lePhone2.setText(result[0][14])
            self.cliedit.lePhone3.setText(result[0][15])
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

            sql = f"DELETE FROM clients WHERE id = '{id}'"
            try:
                self.dbConn.queryDB(sql)
                msg = QMessageBox()
                msg.setWindowTitle('Cliente foi excluído.')
                msg.setText('Este cliente foi deletado com sucesso!')
                msg.exec_()
                self.cliedit.pbExit.click()
            except:
                pass

        def saveCli():
            try:
                name = self.cliedit.leName.text().title()
                assert name, 'Digite o nome do cliente!'
                birth = self.cliedit.deBirthFun.date().toString('dd/MM/yyyy')
                idade = int(QtCore.QDate.currentDate().toString('dd/MM/yyyy')[6:10]) - int(birth[6:10])
                if self.cliedit.buttonGroup.checkedButton().text() == 'PF':
                    assert idade >= 18, 'Este cliente tem menos de 18 anos!'
                cpfcnpj = self.cliedit.leCpfCnpj.text().strip()
                assert cpfcnpjv.validate(cpfcnpj), 'CPF/CNPJ inválido!'
                rgie = self.cliedit.leRgIe.text().strip()
                email = self.cliedit.leMail.text().strip()
                if self.cliedit.leCodCli.text():
                    sql = f"""UPDATE clients SET altdate = '{QtCore.QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")}', lastAlter={self.userId}, blocked = '{int(self.cliedit.checkBox.isChecked())}',
                    name = '{name}', birthFun = '{birth}', sex = {self.cliedit.buttonGroup_2.checkedId()}, cpfcnpj='{cpfcnpj}', rgie = NULLIF('{rgie}', ''),
                    phone1op = '{self.cliedit.cbPhone1.currentText()}', phone1 = '{self.cliedit.lePhone1.text()}', phone2op = '{self.cliedit.cbPhone2.currentText()}',
                    phone2 = '{self.cliedit.lePhone2.text()}', phone3 = '{self.cliedit.lePhone3.text()}', email = NULLIF('{email}', ''), cep = '{self.cliedit.leCep.text()}',
                    adress = '{self.cliedit.leStreet.text()}', number = '{self.cliedit.leNumber.text()}', adress2 = '{self.cliedit.leComp.text()}',
                    district = '{self.cliedit.leDistrict.text()}', city = '{self.cliedit.leCity.text()}', state = '{self.cliedit.leState.text()}', contry = '{self.cliedit.leContry.text()}' WHERE id={int(self.cliedit.leCodCli.text())}"""
                    self.dbConn.queryDB(sql)
                    loadCli(int(self.cliedit.leCodCli.text()))
                else:
                    sql = f"""INSERT INTO clients (regdate, altdate, lastAlter, regtype, blocked,
                    name, birthFun, sex, cpfcnpj, rgie, phone1op, phone1, phone2op, phone2, phone3, email, cep,
                    adress, number, adress2, district, city, state, contry)
                    VALUES ('{QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy hh:mm:ss')}',
                    '{QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy hh:mm:ss')}',
                    {self.userId}, {self.cliedit.buttonGroup.checkedId()},
                    '{int(self.cliedit.checkBox.isChecked())}', '{name}', '{birth}',
                    {self.cliedit.buttonGroup_2.checkedId()},
                    '{cpfcnpj}', NULLIF('{rgie}', ''), '{self.cliedit.cbPhone1.currentText()}',
                    '{self.cliedit.lePhone1.text()}', '{self.cliedit.cbPhone2.currentText() }', '{self.cliedit.lePhone2.text()}',
                    '{self.cliedit.lePhone3.text()}', NULLIF('{email}', ''),
                    '{self.cliedit.leCep.text()}', '{self.cliedit.leStreet.text()}',
                    '{self.cliedit.leNumber.text()}', '{self.cliedit.leComp.text()}',
                    '{self.cliedit.leDistrict.text()}', '{self.cliedit.leCity.text()}',
                    '{self.cliedit.leState.text()}', '{self.cliedit.leContry.text()}')"""
                    print('SQL SaveCli: ', sql)
                    lrid = self.dbConn.queryDB(sql)
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
        self.cliedit = self.loadUI('clients.ui')
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

            if widget == self.cliedit.lePhone1 or widget == self.cliedit.lePhone2:
                widget.setMaxLength(15)
                if self.cliedit.lePhone1.text() or self.cliedit.lePhone2.text():
                    widget.setInputMask(maskk)
                else:
                    widget.setInputMask('')

            if widget == self.cliedit.lePhone3:
                widget.setMaxLength(14)
                if self.cliedit.lePhone3.text():
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
        self.cliedit.lePhone1.textEdited.connect(lambda: mask(self.cliedit.lePhone1))
        self.cliedit.lePhone1.editingFinished.connect(lambda: mask(self.cliedit.lePhone1, '(00)00000-0000'))
        self.cliedit.lePhone2.textEdited.connect(lambda: mask(self.cliedit.lePhone2))
        self.cliedit.lePhone2.editingFinished.connect(lambda: mask(self.cliedit.lePhone2, '(00)00000-0000'))
        self.cliedit.lePhone3.textEdited.connect(lambda: mask(self.cliedit.lePhone3))
        self.cliedit.lePhone3.editingFinished.connect(lambda: mask(self.cliedit.lePhone3, '(00)0000-0000'))
        self.cliedit.leCep.textEdited.connect(lambda: mask(self.cliedit.leCep))
        self.cliedit.leCep.editingFinished.connect(lambda: mask(self.cliedit.leCep, '00000-000'))
        self.cliedit.setModal(True)
        self.cliedit.show()
        if data:
            loadCli(data)
    # End openCliEdit
    # Start openSO
    def openSO(self, id = 0, idC = 0):
        print("o IDC é: ", idC, type(idC))
        def loadOs(id):
            if not idC:
                sql = f"""SELECT clients.name, clients.birthFun, clients.sex, clients.cpfcnpj, clients.rgie, clients.phone1op, clients.phone1, clients.phone1op, clients.phone2, clients.phone3, clients.email, clients.adress, clients.number, clients.adress2, clients.cep, clients.district, clients.city, clients.state, clients.contry, serviceOrders.* FROM serviceOrders INNER JOIN clients ON clients.id=serviceOrders.idCli WHERE serviceOrders.id={id}"""
                print('SQL loadOS: ', sql)
                result = self.dbConn.queryDB(sql)
                print('Resultado: ', result)
                self.sorder.leName.setText(result[0][0])
                self.sorder.dtBirth.setDate(QtCore.QDate.fromString(result[0][1], 'dd/MM/yyyy'))
                self.sorder.buttonGroup.button(result[0][2]).setChecked(True)
                self.sorder.rbM.setEnabled(False)
                self.sorder.rbF.setEnabled(False)
                self.sorder.leCpfCnpj.setText(result[0][3])
                self.sorder.leRgIe.setText(result[0][4])
                self.sorder.cbPhone1.setCurrentText(result[0][5])
                self.sorder.cbPhone1.setDisabled(True)
                self.sorder.lePhone1.setText(result[0][6])
                self.sorder.cbPhone2.setCurrentText(result[0][7])
                self.sorder.cbPhone2.setDisabled(True)
                self.sorder.lePhone2.setText(result[0][8])
                self.sorder.lePhone3.setText(result[0][9])
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
                self.sorder.dtEntryDate.setDateTime(QtCore.QDateTime.fromString(result[0][21], 'dd/MM/yyyy hh:mm:ss'))
                self.sorder.dtAltDate.setEnabled(True)
                self.sorder.dtAltDate.setDateTime(QtCore.QDateTime.fromString(result[0][22], 'dd/MM/yyyy hh:mm:ss'))
                if result[0][23]:
                    self.sorder.dtOutDate.setEnabled(True)
                    self.sorder.dtOutDate.setDateTime(QtCore.QDateTime.fromString(result[0][23], 'dd/MM/yyyy hh:mm:ss'))
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
                self.sorder.leObs1.setText(result[0][36])
                self.sorder.leDefectsFound.setText(result[0][37])
                self.sorder.leServiceDone.setText(result[0][38])
                self.sorder.spServiceValue.setValue(result[0][39])
                self.sorder.leObs2.setText(result[0][40])
                self.sorder.lbStatus2.setText(result[0][41])
                self.sorder.cbStatus.setCurrentText(result[0][41])
                self.sorder.pbPrint.setEnabled(True)
                self.sorder.pbNewOs.setEnabled(True)
                if self.sorder.cbStatus.currentText() in ('Consertado', 'Orçamento reprovado', 'Sem peça de reposição', 'Defeito não encontrado'):
                    self.sorder.pbDelivery.setEnabled(True)
                else:
                    self.sorder.pbDelivery.setEnabled(False)
                if self.sorder.cbStatus.currentText() in ('Orçamento concluído', 'Orçamento aprovado', 'Consertado', 'Em execução do serviço', 'Aguardando peça de reposição'):
                    self.sorder.pbPrint2.setEnabled(True)
                else:
                    self.sorder.pbPrint2.setEnabled(False)
                if self.sorder.cbStatus.currentText() in ('Consertado', 'Equipamento devolvido'):
                    self.sorder.pbPrint3.setEnabled(True)
                else:
                    self.sorder.pbPrint3.setEnabled(False)
                result = self.dbConn.queryDB(f"""SELECT * FROM soProducts WHERE soId={id}""")
                print(result)
                defectFound = self.sorder.leDefectsFound.text()
                ptotal = 0
                if result:
                    self.sorder.twBudget.setRowCount(len(result))
                    self.sorder.twBudget.setColumnCount(4)
                    for row, item in enumerate(result):
                        self.sorder.twBudget.setItem(row, 0, QTableWidgetItem(item[1]))
                        self.sorder.twBudget.setItem(row, 1, QTableWidgetItem(str(item[2])))
                        self.sorder.twBudget.setItem(row, 2, QTableWidgetItem(str(item[3])))
                        self.sorder.twBudget.setItem(row, 3, QTableWidgetItem(str(item[2]*item[3])))
                        ptotal+=float(self.sorder.twBudget.item(row, 3).text())
                    self.sorder.spPartsValue.setValue(ptotal)
                self.sorder.spTotalValue.setValue(ptotal+self.sorder.spServiceValue.value())

            else:
                sql = f"""SELECT name, birthFun, sex, cpfcnpj, rgie, phone1op, phone1, phone1op, phone2, phone3, email, adress, number, adress2, cep, district, city, state, contry FROM clients WHERE id={idC}"""
                print('SQL loadOS: ', sql)
                result = self.dbConn.queryDB(sql)
                print('Resultado: ', result)
                self.sorder.leCodCli.setText(str(idC))
                self.sorder.leName.setText(result[0][0])
                self.sorder.dtBirth.setDate(QtCore.QDate.fromString(result[0][1], 'dd/MM/yyyy'))
                self.sorder.buttonGroup.button(result[0][2]).setChecked(True)
                self.sorder.rbM.setEnabled(False)
                self.sorder.rbF.setEnabled(False)
                self.sorder.leCpfCnpj.setText(result[0][3])
                self.sorder.leRgIe.setText(result[0][4])
                self.sorder.cbPhone1.setCurrentText(result[0][5])
                self.sorder.lePhone1.setText(result[0][6])
                self.sorder.cbPhone1.setDisabled(True)
                self.sorder.cbPhone2.setCurrentText(result[0][7])
                self.sorder.lePhone2.setText(result[0][8])
                self.sorder.cbPhone2.setDisabled(True)
                self.sorder.lePhone3.setText(result[0][9])
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
            try:
                print('Salvando OS...')
                idCli = int(self.sorder.leCodCli.text())
                type = self.sorder.cbType.currentText()
                assert type, 'Selecione um tipo de aparelho!'
                brand = self.sorder.cbBrand.currentText()
                assert brand, 'Selecione uma Marca!'
                model = self.sorder.leModel.text()
                color = self.sorder.leColor.text()
                assert color, 'Selecione uma cor!'
                ns = self.sorder.leNs.text()
                br = self.sorder.leBarCode.text()
                imei1 = self.sorder.leImei1.text()
                imei2 = self.sorder.leImei2.text()
                acessories = self.sorder.leAcessories.text()
                deviceStatus = self.sorder.leDeviceStatus.text()
                defect = self.sorder.leDefect.text()
                assert defect, 'Descreva o defeito do aparelho!'
                obs1 = self.sorder.leObs1.text()
                defectFound = self.sorder.leDefectsFound.text()
                serviceDone = self.sorder.leServiceDone.text()
                obs2 = self.sorder.leObs2.text()
                serviceValue = self.sorder.spServiceValue.value()
                status = self.sorder.cbStatus.currentText()
                if status in ('Orçamento aprovado', 'Consertado', 'Aguardando peça de reposição', 'Orçamento concluído', 'Equipamento devolvido consertado', 'Orçamento reprovado', 'Em execução do serviço'):
                    assert self.sorder.spTotalValue.value(), 'Antes disso insira um valor de serviço ou peça na aba orçamento.'

            except AssertionError as e:
                msg = QMessageBox()
                msg.setWindowTitle('Falha ao salvar.')
                print(e.args)
                msg.setText(e.args[0])
                msg.exec_()

            if self.sorder.leOs.text():
                id = int(self.sorder.leOs.text())
                sql = f"""UPDATE serviceOrders SET altDate='{QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy hh:mm:ss')}', lastAlter={self.userId},
                deviceType='{type}', brand='{brand}', model='{model}', color='{color}', ns='{ns}', barCode='{br}', imei1='{imei1}', imei2='{imei2}',
                acessories='{acessories}', deviceStatus='{deviceStatus}', defect='{defect}', obs1='{obs1}', defectFound='{defectFound}', serviceDone='{serviceDone}',
                serviceValue={serviceValue}, obs2='{obs2}', status='{status}' WHERE id={id}"""

                self.dbConn.queryDB(sql)
                rnumber = self.sorder.twBudget.rowCount()
                if rnumber:
                    sql = f"DELETE FROM soProducts WHERE soId={id}"
                    self.dbConn.queryDB(sql)
                    for row in range(rnumber):
                        desc = self.sorder.twBudget.item(row, 0).text()
                        amount = int(self.sorder.twBudget.item(row, 1).text())
                        value = float(self.sorder.twBudget.item(row, 2).text())
                        sql = f"INSERT INTO soProducts (soId, description, amount, value) VALUES ({id}, '{desc}', {amount}, {value})"
                        print('SQL', sql)
                        self.dbConn.queryDB(sql)
                if not rnumber and self.sorder.spPartsValue.value():
                    sql = f"DELETE FROM soProducts WHERE soId={id}"
                    self.dbConn.queryDB(sql)
                    self.sorder.spPartsValue.setValue(0.0)

                loadOs(id)
            else:
                sql = f"""INSERT INTO serviceOrders (idCli, entryDate, altDate, lastAlter,
                deviceType, brand, model, color, ns, barCode, imei1, imei2,
                acessories, deviceStatus, defect, obs1, defectFound, serviceDone,
                serviceValue, obs2, status) VALUES ({idCli},
                '{QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy hh:mm:ss')}', '{QtCore.QDateTime.currentDateTime().toString('dd/MM/yyyy hh:mm:ss')}', {self.userId}, '{type}',
                '{brand}', '{model}', '{color}', '{ns}', '{br}', '{imei1}', '{imei2}',
                '{acessories}', '{deviceStatus}', '{defect}', '{obs1}', '{defectFound}',
                '{serviceDone}', {serviceValue}, '{obs2}', '{status}')"""
                print('SQL saveCli: ', sql)
                lrid = self.dbConn.queryDB(sql)
                self.openSO(lrid)

        def printSo(id, osType):
            from exportPDF import makePDF
            makePDF(id, osType)
            PDF_PATH = f'{os.getcwd()}/OS_DIR/os{id}.pdf'
            try:
                import platform
                if platform.system() == 'Windows':
                    os.system(f'start {PDF_PATH}')
                elif platform.system() == 'Linux':
                    os.system(f'xdg-open {PDF_PATH}')
                else:
                    raise Exception('Seu sistema operacional não é suportado.')
            except:
                import webbrowser
                webbrowser.open(PDF_PATH)

        print('Abrindo SO edit')
        self.sorder = self.loadUI('sorder.ui')
        self.sorder.pbSave.clicked.connect(saveOs)
        self.sorder.pbSearch.clicked.connect(self.sorder.pbExit.click)
        self.sorder.pbSearch.clicked.connect(lambda: self.openCliEdit(int(self.sorder.leCodCli.text())))
        self.sorder.cbStatus.currentTextChanged.connect(lambda: self.sorder.lbStatus2.setText(self.sorder.cbStatus.currentText()))
        self.sorder.pbPrint.clicked.connect(lambda: printSo(id, 1))
        self.sorder.pbPrint2.clicked.connect(lambda: printSo(id, 2))
        self.sorder.pbPrint3.clicked.connect(lambda: printSo(id, 3))

        def addToTable():
            row = self.sorder.twBudget.rowCount()+1
            self.sorder.twBudget.setRowCount(row)
            desc = self.sorder.cbAddDesc.currentText()
            amount = self.sorder.spAddAmount.value()
            pvalue = self.sorder.spAddValue.value()
            svalue = amount * pvalue
            self.sorder.twBudget.setItem(row-1, 0, QTableWidgetItem(desc))
            self.sorder.twBudget.setItem(row-1, 1, QTableWidgetItem(str(amount)))
            self.sorder.twBudget.setItem(row-1, 2, QTableWidgetItem(str(pvalue)))
            self.sorder.twBudget.setItem(row-1, 3, QTableWidgetItem(str(svalue)))
        self.sorder.twBudget.itemClicked.connect(lambda: self.sorder.twBudget.removeRow(self.sorder.twBudget.currentRow()))
        self.sorder.pbAddPart.clicked.connect(addToTable)
        self.sorder.setModal(True)
        self.sorder.show()
        loadOs(id)
    # End openSO

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    w = App()
    sys.exit(app.exec_())
