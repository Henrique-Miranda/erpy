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
        try:
            if len(data) == 11 and data.isnumeric():
                data = '{}.{}.{}-{}'.format(data[0:3], data[3:6], data[6:9], data[9:])
        except:
            pass
        banco = Database('database.db')
        if local == 'Cliente':
            sql = f"SELECT * FROM clients WHERE name LIKE '{data}%' OR cpfcnpj LIKE '{data}%'"
        if local == 'Ordem de Serviço':
            sql = f"SELECT * FROM service_order WHERE id LIKE '{data}%' OR brand LIKE '{data}%'"

        resultado = banco.queryDB(sql)
        print('sql: ', sql)
        print(resultado)
        self.home.tableWidget.setRowCount(len(resultado))
        self.home.tableWidget.setColumnCount(12)
        self.home.tableWidget.setHorizontalHeaderLabels(['Código', 'Nome', 'Nascimento', 'Sexo', 'CPF/CNPJ', 'RG/IE', 'Operadora 1', 'Celular 1',
        'Operadora 2', 'Celular 2', 'Telefone 3', 'E-Mail'])

        for column, item in enumerate(resultado):
            self.home.tableWidget.setItem(column, 0, QTableWidgetItem(str(item[0])))
            self.home.tableWidget.setItem(column, 1, QTableWidgetItem(item[5]))
            self.home.tableWidget.setItem(column, 2, QTableWidgetItem(item[6]))
            self.home.tableWidget.setItem(column, 3, QTableWidgetItem(item[7]))
            self.home.tableWidget.setItem(column, 4, QTableWidgetItem(item[8]))
            self.home.tableWidget.setItem(column, 5, QTableWidgetItem(item[9]))
            self.home.tableWidget.setItem(column, 6, QTableWidgetItem(item[10]))
            self.home.tableWidget.setItem(column, 7, QTableWidgetItem(item[11]))
            self.home.tableWidget.setItem(column, 8, QTableWidgetItem(item[12]))
            self.home.tableWidget.setItem(column, 9, QTableWidgetItem(item[13]))
            self.home.tableWidget.setItem(column, 10, QTableWidgetItem(item[14]))
            self.home.tableWidget.setItem(column, 11, QTableWidgetItem(item[15]))
            self.home.tableWidget.setItem(column, 12, QTableWidgetItem(item[16]))
        self.home.tableWidget.itemDoubleClicked.connect(lambda: self.openCliEdit(int(resultado[self.home.tableWidget.currentRow()][0])))

    def openHome(self):
        print('Abrindo Home')
        self.Home = QMainWindow()
        self.home = Ui_Home()
        self.home.setupUi(self.Home)
        self.home.pbClient.clicked.connect(self.openCliEdit)
        self.home.pbSo.clicked.connect(lambda: self.openSO(1))
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
            self.cliedit.dateTimeCad.setDateTime(QtCore.QDateTime.fromString(resultado[0][1], ))
            self.cliedit.dateTimeAlt.setEnabled(True)
            self.cliedit.dateTimeAlt.setDateTime(QtCore.QDateTime.fromString(resultado[0][2], ))
            if resultado[0][3] == 'PF':
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
            if resultado[0][4] and not self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(True)
            elif not resultado[0][4] and self.cliedit.checkBox.checkState():
                self.cliedit.checkBox.setChecked(False)
            self.cliedit.leName.setText(resultado[0][5])
            self.cliedit.deBirthFun.setDate(QtCore.QDate.fromString(resultado[0][6], ))
            if resultado[0][7] == 'F':
                self.cliedit.rbF.setChecked(True)
            else:
                self.cliedit.rbM.setChecked(True)
            self.cliedit.leCpfCnpj.setText(resultado[0][8])
            self.cliedit.leRgIe.setText(resultado[0][9])
            self.cliedit.cbCell1.setCurrentText(resultado[0][10])
            self.cliedit.leCell1.setText(resultado[0][11])
            self.cliedit.cbCell2.setCurrentText(resultado[0][12])
            self.cliedit.leCell2.setText(resultado[0][13])
            self.cliedit.leTel.setText(resultado[0][14])
            self.cliedit.leMail.setText(resultado[0][15])
            self.cliedit.leCep.setText(resultado[0][16])
            self.cliedit.leStreet.setText(resultado[0][17])
            self.cliedit.leNumber.setText(resultado[0][18])
            self.cliedit.leComp.setText(resultado[0][19])
            self.cliedit.leDistrict.setText(resultado[0][20])
            self.cliedit.leCity.setText(resultado[0][21])
            self.cliedit.leState.setText(resultado[0][22])
            self.cliedit.leContry.setText(resultado[0][23])
            self.cliedit.leCodCli.setEnabled(True)
            self.cliedit.pbDelete.setEnabled(True)
            self.cliedit.pbNew.setEnabled(True)

        def delCli(id):
            banco = Database('database.db')
            sql = f"""DELETE FROM clients WHERE id = '{id}'"""
            banco.queryDB(sql)
            msg = QMessageBox()
            msg.setWindowTitle('Cliente foi excluído.')
            msg.setText('Este cliente foi deletado com sucesso!')
            msg.exec_()
            self.cliedit.pbExit.click()

        def saveCli():
            try:
                banco = Database('database.db')
                dic = {}
                name = self.cliedit.leName.text().title()
                assert name != '', 'Digite o nome do cliente!'
                birth = self.cliedit.deBirthFun.date().toString('yyyy-MM-dd')
                print(birth)
                idade = int(QtCore.QDate.currentDate().toString('yyyy-MM-dd')[0:4]) - int(birth[0:4])
                if self.cliedit.buttonGroup.checkedButton() == 'PF':
                    assert idade >= 18, 'Este cliente tem menos de 18 anos!'
                cpfcnpj = self.cliedit.leCpfCnpj.text().strip()
                assert cpfcnpjv.validate(cpfcnpj) == True, 'CPF/CNPJ inválido!'
                rgie = self.cliedit.leRgIe.text().strip()
                if rgie: dic['rgie'] = rgie
                email = self.cliedit.leMail.text().strip()
                if self.cliedit.leCodCli.text():
                    sql = f"""UPDATE clients SET altdate = '{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}', regtype = '{self.cliedit.buttonGroup.checkedButton().text()}',
                    blocked = '{int(self.cliedit.checkBox.isChecked())}',
                    name = '{name}', birthFun = '{birth}', sex = '{self.cliedit.buttonGroup_2.checkedButton().text()}', rgie = '{rgie}',
                    cell1op = '{self.cliedit.cbCell1.currentText()}', cell1 = '{self.cliedit.leCell1.text()}', cell2op = '{self.cliedit.cbCell2.currentText()}',
                    cell2 = '{self.cliedit.leCell2.text()}', tel = '{self.cliedit.leTel.text()}', email = '{email}', cep = '{self.cliedit.leCep.text()}',
                    adress = '{self.cliedit.leStreet.text()}', number = '{self.cliedit.leNumber.text()}', adress2 = '{self.cliedit.leComp.text()}',
                    district = '{self.cliedit.leDistrict.text()}', city = '{self.cliedit.leCity.text()}', state = '{self.cliedit.leState.text()}', contry = '{self.cliedit.leContry.text()}' WHERE id = '{self.cliedit.leCodCli.text()}'"""
                else:
                    sql = f"""INSERT INTO clients (regdate, altdate, regtype, blocked,
                    name, birthFun, sex, cpfcnpj, rgie, cell1op, cell1, cell2op, cell2, tel, email, cep,
                    adress, number, adress2, district, city, state, contry)
                    VALUES ('{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}',
                    '{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}',
                    '{self.cliedit.buttonGroup.checkedButton().text()}',
                    '{int(self.cliedit.checkBox.isChecked())}', '{name}', '{birth}',
                    '{self.cliedit.buttonGroup_2.checkedButton().text()}',
                    '{cpfcnpj}', '{rgie}', '{self.cliedit.cbCell1.currentText()}',
                    '{self.cliedit.leCell1.text()}', '{self.cliedit.cbCell2.currentText() }', '{self.cliedit.leCell2.text()}',
                    '{self.cliedit.leTel.text()}', '{email}',
                    '{self.cliedit.leCep.text()}', '{self.cliedit.leStreet.text()}',
                    '{self.cliedit.leNumber.text()}', '{self.cliedit.leComp.text()}',
                    '{self.cliedit.leDistrict.text()}', '{self.cliedit.leCity.text()}',
                    '{self.cliedit.leState.text()}', '{self.cliedit.leContry.text()}')"""
                print('SQL: ', sql)
                banco.queryDB(sql)
                loadCli(self.cliedit.leCpfCnpj.text().strip(), "cpfcnpj")

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
        if data != 0:
            loadCli(data)

    def openSO(self, id = 0):
        def saveOs():
            print('Salvando OS...')
            idCli = self.sorder.leCodCli.text()
            dtEntry = QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
            type = self.sorder.cbType.currentText()
            brand = self.sorder.cbBrand.currentText()
            model = self.sorder.leModel.text()
            color = self.sorder.leColor.text()
            ns = self.sorder.leNs.text()
            br = self.sorder.leBarCode.text()
            imei1 = self.sorder.leImei1.text()
            imei2 = self.sorder.leImei2.text()
            acessories = self.sorder.leAcessories.text()
            deviceStatus = self.sorder.leDeviceStatus.text()
            defect = self.sorder.leDefect.text()
            obs1 = self.sorder.teObs1.toPlainText()
            defectFound = self.sorder.leDefectsFound.text()
            serviceDone = self.sorder.leServiceDone.text()
            partsValue = self.sorder.lePartsValue.text()
            serviceValue = self.sorder.leServiceValue.text()
            total = self.sorder.leTotalValue.text()
            obs2 = self.sorder.leObs2.text()
            status = self.sorder.lbStatus2.text()

            sql = f"""INSERT INTO service_order (idCli, entryDate, deviceType, brand, model, color, ns, barCode, imei1, imei2,
            acessories, deviceStatus, defect, obs1, defectFound, serviceDone,
            partTotalValue, serviceValue, total, obs2, status) VALUES ({int(idCli)}, datetime('now',
            'localtime'),  '{type}', '{brand}', '{model}', '{color}', '{ns}', '{br}', '{imei1}', '{imei2}',
            '{acessories}', '{deviceStatus}', '{defect}', '{obs1}', '{defectFound}', '{serviceDone}', '{partsValue}', '{serviceValue}', '{total}', '{obs2}', '{status}')"""
            print(sql)
            banco = Database('database.db')
            banco.queryDB(sql)



        def loadOs():
            pass
        print('Abrindo SO edit')
        self.SOrder = QDialog()
        self.sorder = Ui_SOrderEdit()
        self.sorder.setupUi(self.SOrder)
        self.sorder.pbSave.clicked.connect(saveOs)
        self.sorder.pbSearch.clicked.connect(lambda: self.openCliEdit(1))
        self.sorder.pbSearch.clicked.connect(self.sorder.pbExit.click)
        self.sorder.rbAnalysis.clicked.connect(lambda: self.sorder.lbStatus2.setText('Em análise'))
        self.sorder.rbBudget.clicked.connect(lambda: self.sorder.lbStatus2.setText('Com orçamento'))
        self.sorder.rbApproved.clicked.connect(lambda: self.sorder.lbStatus2.setText('Aprovado'))
        self.sorder.rbRefused.clicked.connect(lambda: self.sorder.lbStatus2.setText('Recusado'))
        self.sorder.rbFixed.clicked.connect(lambda: self.sorder.lbStatus2.setText('Cosertado'))
        self.sorder.rbDelivery.clicked.connect(lambda: self.sorder.lbStatus2.setText('Devolver'))
        self.sorder.leCodCli.setText(str(id))
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
