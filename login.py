# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui',
# licensing of 'login.ui' applies.
#
# Created: Sun Dec  9 17:50:04 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(193, 264)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("IMG/logoblack.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblogo = QtWidgets.QLabel(Login)
        self.lblogo.setMaximumSize(QtCore.QSize(130, 130))
        self.lblogo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblogo.setAutoFillBackground(False)
        self.lblogo.setText("")
        self.lblogo.setPixmap(QtGui.QPixmap("IMG/logoblack.png"))
        self.lblogo.setScaledContents(True)
        self.lblogo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblogo.setObjectName("lblogo")
        self.horizontalLayout_3.addWidget(self.lblogo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbuser = QtWidgets.QLabel(Login)
        self.lbuser.setMinimumSize(QtCore.QSize(0, 0))
        self.lbuser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lbuser.setScaledContents(True)
        self.lbuser.setOpenExternalLinks(False)
        self.lbuser.setObjectName("lbuser")
        self.horizontalLayout.addWidget(self.lbuser)
        self.leuser = QtWidgets.QLineEdit(Login)
        self.leuser.setObjectName("leuser")
        self.horizontalLayout.addWidget(self.leuser)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbpass = QtWidgets.QLabel(Login)
        self.lbpass.setObjectName("lbpass")
        self.horizontalLayout_2.addWidget(self.lbpass)
        self.lepass = QtWidgets.QLineEdit(Login)
        self.lepass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lepass.setObjectName("lepass")
        self.horizontalLayout_2.addWidget(self.lepass)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Login)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Login)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Login.reject)
        QtCore.QMetaObject.connectSlotsByName(Login)
        Login.setTabOrder(self.leuser, self.lepass)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtWidgets.QApplication.translate("Login", "Login", None, -1))
        self.lbuser.setText(QtWidgets.QApplication.translate("Login", "Usuário:", None, -1))
        self.lbpass.setText(QtWidgets.QApplication.translate("Login", "Senha:", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

