import sys, os
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QDialog
from PySide2 import QtCore
from database import Database
from login import Ui_Login
from home import Ui_Home
from clients import Ui_ClientEdit
from sorder import Ui_SOrderEdit


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
        print('Abrindo Cli edit')
        self.CliEdit = QDialog()
        self.cliedit = Ui_ClientEdit()
        self.cliedit.setupUi(self.CliEdit)
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
