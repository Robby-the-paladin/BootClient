import os.path
import sys

import git
from git import Repo
from git import RemoteProgress
from PyQt6 import QtWidgets
from threading import Thread

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject, QTextCodec, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class Document(QObject):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_text = ""

    def get_text(self):
        return self.m_text

    def set_text(self, text):
        if self.m_text == text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    text = pyqtProperty(str, fget=get_text, fset=set_text, notify=textChanged)


class DownloadManager(QObject):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_finished)

    @property
    def manager(self):
        return self._manager

    def start_download(self, url):
        self.manager.get(QNetworkRequest(url))

    def handle_finished(self, reply):
        if reply.error() != QNetworkReply.NoError:
            print("error: ", reply.errorString())
            return
        codec = QTextCodec.codecForName("UTF-8")
        raw_data = codec.toUnicode(reply.readAll())
        self.finished.emit(raw_data)

from PyQt5 import QtCore, QtGui, QtWidgets

class DownloadManager(QObject):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_finished)

    @property
    def manager(self):
        return self._manager

    def start_download(self, url):
        self.manager.get(QNetworkRequest(url))

    def handle_finished(self, reply):
        if reply.error() != QNetworkReply.NoError:
            print("error: ", reply.errorString())
            return
        codec = QTextCodec.codecForName("UTF-8")
        raw_data = codec.toUnicode(reply.readAll())
        self.finished.emit(raw_data)

class Signaller(QObject):
    progress_changed = pyqtSignal(int)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(7, 532, 631, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 530, 141, 51))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 20, 631, 491))
        self.widget.setObjectName("widget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.PATH_OF_GIT_REPO = r'C:\\Users\\mea25\\Desktop\\BootClient\\BootClient\\.git'  # make sure .git folder is properly configured
        self.COMMIT_MESSAGE = 'Pyhon commit'

        self.pushButton.clicked.connect(lambda: self.button_func())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

    class ProgressPrinter(RemoteProgress):
        def setProgress(self, progress):
            self.progress = progress

        def update(self, op_code, cur_count, max_count=None, message=''):
            print(op_code, cur_count, max_count, cur_count * 100 / (max_count or 100.0), message or "NO MESSAGE")
            self.progress.emit(int(cur_count * 100 / (max_count or 100.0)))
            #ui.progressBar.setValue(int(cur_count * 100 / (max_count or 100.0)))

    def button_func(self):
        print("button")
        self.thread = self.git_clone()
        self.thread.init_progress_printer(self.ProgressPrinter())
        self.thread.start()
        self.thread.update_progress.connect(self.evt_update_progress)

    def evt_update_progress(self, val):
        self.progressBar.setValue(val)


    class git_push(QtCore.QThread):
        update_progress = pyqtSignal(int)
        def init_progress_printer(self, printer):
            self.printer = printer

        def __init__(self):
            QtCore.QThread.__init__(self)

        def __del__(self):
            self.wait()

        def run(self):
            try:
                self.printer.setProgress(self.update_progress)
                repo = Repo(self.PATH_OF_GIT_REPO)
                repo.git.add(update=True)
                repo.git.add("BootClient.py")
                repo.git.add("env")
                repo.index.commit(self.COMMIT_MESSAGE)
                origin = repo.remote(name='origin')
                origin.push(progress=self.printer)
                print("pushed")
            except:
                print('Some error occured while pushing the code')

    class git_pull(QtCore.QThread):
        update_progress = pyqtSignal(int)
        def init_progress_printer(self, printer):
            self.printer = printer

        def __init__(self):
            QtCore.QThread.__init__(self)

        def __del__(self):
            self.wait()

        def run(self):
            try:
                self.printer.setProgress(self.update_progress)
                repo = Repo(self.PATH_OF_GIT_REPO)
                origin = repo.remote(name='origin')
                origin.pull(progress=self.printer)
                print("pulled")
            except:
                print('Some error occured while pulling the code')

    class git_clone(QtCore.QThread):
        update_progress = pyqtSignal(int)
        def init_progress_printer(self, printer):
            self.printer = printer

        def __init__(self):
            QtCore.QThread.__init__(self)

        def __del__(self):
            self.wait()

        def run(self):
            try:
                self.printer.setProgress(self.update_progress)
                git.Repo.clone_from(
                    url="https://github.com/u-boot/u-boot",
                    to_path="u-boot",
                    depth=1,
                    progress=self.printer,
                )
                print("cloned")
            except:
                print('Some error occured while cloning the code')


from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    filename = os.path.join(CURRENT_DIR, "index.html")

    document = Document()
    download_manager = DownloadManager()

    channel = QWebChannel()
    channel.registerObject("content", document)

    # remote file
    markdown_url = QUrl.fromUserInput("https://raw.githubusercontent.com/eyllanesc/stackoverflow/master/README.md")
    # local file
    # markdown_url = QUrl.fromLocalFile("README.md")

    download_manager.finished.connect(document.set_text)
    download_manager.start_download(markdown_url)

    ui.widget.page().setWebChannel(channel)
    url = QUrl.fromLocalFile(filename)
    ui.widget.load(url)

    MainWindow.show()
    sys.exit(app.exec_())