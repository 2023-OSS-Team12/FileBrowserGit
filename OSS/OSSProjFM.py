import sys
import os

import git
from git import Repo
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
import subprocess
import platform
import shutil
import pathlib

from git import Repo


class FileSearcher:
    def __init__(self, root_path):
        self.root_path = root_path

    def search_file(self, name, filetype):
        for dirpath, dirname, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename == f"{name}":
                    return os.path.join(dirpath, filename)
        return None

    def list_files(self):
        return os.listdir(self.root_path)

def move_file(filePath, folder_path):
    shutil.move(filePath, folder_path)

def open_file(findPath):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(findPath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', findPath))


class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.searcher = FileSearcher("/")  # Create a FileSearcher object with root path '/'
        self.selected_files = []
        layout = self.layout()

        # Add widgets for file searching and manipulation
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)
        layout.addWidget(browse_button)

        open_button = QPushButton("Git Init")
        open_button.clicked.connect(self.init_repository)
        layout.addWidget(open_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        add_button = QPushButton("Git Add")
        add_button.clicked.connect(self.gitadd)
        layout.addWidget(add_button)

    def init_repository(self, bare=False):
        path = self.getExistingDirectory(self, 'search folder to git init', './')
        repo = Repo.init(path)
        repo.index.add(['new.txt'])

    def gitadd(self):
        #pathrepo = self.getExistingDirectory(self, 'search folder to git add', './')
        pathfile = self.getOpenFileName(self,'search file to git add', './')
        print(pathfile)
        repo = git.Repo(pathfile)
        repo.index.add([pathfile])

    def gitcommit(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        repo = Repo(fname)
        repo.index.commit("commited")∂

    def browse(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.searcher = FileSearcher(folder_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()
    if dialog.exec_() == QFileDialog.Accepted:
        print(dialog.selectedFiles())
    sys.exit(app.exec_())
