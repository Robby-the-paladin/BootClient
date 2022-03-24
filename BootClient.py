from git import Repo
from git import RemoteProgress
from PyQt6 import QtWidgets
import sys
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.window = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 510, 571, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 490, 161, 81))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.PATH_OF_GIT_REPO = r'C:\\Users\\mea25\\Desktop\\BootClient\\BootClient\\.git'  # make sure .git folder is properly configured
        self.COMMIT_MESSAGE = 'Pyhon commit'

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(lambda: self.git_push())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

    def createProgressPrinter(self):
        return Ui_MainWindow.ProgressPrinter(self)

    class ProgressPrinter(RemoteProgress):
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def update(self, op_code, cur_count, max_count=None, message=''):
            print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

    def git_push(self):
        try:
            repo = Repo(self.PATH_OF_GIT_REPO)
            repo.git.add(update=True)
            repo.git.add("BootClient.py")
            repo.git.add("env")
            repo.index.commit(self.COMMIT_MESSAGE)
            origin = repo.remote(name='origin')
            origin.push(progress=self.createProgressPrinter())
        except:
            print('Some error occured while pushing the code')

    def git_pull(self):
        try:
            repo = Repo(self.PATH_OF_GIT_REPO)
            origin = repo.remote(name='origin')
            origin.pull(progress=self.createProgressPrinter())
        except:
            print('Some error occured while pulling the code')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec())
