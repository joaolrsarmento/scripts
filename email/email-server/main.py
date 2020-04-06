from controllers.emailScript import GmailAccount
from controllers.printScript import Printer
from constants.constants import ENABLE_LESS_SECURE_APPS_URL, EMAIL_RECEIVER, EMAIL_SENDER, PASSWORD_RECEIVER
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot
import sys
import os

class MainInterface(QDialog):
    def __init__(self, parent=None):
        super(MainInterface, self).__init__(parent)
        self.setWindowTitle('Servidor')
        self.setMinimumSize(320, 240)

        self.layout = QVBoxLayout()
        self.label1 = QLabel('Email do destinatário')
        self.emailReceiver = QLineEdit(EMAIL_RECEIVER)
        self.label2 = QLabel('Senha do destinatário')
        self.passwordReceiver = QLineEdit(PASSWORD_RECEIVER)
        self.passwordReceiver.setEchoMode(3)
        self.label3 = QLabel('Email do remetente')
        self.emailSender = QLineEdit(EMAIL_SENDER)

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.emailReceiver)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.passwordReceiver)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.emailSender)

        self.subLayout = QHBoxLayout()
        self.initButton = QPushButton('Iniciar servidor')
        self.exitButton = QPushButton('Encerrar servidor')
        self.subLayout.addWidget(self.initButton)
        self.subLayout.addWidget(self.exitButton)
        self.layout.addLayout(self.subLayout)

        self.setLayout(self.layout)

        self.initButton.clicked.connect(self.onClickInit)
        self.exitButton.clicked.connect(self.onClickExit)

    @pyqtSlot()
    def onClickInit(self):
        self.data = {}
        self.data['Email receiver'] = self.emailReceiver.text()
        self.data['Password receiver'] = self.passwordReceiver.text()
        self.data['Email sender'] = self.emailSender.text()
        
        self.initButton.setEnabled(False)

        self.mainLoop()

    def onClickExit(self):
        sys.exit()

    def mainLoop(self):
        print('Be sure to enable the access on your email.')
        print('If you are not sure, check on:', ENABLE_LESS_SECURE_APPS_URL)
        print('Be sure to enable the access of the module IMAP Lib on your email\n'
            'You should go to your email settings and enable the access of IMAP')
        print('Starting program...')

        while True:
            """
            This server shall be running until EOF.
            Obs. It's only available for windows for now.
            """
            try:
                # Connects
                account = GmailAccount(self.data['Email receiver'],
                                    self.data['Password receiver'],
                                    self.data['Email sender'])
                # Get printer
                printer = Printer()
                # Get new attachments
                attachments = account.run()
                # Iterator over them, print and delete.
                for attachment in attachments:
                    print('Printing: ', attachment.split('/')[len(attachment.split('/')) - 1])
                    # Print the attachment pdf
                    printer.run(attachment)
                    print('Deleting...')
                    # Delete the attachment from the pc memmory
                    os.remove(attachment)
            
            except EOFError:
                # If EOF, quit server.
                account.quit()
                break
            else:
                # Try again.
                continue

if __name__ == '__main__':
    root = QApplication(sys.argv)
    app = MainInterface()
    app.show()
    sys.exit(root.exec_())