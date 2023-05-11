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
    selected_files = []
    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.searcher = FileSearcher("/")  # Create a FileSearcher object with root path '/'

        layout = self.layout()

        # Add widgets for file searching and manipulation
        restore_button = QPushButton("Git Restore")
        restore_button.clicked.connect(self.git_restore)
        layout.addWidget(restore_button)

        open_button = QPushButton("Git Init")
        open_button.clicked.connect(self.init_repository)
        layout.addWidget(open_button)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        add_button = QPushButton("Git Add")
        add_button.clicked.connect(self.git_add)
        layout.addWidget(add_button)

    def init_repository(self, bare=False):
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        Repo.init(filelocation)  # git init(폴더 내 파일을 선택하였을 때)
    def path(self,dir):
        FileDialog.selected_files = dir
    def git_add(self, selected_files): # git add누르면
        '''
        pathrepo = self.getExistingDirectory(self, 'search folder to git add', './')
        print("path repo",pathrepo)
        repo = git.Repo(pathrepo)
        repo.index.add('new.txt')
        '''
        index = FileDialog.selected_files[0].split('/')# 파일 위치를 불러옴, /로 나눔
        filename = index[-1]#파일 이름만 저장
        index.remove(filename)
        filelocation = ""#파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.index.add(filename)
        print(filename,"is on staged")

    def git_restore(self):# restore 기능임
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.git.reset(filename)
        print(filename, "is on untracked")

    def git_commit(self):#not implement
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        repo = Repo(fname)
        repo.index.commit("commited")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()
    dialog.exec_()

    while(dialog.exec_() == QFileDialog.Accepted):#exit하기 전까지 무한 반복
        print(dialog.selectedFiles())#경로 나오는지 print
        #dialog.selectedFiles()
        dialog.selected_files = dialog.selectedFiles()#경로 선택해서 저장
        dialog.path(dialog.selectedFiles())

    sys.exit(app.exec_())